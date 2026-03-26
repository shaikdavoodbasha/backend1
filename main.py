from fastapi import FastAPI,HTTPException
from typing import Optional
from pydantic import BaseModel,Field
app = FastAPI()
#here app is object

#@app is a decorator
@app.get('/') #root path or root directory
def root_url():
    #business logic here
    return {"message":"Welcome to fast api"}

@app.get('/one')
def one():
    return {"message":"Welcome to second page"}

@app.get('/two')
def two():
    return {"message":"welcome to third page"}

users = {
    1:{"name":"Teja",
       "torders":"Laptop,phone,Charger",
       "orders":{
           101:"laptop",
           102:"phone"
       }
       },
    2:{"name":"Sai Sumanth",
       "torders":"mac,airpod",
       "orders":{
           201:"mac",
           202:"AirPod"
       }
       },
    3:{"name":"Nithish",
       "torders":"Mac Mini,Chair",
       "orders":{
           301:"Mac Mini",
           302:'Chair'
       }
       },
    4:{"name":"Siva Tharun",
       "torders":"Spects,Charger",
       "orders":{
           401:"Charger",
           402:"Spects"
       }       }
}
people =[
    {"id": 1, "name": "Rahul", "age": 22, "city": "Bangalore"},
    {"id": 2, "name": "Anjali", "age": 25, "city": "Hyderabad"},
    {"id": 3, "name": "Kiran", "age": 28, "city": "Chennai"},
    {"id": 4, "name": "Sneha", "age": 21, "city": "Bangalore"}
]
#These are examples of Path perameters,Path perameter are default you must give them bro 
@app.get('/user/{user_id}/torders')
def get_users(user_id:int):
    return users[user_id]["torders"]


@app.get('/user/{user_id}/orders/{order_id}')
def get_users(user_id:int,order_id:int):
    return users[user_id]["orders"][order_id]

#Query parameter:This is also same as path parameter but it is a optional not mandatory

@app.get('/people')
def peoples_data(city:Optional[str]=None,age:Optional[int]=None):
    if(city):
        result = list(filter(lambda user: user["city"] == city, people))
        return result
    
    if(age):
        age_result = list(filter(lambda user:user['age']>age,people))
        return age_result
    # else:
    #     raise HTTPException(status_code={202})


#pydantic models bro 
class Products(BaseModel):
    pname:str = Field(...,min_length=3)
    pnumber:int

all_product = {}
product_id = 1
@app.post('/create')
def create_product(product:Products):
    global product_id
    all_product[product_id] = product
    response ={
        "message":"product added successfully",
        "product_id":product_id,
        "prodcts":all_product[product_id]
    }
    product_id += 1
    return response

@app.get('/products')
def products():
    return all_product

#CURD Operations Broo😁
@app.put('/products/{product_id}')
def product_up(product_id:int,products:Products):
    if product_id not in all_product:
        raise HTTPException(status_code=404,detail='Product Not found')
    all_product[product_id]=products
    return {"messaage":"Product updated","product":products}

@app.delete('/products/{product_id}')
def product_deleting(product_id:int):
    if product_id not in all_product:
        raise HTTPException(status_code=404,detail="product not found")
    delete = all_product.pop(product_id)
    return {"message":"Product deleted Successfully","user":delete}