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
def get_product_by_id(id: int, db : Session = Depends(get_db)):
    
    """
    db : Session = Depends(get_db) -> FastAPI’s dependency system runs the get_db() function 
                                            and injects its returned Session object into db
    db.query(dbModels.Product) -> fetch data from the Product table
    .filter(dbModels.Product.id == id) -> Adds a WHERE clause to the SQL query so only 
                                            the product with that specific id is selected
    .first() -> to return the first matching row only.
    """
    
    db_pdt = db.query(dbModels.Product).filter(dbModels.Product.id == id).first()
    if db_pdt:
        return db_pdt
    return "Product not found"

@app.post("/product")
def add_new_product(nw_pdt : Product, db : Session = Depends(get_db)):
    db.add(dbModels.Product(**nw_pdt.model_dump()))
    db.commit()
    return nw_pdt

@app.post("/addMoreProducts")
def add_more_products(nw_pdt : List[Product],  db : Session = Depends(get_db)):
    pdts = []
    for pdt in nw_pdt:
        pdts.append(dbModels.Product(**pdt.model_dump()))
    db.add_all(pdts)
    db.commit()
    return {
        "message": f"Successfully added {len(nw_pdt)} product(s)",
        "added": nw_pdt
    }

@app.put("/product/{id}")
def update_product(id: int, pdt: Product, db: Session = Depends(get_db)):
    db_pdt = db.query(dbModels.Product).filter(dbModels.Product.id == id).first()

    if not db_pdt:
        return {"error": "Product not found"}

    """
        pdt → Pydantic model (data coming from request body)
        model_dump() → converts Pydantic model into a dictionary
        exclude_unset=True → only includes fields sent by user
        .items() → gives (key, value) pairs
        setattr() → updates the SQLAlchemy model field dynamically.

    """
    for key, value in pdt.model_dump(exclude_unset=True).items():
        setattr(db_pdt, key, value)

    db.commit()
    db.refresh(db_pdt)

    return db_pdt


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