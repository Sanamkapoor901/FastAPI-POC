from sqlalchemy import or_
from sqlalchemy.orm import Session
from product.models import Product
from product.schemas import ProductCreate, ProductUpdate
from typing import List, Optional, Tuple

def get_product(db: Session, product_id: int, user_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id, Product.created_by == user_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None,
                name: Optional[str] = None, price_min: Optional[float] = None,
                price_max: Optional[float] = None, quantity_min: Optional[int] = None,
                quantity_max: Optional[int] = None, user_id: Optional[int] = None) -> Tuple[int, List[Product]]:

    query = db.query(Product)

    # Apply search if it exists
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    # Apply filters if they exist
    if user_id:
        query = query.filter(Product.created_by == user_id)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if price_min:
        query = query.filter(Product.price >= price_min)
    if price_max:
        query = query.filter(Product.price <= price_max)
    if quantity_min:
        query = query.filter(Product.quantity >= quantity_min)
    if quantity_max:
        query = query.filter(Product.quantity <= quantity_max)

    total = query.count()
    query = query.offset(skip).limit(limit).all()

    return total, query

def create_product(db: Session, product: ProductCreate, user_id: int) -> Product:
    product = Product(**product.model_dump(), created_by=user_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product_id: int, product_update: ProductUpdate, user_id: int) -> Optional[Product]:
    product = db.query(Product).filter(Product.id == product_id, Product.created_by == user_id).first()
    if product:
        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: int, user_id: int) -> Optional[Product]:
    product = db.query(Product).filter(Product.id == product_id, Product.created_by == user_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product
