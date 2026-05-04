from pydantic import BaseModel
from typing import List
from .products import get_all_product

class Product(BaseModel):
    id: str
    name: str
    price: float

    model_config = {
        "extra": "allow"
    }

products: List[Product] = [Product(**item) for item in get_all_product()]



