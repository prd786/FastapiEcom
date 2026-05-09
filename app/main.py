
from fastapi import FastAPI, HTTPException , Path, Depends
from services.product import Product
from services.pydbconn import init_db, get_db, Product as DBProduct
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app")
    init_db()
    yield
    print("Shutting down app")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "welcome to fast api tutorial"}

@app.get("/products")
def read_products(db: Session = Depends(get_db)):
    products = db.query(DBProduct).all()
    return products

@app.get("/products/{product_id}")
def get_product(product_id: str = Path(..., description="The ID of the product to retrieve", examples=["123"]), db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
        
@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = DBProduct(id=product.id, name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "saved", "product": db_product}

# Example: Calling PostgreSQL Function/Procedure with Parameters
@app.get("/products-by-price/{price}")
def get_products_by_price(price: float = Path(..., description="Maximum price filter", examples=[50.0]), db: Session = Depends(get_db)):

    try:
        # Method 1: Using text() to execute raw SQL
        query = text("SELECT * FROM get_products_by_max_price(:max_price)")
        result = db.execute(query, {"max_price": price})
        products = result.fetchall()
        
        if not products:
            return {"message": "No products found", "products": []}
        
        return {
            "message": f"Products with price <= {price}",
            "products": [{"id": p[0], "name": p[1], "price": p[2]} for p in products]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling function: {str(e)}")

# Example 2: Using stored procedure with multiple parameters
@app.get("/product-search/{min_price}/{max_price}")
def search_products_by_price_range(
    min_price: float = Path(..., description="Minimum price", examples=[10.0]),
    max_price: float = Path(..., description="Maximum price", examples=[100.0]),
    db: Session = Depends(get_db)
):

    try:
        query = text("SELECT * FROM get_products_by_price_range(:min_price, :max_price)")
        result = db.execute(query, {"min_price": min_price, "max_price": max_price})
        products = result.fetchall()
        
        return {
            "message": f"Products between {min_price} and {max_price}",
            "products": [{"id": p[0], "name": p[1], "price": p[2]} for p in products]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Example 3: Calling procedure (not returning result set)
@app.post("/update-product-price/{product_id}/{new_price}")
def update_product_price(
    product_id: int = Path(..., description="Product ID", examples=["1"]),
    new_price: int = Path(..., description="New price", examples=[99.99]),
    db: Session = Depends(get_db)
):

    try:
        # Call procedure
        db.execute(text("CALL update_product_price(:product_id, :new_price)"), 
                  {"product_id": product_id, "new_price": new_price})
        db.commit()
        return {"message": f"Product {product_id} price updated to {new_price}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")












