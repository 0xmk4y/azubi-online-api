from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

# GET /cart: Retrieve the current state of the shopping cart
@router.get("/", response_model=List[schemas.CartItemResponse])
def read_cart(db: Session = Depends(get_db)):
    return crud.get_cart(db)

# POST /cart: Add a product to the cart
@router.post("/", response_model=schemas.CartItemResponse)
def add_to_cart(cart_item: schemas.CartItemBase, db: Session = Depends(get_db)):
    return crud.add_to_cart(db, cart_item)

# PUT /cart/:id: Update the quantity of a product in the cart
@router.put("/{cart_id}", response_model=schemas.CartItemResponse)
def update_cart_item(cart_id: int, cart_item: schemas.CartItemBase, db: Session = Depends(get_db)):
    updated_item = crud.update_cart_item(db, cart_id, cart_item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item

# DELETE /cart/:id: Remove a product from the cart
@router.delete("/{cart_id}", response_model=schemas.CartItemResponse)
def delete_cart_item(cart_id: int, db: Session = Depends(get_db)):
    cart_item = crud.delete_cart_item(db, cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item
