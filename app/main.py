from fastapi import FastAPI
from services.products import get_all_product , get_product_by_id

app = FastAPI()
@app.get("/")

def read_root():
    return {"message": "welcome to fast api tutorial"}

@app.get("/products")       
def get_products():
    return get_all_product()

@app.get("/products/{product_id}")
def get_product(product_id: str):
    return get_product_by_id(product_id)













