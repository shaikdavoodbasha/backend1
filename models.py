#here we need two classes one is for create database and vlaues
# another one is for retreving those values

from sqlmodel import SQLModel,Field
from typing import Optional

class User(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str
    phone:int
    email:str

#this class is used to create tables very important

#this one is for sending and retreving the data 
class CreateUser(SQLModel):
    name:str
    phone:int
    email:str

