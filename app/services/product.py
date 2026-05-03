from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: str
    name: str
    price: float

products: List[Product] = []



