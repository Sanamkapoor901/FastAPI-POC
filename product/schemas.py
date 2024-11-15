# schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from user.schemas import UserResponse

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class ProductResponse(ProductBase):
    id: int
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)


class ProductPaginationResponse(BaseModel):
    total: int
    skip: int
    limit: int
    products: List[ProductResponse]

    model_config = ConfigDict(from_attributes=True)