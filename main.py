from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return {"message" : "Hello FastApi Learner"}

@app.get("/about")
def aboutMe():
    return {"Message" : "This is all the abouts about me"}

products = [
    Product(id = 101,name = "pen",price = 10,quantity = 100, description ="blue gel pen"),
    Product(id = 102,name = "pencil",price = 5,quantity = 200, description ="Natraj pencil"),
    Product(id = 103,name = "Eraser",price = 7,quantity = 200, description ="20gms eraser"),
    Product(id = 104,name = "Sharpner",price = 8,quantity = 200, description ="quicky sharpner"),
]

@app.get("/product")
def get_products():
    return products