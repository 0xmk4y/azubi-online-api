from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List
from utils import authenticate


router = APIRouter()

# GET /products: Retrieve a list of all products
@router.get("/", response_model=List[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

# GET /products/:id: Retrieve details of a specific product by ID
@router.get("/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# POST /products: Add a new product (admin functionality)
@router.post("/", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    return crud.create_product(db, product)

# PUT /products/:id: Update an existing product (admin functionality)
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    updated_product = crud.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# DELETE /products/:id: Delete a product (admin functionality)
@router.delete("/{product_id}", response_model=schemas.ProductResponse)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
