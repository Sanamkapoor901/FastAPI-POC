from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from product.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductPaginationResponse
from product.crud import create_product, get_product, get_products, update_product, delete_product
from dependencies import get_current_user
from user.schemas import UserResponse

router = APIRouter()

@router.post("/product/", response_model=ProductResponse)
async def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    return create_product(db=db, product=product, user_id=current_user.id)

@router.get("/products/", response_model=ProductPaginationResponse)
async def get_products_endpoint(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user),
    search: Optional[str] = None,
    name: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    quantity_min: Optional[int] = None,
    quantity_max: Optional[int] = None
):
    products_count, products = get_products(db=db, user_id=current_user.id, skip=skip, limit=limit,
                                            search=search, name=name, price_min=price_min, price_max=price_max,
                                            quantity_min=quantity_min, quantity_max=quantity_max)

    return {"total": products_count, "skip": skip, "limit": limit, "products": products}

@router.get("/product/all/", response_model=ProductPaginationResponse)
async def get_all_products_endpoint(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user),
    search: Optional[str] = None,
    name: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    quantity_min: Optional[int] = None,
    quantity_max: Optional[int] = None
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Not authorized to access this resource")

    products_count, products = get_products(db=db, skip=skip, limit=limit, search=search,
                                            name=name, price_min=price_min, price_max=price_max,
                                            quantity_min=quantity_min, quantity_max=quantity_max)

    return {"total": products_count, "skip": skip, "limit": limit, "products": products}

@router.get("/product/{product_id}/", response_model=ProductResponse)
async def get_product_endpoint(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
):
    product = get_product(db=db, product_id=product_id, user_id=current_user.id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/product/{product_id}/", response_model=ProductResponse)
async def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    db_product = update_product(db=db, product_id=product_id, product_update=product, user_id=current_user.id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/product/{product_id}/", response_model=dict)
async def delete_product_endpoint(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
):
    db_product = delete_product(db=db, product_id=product_id, user_id=current_user.id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

