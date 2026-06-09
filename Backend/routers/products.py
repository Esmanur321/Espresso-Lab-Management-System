"""
==============================================
routers/products.py - Product CRUD Endpoints
==============================================

GET    /products         → List all products
GET    /products/{id}    → Get single product
POST   /products         → Create new product
PUT    /products/{id}    → Update product
DELETE /products/{id}    → Soft delete product
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Product
from schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[ProductResponse], summary="List all products")
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    Returns all active products from the database.
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return
    - **category**: Filter by category (optional)
    """
    query = db.query(Product).filter(Product.is_active == True)

    if category:
        query = query.filter(Product.category == category)

    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductResponse, summary="Get single product")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Returns a single product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found (ID: {product_id})"
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Create new product")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """
    Creates a new product.

    Required fields: **name**, **price**
    """
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/{product_id}", response_model=ProductResponse, summary="Update product")
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    """Updates an existing product. Only the provided fields are updated."""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found (ID: {product_id})"
        )

    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Soft deletes a product (sets is_active=False).
    The product is not permanently removed from the database.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found (ID: {product_id})"
        )

    product.is_active = False
    db.commit()
    return None
