# from fastapi import FastAPI,Depends,HTTPException
# from sqlmodel import SQLModel,create_engine,Session,select
# from contextlib import asynccontextmanager
# from typing import Annotated #for typeints
# from models import User,CreateUser

# DATABASE_URL = "sqlite:///./users.db" #here this will crates users.db file inside our folder
# engine = create_engine(DATABASE_URL,echo=True)
# #this is creating an sql evironment
# #event handler used create the database and connect the data base

# @asynccontextmanager #Event handler for creating table and connect to the database model to the mainfile
# async def lifespan(app:FastAPI):
#     SQLModel.metadata.create_all(engine)
#     yield
# #this is used for when server start ,when the are not table used to create tables and used to connecting to the database

# app = FastAPI(lifespan=lifespan)

# #now we are creating one dependenci for maintaining sessions 

# def get_session():
#     with Session(engine) as session:
#         yield session
# # This Environment is setup once at the beginning of the any backend project using fast FastAPI
# # so we need not to worry a lot about it once you understand it then you can start your another work

# SessionDep = Annotated[Session,Depends(get_session)]
# #this is line is for when we connect to data verify wheather session is present or not



# @app.post("/createuser")
# def create_user(user:CreateUser,session:SessionDep):
#     new_user = User.model_validate(user)
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)
#     return new_user


# #here why we are using the response model  beacuse to getting the response data in list format
# @app.get('/allusers',response_model=list[User])
# def get_users(session:SessionDep):
#     users = session.exec(select(User)).all()
#     if not users:
#         raise HTTPException(status_code=404,details="User Not found")
#     return users


# @app.get('/users/{user_id}',response_model=User)
# def get_single_user(user_id:int,session:SessionDep):
#     user = session.get(User,user_id)
#     if not user:
#         raise HTTPException(status_code=404,detail="User Not Found")
#     return user