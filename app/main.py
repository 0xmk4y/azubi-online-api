from fastapi import FastAPI
from database import Base, engine
from routes import products, cart


app = FastAPI(
    title="Shopping Cart API",
    description="API for managing products and a shopping cart",
    version="1.0.0",
    debug=True
)

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9024, reload=True)
