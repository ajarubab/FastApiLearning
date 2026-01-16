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
    Product(1,"pen",10,15,"blue gel pen"),
    Product(2,"pencil",5,60,"40 cm natraj pencil"),
]

@app.get("/product")
def get_products():
    return products