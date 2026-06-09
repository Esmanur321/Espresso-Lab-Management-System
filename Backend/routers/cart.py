"""
==============================================
routers/cart.py - Cart CRUD Endpoints
==============================================

GET    /cart/{user_id}                     → Get user cart
POST   /cart/{user_id}/items               → Add item to cart
PUT    /cart/{user_id}/items/{item_id}     → Update item quantity
DELETE /cart/{user_id}/items/{item_id}     → Remove item from cart
DELETE /cart/{user_id}                     → Clear entire cart
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import CartItem, Product, User
from schemas import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get("/{user_id}", response_model=CartResponse, summary="Get user cart")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Returns the cart contents for a specific user.
    Also calculates total item count and subtotal.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found (ID: {user_id})")

    items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    total_items = sum(item.quantity for item in items)
    subtotal = sum(item.quantity * item.product.price for item in items)

    return CartResponse(
        items=items,
        total_items=total_items,
        subtotal=round(subtotal, 2)
    )


@router.post("/{user_id}/items", response_model=CartItemResponse, status_code=201, summary="Add item to cart")
def add_to_cart(user_id: int, item_data: CartItemCreate, db: Session = Depends(get_db)):
    """
    Adds a product to the user's cart.

    WEEK 8 - BUSINESS RULE: Stock check is performed.
    If the product is already in the cart, its quantity is increased.
    """
    # Check user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found (ID: {user_id})")

    # Check product exists and is active
    product = db.query(Product).filter(
        Product.id == item_data.product_id,
        Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product not found (ID: {item_data.product_id})")

    # WEEK 8 - STOCK CHECK
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == item_data.product_id
    ).first()
    already_in_cart = existing_item.quantity if existing_item else 0

    if already_in_cart + item_data.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Available: {product.stock}, "
                   f"Already in cart: {already_in_cart}."
        )

    if existing_item:
        existing_item.quantity += item_data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        new_item = CartItem(
            user_id=user_id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item


@router.put("/{user_id}/items/{item_id}", response_model=CartItemResponse, summary="Update cart item quantity")
def update_cart_item(user_id: int, item_id: int, item_data: CartItemUpdate, db: Session = Depends(get_db)):
    """Updates the quantity of an item in the cart."""
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if item_data.quantity <= 0:
        db.delete(item)
        db.commit()
        raise HTTPException(status_code=200, detail="Item removed from cart")

    item.quantity = item_data.quantity
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{user_id}/items/{item_id}", status_code=204, summary="Remove item from cart")
def remove_from_cart(user_id: int, item_id: int, db: Session = Depends(get_db)):
    """Removes the specified item from the cart."""
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
    return None


@router.delete("/{user_id}", status_code=204, summary="Clear entire cart")
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    """Clears all items from the user's cart."""
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    return None
