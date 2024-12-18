from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas
from fastapi import HTTPException
import json

# --- Product Operations ---

def get_products(db: Session):
    """Retrieve all products."""
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    """Retrieve a specific product by ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    """Create a new product."""
    db_product = models.Product(**product.model_dump())
    db_product.images = str(db_product.images)
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating product")

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    """Update an existing product."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    for key, value in product.dict().items():
        setattr(db_product, key, value)   
    db_product.images = str(db_product.images)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """Delete a product by ID."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


# --- Cart Operations ---

def get_cart(db: Session):
    """Retrieve all items in the shopping cart."""
    return db.query(models.CartItem).all()

def get_cart_item_by_id(db: Session, cart_id: int):
    """Retrieve a specific cart item by ID."""
    return db.query(models.CartItem).filter(models.CartItem.id == cart_id).first()

def add_to_cart(db: Session, cart_item: schemas.CartItemBase):
    """Add a product to the cart."""
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.product_id == cart_item.product_id).first()
    if db_cart_item:
        # If the product is already in the cart, increase the quantity
        db_cart_item.quantity += cart_item.quantity
    else:
        # Otherwise, create a new cart item
        db_cart_item = models.CartItem(**cart_item.dict())
        db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def update_cart_item(db: Session, cart_id: int, cart_item: schemas.CartItemBase):
    """Update the quantity of a product in the cart."""
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_id).first()
    if not db_cart_item:
        return None
    db_cart_item.quantity = cart_item.quantity
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def delete_cart_item(db: Session, cart_id: int):
    """Remove a product from the cart."""
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_id).first()
    if not db_cart_item:
        return None
    db.delete(db_cart_item)
    db.commit()
    return db_cart_item
