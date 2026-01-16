class Product:
    id : int
    name: str
    price : float
    quantity : int
    description : str

    def __init__(self,id: int,name: str,price: float,quantity: int,description : str):
        self.id = id
        self.name= name
        self.price = price
        self.quantity = quantity
        self.description = description
