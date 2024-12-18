from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = None
    price: float
    images: Optional[Dict[str, str]] = None  # JSON-compatible dictionary

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    images: str = None

    model_config = ConfigDict(from_attributes=True)

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(CartItemBase):
    id: int
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)
