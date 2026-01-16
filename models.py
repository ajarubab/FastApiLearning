from pydantic import BaseModel
from typing import Optional

# For new data creation or full updation
class Product(BaseModel):
    id : int
    name: str
    price : float
    quantity : int
    description : str

#  For partial update
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None