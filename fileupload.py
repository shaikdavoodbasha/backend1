from fastapi import FastAPI, Depends, HTTPException, Form, File, UploadFile
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated
from models import User, CreateUser   # ✅ fixed import
import os
import shutil
import uuid   # ✅ for unique filenames

# ---------------- DATABASE ---------------- #
DATABASE_URL = "sqlite:///./users.db"
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

# ---------------- FILE STORAGE ---------------- #
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# ---------------- API ---------------- #
@app.post("/createuser")
def create_user(
    session: SessionDep,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    # ✅ Validate input
    user_data = {"name": name, "phone": phone, "email": email}
    validated = CreateUser.model_validate(user_data)

    # ✅ Check duplicate email
    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # ✅ Unique filename
    file_ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    # file_path = os.path.join(UPLOADS_DIR, unique_filename)
    file_path = os.path.abspath(os.path.join(UPLOADS_DIR, unique_filename))
    # ✅ Save file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # ✅ Create user
    user = User(
        **validated.model_dump(),
        file_path=file_path   # ✅ store full path
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "User created successfully",
        "data": user
    }