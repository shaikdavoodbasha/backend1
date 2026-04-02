# from fastapi import FastAPI,Depends,HTTPException,Form,File,UploadFile
# from sqlmodel import SQLModel,create_engine,Session,select
# from contextlib import asynccontextmanager
# from typing import Annotated
# from models import User,CreateUser
# import os,shutil
# from pydantic import ValidationError



# DATABASE_URL = "sqlite:///./users.db"
# engine = create_engine(DATABASE_URL,echo=True)

# #background runner handler for creating tables and connecting to the data base

# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     SQLModel.metadata.create_all(engine)
#     yield

# app =FastAPI(lifespan=lifespan)

# def get_session():
#     with Session(engine) as session:
#         yield session

# SessionDep = Annotated[Session,Depends(get_session)]

# # @app.post("/createuser")
# # def create_user(user:CreateUser,session:SessionDep):
# #     new_user = User.model_validate(user)
# #     session.add(new_user)
# #     session.commit()
# #     session.refresh(new_user)
# #     return new_user

# # @app.get("/users",response_model=list[User])
# # def get_users(session:SessionDep):
# #     users = session.exec(select(User)).all()
# #     if not users:
# #         raise HTTPException(status_code=404,detail = "User Not found")
# #     return users


# # @app.get("/users/{user_id}",response_model=User)
# # def get_single_user(user_id:int,session:SessionDep):
# #     user = session.get(User,user_id)
# #     if not user:
# #         raise HTTPException(status_code=404,detail="User Not Found buddy.")
# #     return user

# # @app.put("/users/{user_id}",response_model=User)
# # def update_user(user_id:int,update:CreateUser,session:SessionDep):
# #     user = session.get(User,user_id)
# #     if not user:
# #         raise HTTPException(status_code=404,detail="User Not Found buddy.")
    
# #     user.name = update.name
# #     user.phone = update.phone
# #     user.email = update.email
# #     session.add(user)
# #     session.commit()
# #     session.refresh(user)
# #     return user

# # @app.delete("/users/{user_id}")
# # def delete_user(user_id:int,session:SessionDep):
# #     user = session.get(User,user_id)
# #     if not user:
# #         raise HTTPException(status_code=404,detail="User Not Found buddy.")
# #     session.delete(user)
# #     session.commit()
# #     return {"message":"user deleted successfull"}


# UPLOADS_DIRS = "uploads"
# os.makedirs(UPLOADS_DIRS,exist_ok=True)

# @app.post("/createuser")
# def usercreate(
#     session: SessionDep,
#     name: str = Form(...),
#     phone: int = Form(...),
#     email: str = Form(...),
#     file: UploadFile = File(...)
# ):
#     user_data = {"name": name, "phone": phone, "email": email}

#     try:
#         validated = CreateUser.model_validate(user_data)
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=e.errors())

#     file_path = os.path.join(UPLOADS_DIRS, file.filename)

#     with open(file_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     user = User(**validated.model_dump(), file_path=file_path)

#     session.add(user)
#     session.commit()
#     session.refresh(user)

#     return user
#     #here why we are using that two starts means to convert the data into dictionary



from fastapi import FastAPI, Depends, HTTPException, Form, File, UploadFile
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from typing import Annotated
from models import User, CreateUser
from pydantic import ValidationError
import os
import shutil

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, echo=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)


@app.post("/createuser")
def usercreate(
    session: SessionDep,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # validate input using CreateUser model
        validated = CreateUser(
            name=name,
            phone=phone,
            email=email
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    # save file
    file_path = os.path.join(UPLOADS_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # create DB object
    user = User(
        name=validated.name,
        phone=validated.phone,
        email=validated.email,
        file_path=file_path
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user