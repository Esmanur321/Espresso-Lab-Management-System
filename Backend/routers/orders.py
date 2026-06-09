"""
==============================================
routers/orders.py - Order CRUD Endpoints
==============================================

WEEK 8 - Core Business Logic:
- Stock is reduced when an order is placed
- Cannot order from an empty cart
- Stock is restored when an order is cancelled
- Order status flow: pending → confirmed → shipped → delivered

GET    /orders               → List all orders
GET    /orders/{id}          → Get single order
GET    /orders/user/{uid}    → Get user's orders
POST   /orders               → Create new order
PUT    /orders/{id}/status   → Update order status
DELETE /orders/{id}          → Cancel order (stock restored)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Order, OrderItem, Product, User, CartItem
from schemas import OrderCreate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# Valid order status transitions (business rule)
VALID_STATUS_TRANSITIONS = {
    "pending":   ["confirmed", "cancelled"],
    "confirmed": ["shipped", "cancelled"],
    "shipped":   ["delivered"],
    "delivered": [],      # Final state, cannot be changed
    "cancelled": []       # Final state, cannot be changed
}


@router.get("/", response_model=List[OrderResponse], summary="List all orders")
def get_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Returns all orders (for admin use)."""
    return db.query(Order).offset(skip).limit(limit).all()


@router.get("/user/{user_id}", response_model=List[OrderResponse], summary="Get user's orders")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """Returns all orders for a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found (ID: {user_id})")
    return db.query(Order).filter(Order.user_id == user_id).all()


@router.get("/{order_id}", response_model=OrderResponse, summary="Get single order")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Returns a single order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order not found (ID: {order_id})")
    return order


@router.post("/", response_model=OrderResponse, status_code=201, summary="Create new order")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """
    Creates a new order.

    WEEK 8 - BUSINESS RULES:
    1. Cannot place an order with an empty item list
    2. Stock is checked for each product
    3. Stock is reduced upon successful order
    4. Cart is cleared after order is placed
    """
    # 1. Check user exists
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. BUSINESS RULE: Cannot place empty order
    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="An order must contain at least one item"
        )

    # 3. BUSINESS RULE: Check stock for each item
    for item in order_data.items:
        product = db.query(Product).filter(
            Product.id == item.product_id,
            Product.is_active == True
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product not found or inactive (ID: {item.product_id})"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'. "
                       f"Requested: {item.quantity}, Available: {product.stock}"
            )

    # 4. Calculate total (Apply 10% discount)
    raw_total = sum(item.quantity * item.unit_price for item in order_data.items)
    discount = raw_total * 0.10
    total = raw_total - discount

    payment_method = (order_data.payment_method or "online").lower()
    if payment_method not in ("online", "offline"):
        raise HTTPException(
            status_code=400,
            detail="payment_method must be 'online' or 'offline'"
        )

    # Offline orders wait for admin approval; online orders wait for payment gateway
    payment_status = "pending"

    # 5. Create order
    new_order = Order(
        user_id=order_data.user_id,
        total=round(total, 2),
        status="pending",
        payment_method=payment_method,
        payment_status=payment_status,
    )
    db.add(new_order)
    db.flush()

    # 6. Add order items and REDUCE STOCK
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(order_item)

        # Reduce stock (BUSINESS RULE)
        product.stock -= item.quantity

    # 7. Clear the user's cart
    db.query(CartItem).filter(CartItem.user_id == order_data.user_id).delete()

    db.commit()
    db.refresh(new_order)
    return new_order


@router.put("/{order_id}/status", response_model=OrderResponse, summary="Update order status")
def update_order_status(order_id: int, new_status: str, db: Session = Depends(get_db)):
    """
    Updates the order status.

    WEEK 8 - BUSINESS RULE: Status transitions are validated.
    pending → confirmed → shipped → delivered
    Any stage can transition to cancelled.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order not found (ID: {order_id})")

    allowed = VALID_STATUS_TRANSITIONS.get(order.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from '{order.status}' to '{new_status}'. "
                   f"Allowed transitions: {allowed if allowed else 'None (final state)'}"
        )

    # Restore stock if order is cancelled (BUSINESS RULE)
    if new_status == "cancelled":
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock += item.quantity

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=204, summary="Cancel order")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """
    Cancels an order and restores stock.

    WEEK 8 - BUSINESS RULE: Only 'pending' or 'confirmed' orders can be cancelled.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order not found (ID: {order_id})")

    if order.status not in ["pending", "confirmed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel an order with status '{order.status}'"
        )

    # Restore stock
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity

    order.status = "cancelled"
    db.commit()
    return None
