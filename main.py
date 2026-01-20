from fastapi import FastAPI, Depends
from models import Product, ProductUpdate
from typing import List
from dbConfig import session, engine
import dbModels
from sqlalchemy.orm import Session

app = FastAPI()

# binding postgresql to vscode to create table according to dbModels via dbConfig
dbModels.Base.metadata.create_all(bind=engine)

# Global method for session opening and closing
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return {"message" : "Hello FastApi Learner"}

@app.get("/about")
def aboutMe():
    return {"Message" : "This is all the abouts about me"}

products = [
    Product(id = 101,name = "pen",price = 10,quantity = 100, description ="blue gel pen"),
    Product(id = 102,name = "pencil",price = 5.5,quantity = 200, description ="Natraj pencil"),
    Product(id = 103,name = "Eraser",price = 7.5,quantity = 200, description ="20gms eraser"),
    Product(id = 104,name = "Sharpner",price = 8,quantity = 200, description ="quicky sharpner"),
]

# INITIALISING THE DATABSE TABLE PRODUCT WITH THE PYDANTIC TYPE DATA PRODUCTS CONVERTED INTO DPMODALS TYPE DATA ON 0 OBJECT(ROW) COUNT ONLY
def db_init():
    db = session()
    count = db.query(dbModels.Product).count()

    if count == 0:
        for pdt in products:
            db.add(dbModels.Product(**pdt.model_dump()))
        db.commit()

db_init()


@app.get("/products")
def get_all_products(db : Session = Depends(get_db)):
    db_pds = db.query(dbModels.Product).all()
    return db_pds

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for pdt in products:
        if pdt.id == id:
            return pdt
    
    return "Product not found"

@app.post("/product")
def add_new_product(nw_pdt : Product):
    products.append(nw_pdt)
    return nw_pdt

@app.post("/addMoreProducts")
def add_more_products(nw_pdt : List[Product]):
    products.extend(nw_pdt)
    return {
        "message": f"Successfully added {len(nw_pdt)} product(s)",
        "added": nw_pdt
    }

@app.put("/product/{id}")
def update_product(id: int, pdt: Product):
    if pdt.id != id:
        return {"error": "ID in URL and body must match"}

    for index, prod in enumerate(products):
        if prod.id == id:
            products[index] = pdt
            return pdt

    return {"error": "Product not found"}


@app.patch("/update/{id}")
def update_products(id: int, pdt: ProductUpdate):
    for prod in products:
        if prod.id == id:
            updates = pdt.model_dump(exclude_unset=True)
            for key, value in updates.items():
                setattr(prod, key, value)
            return prod
    
    return {"error": "Product not found"}

@app.delete("/product")
def delete_product(id: int):
    for i, product in enumerate(products):
        if product.id == id:
            del products[i]
            return {
                "Message" :  "Product Deleted Successfully"
            }

    return {
        "error" : "Product with this Id Not Found"
    }