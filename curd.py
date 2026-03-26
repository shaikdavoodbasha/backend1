from fastapi import FastAPI,HTTPException
from typing import Optional
from pydantic import BaseModel,Field

app = FastAPI()

class Users(BaseModel):
    user_name:str
    user_age:int
    user_address:str
all_users = {}
response = {}
user_id = 1
@app.post('/users')
def create_users(user:Users):
    global all_users
    global user_id
    global response
    all_users[user_id] = user
    response = {
        "message":"User Created Successfully",
        "User_id":user_id,
        "User":all_users[user_id]
    }
    user_id+=1
    return response

@app.get('/users')
def get_users():
    return all_users

@app.get('/users/{user_id}')
def get_users(user_id:int):
    if user_id not in all_users:
        raise HTTPException(status_code=404,detail='user Not Found bro ')
    return all_users[user_id]

@app.put('/users/{user_id}')
def update_user(user_id:int,user:Users):
    if user_id not in all_users:
        raise HTTPException(status_code=404,detail="user not found")
    all_users[user_id]= user
    return all_users