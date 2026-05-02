import json 
from pathlib import Path 
from typing import List ,Dict

print("__file__:", __file__)

DataFile = Path(__file__).resolve().parents[2] / "data" / "products.json"
# DataFile = Path(__file__).parent.parent / "data" / "products.json"
print("Resolved:", Path(__file__).resolve().parents[2] )
print("Path:", DataFile)
print("Exists:", DataFile.exists())

def get_products() ->List[dict]:
    if not DataFile.exists():
     raise FileNotFoundError(f"Data file not found at {DataFile}")
    
    with open(DataFile , 'r', encoding='utf-8' ) as file:
        return json.load(file)
    

def get_all_product() ->List[dict]:
    return get_products()

def get_product_by_id(product_id: str) -> Dict:
    products  = get_products()
    for product in products:
        if product["id"] == product_id:
            return product
    raise ValueError(f"Product with id {product_id} not found")









