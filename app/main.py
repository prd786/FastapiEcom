from fastapi import FastAPI, HTTPException
from services.product import Product, products

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "welcome to fast api tutorial"}

@app.get("/products")
def read_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: str):
    for item in products:
        if item.id == product_id:
            return item
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return {"message": "saved", "product": product}


# @app.post("/products")
# def create_product(product: Product):
#     products.append(product)
#     return {"message": "saved"}

# @app.get("/products")
# def get_products():
#     return products








