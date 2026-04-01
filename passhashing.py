from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated
from hashingmodel import User, CreateUser, LoginUser
from passlib.context import CryptContext

# ---------------- DATABASE ---------------- #
DATABASE_URL = "sqlite:///./hamara.db"
engine = create_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

# ---------------- SESSION ---------------- #
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# ---------------- AUTH ---------------- #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ---------------- REGISTER ---------------- #
@app.post("/register")
def register(session: SessionDep, user_data: CreateUser):

    # ✅ Check if email exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Hash password
    hashed_pwd = hash_password(user_data.password)

    # ✅ Create user
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_pwd
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }

# ---------------- LOGIN ---------------- #
@app.post("/login")
def login(session: SessionDep, login_user: LoginUser):

    # ✅ Check if user exists FIRST
    user = session.exec(
        select(User).where(User.email == login_user.email)
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # ✅ Verify password
    if not verify_password(login_user.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }