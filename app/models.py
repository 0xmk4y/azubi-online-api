from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import json
from typing import Union, Optional
from database import engine

Base = declarative_base()

# Product model with JSON-encoded images
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    images = Column(String) 

# CartItem model with a foreign key relationship to Product
class CartItem(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    product = relationship("Product", back_populates="cart_items")

# Back reference in Product model to CartItem
Product.cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")

# Initialize the database
Base.metadata.create_all(bind=engine)