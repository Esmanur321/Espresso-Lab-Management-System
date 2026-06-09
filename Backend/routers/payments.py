from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import List, Literal
import stripe
from queue_service import queue_service
from database import get_db
from models import Order, User, Product, OrderItem
from schemas import OfflinePendingOrderResponse, OrderResponse

import os

router = APIRouter(prefix="/payments", tags=["Payments"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaymentRequest(BaseModel):
    order_id: int
    amount: int  # in cents
    currency: str = "try"
    source: str  # Stripe token or source from frontend


class OfflinePaymentApproval(BaseModel):
    order_id: int
    admin_id: int
    approved: bool


class OfflinePaymentStatusUpdate(BaseModel):
    admin_id: int
    payment_status: Literal["approved", "rejected"]


def _require_admin(admin_id: int, db: Session) -> User:
    admin_user = db.query(User).filter(User.id == admin_id).first()
    if not admin_user or not admin_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return admin_user


def _restore_order_stock(order: Order, db: Session) -> None:
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity


def _apply_offline_decision(order: Order, approved: bool, db: Session) -> str:
    if order.payment_method != "offline":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is not an offline payment order",
        )
    if order.payment_status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Offline payment already reviewed (status: {order.payment_status})",
        )

    if approved:
        order.payment_status = "approved"
        order.status = "confirmed"
        result_status = "approved"
    else:
        order.payment_status = "rejected"
        order.status = "cancelled"
        _restore_order_stock(order, db)
        result_status = "rejected"

    db.commit()
    return result_status


@router.post("/online", summary="Process Electronic Payment (Online)")
def process_online_payment(request: PaymentRequest, db: Session = Depends(get_db)):
    """
    Process an online payment using the Stripe API (Sandbox).
    This endpoint ONLY publishes the outcome to RabbitMQ for asynchronous DB update.
    """
    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.payment_method == "offline":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This order uses offline payment; use bank transfer instead",
        )

    # Note: We do NOT commit order.payment_method = "online" here anymore,
    # the worker will update it asynchronously or we can do it when creating order.
    try:
        # Log the payment request details for debugging
        print(f"[STRIPE DEBUG] Processing payment - Order ID: {request.order_id}, Amount: {request.amount}, Currency: {request.currency}, Source: {request.source[:20]}...")
        
        intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency=request.currency,
            payment_method=request.source,
            confirm=True,
            return_url="http://localhost:3000/profile",
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": "never"
            }
        )
        
        print(f"[STRIPE DEBUG] Payment successful - Intent ID: {intent.id}")

        # DO NOT update database status here.
        # Instead, delegate to RabbitMQ.
        queue_service.publish_message({
            "event": "payment_processed",
            "order_id": request.order_id,
            "status": "success",
            "type": "online",
            "charge_id": intent.id,
        })

        return {"status": "success", "message": "Payment details submitted for background processing"}

    except stripe.error.CardError as e:
        # Log detailed Stripe error information
        print(f"[STRIPE ERROR] CardError occurred: {str(e)}")
        
        # DO NOT update database status here.
        # Publish payment failure event so background worker handles cancellations and stock restoration.
        queue_service.publish_message({
            "event": "payment_failed",
            "order_id": request.order_id,
            "status": "failed",
            "error": str(e),
        })

        error_message = e.user_message if hasattr(e, 'user_message') and e.user_message else str(e)
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=error_message)

    except (stripe.error.APIError, stripe.error.StripeError, Exception) as e:
        print(f"[STRIPE ERROR] Error occurred: {str(e)}")
        
        # Publish error/failure event
        queue_service.publish_message({
            "event": "payment_failed",
            "order_id": request.order_id,
            "status": "failed",
            "error": str(e),
        })

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment processing error",
        )


@router.post("/offline", summary="Register Offline Payment (Customer)")
def register_offline_payment(order_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Confirms an offline (bank transfer / EFT) order is awaiting admin approval.
    Order must already exist with payment_method=offline and payment_status=pending.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.payment_method != "offline":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is not configured for offline payment",
        )

    if order.payment_status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Offline payment is already {order.payment_status}",
        )

    queue_service.publish_message({
        "event": "offline_payment_pending",
        "order_id": order.id,
        "user_id": order.user_id,
        "amount": order.total,
    })

    return {
        "status": "success",
        "message": "Offline payment registered; awaiting admin approval",
        "order_id": order.id,
        "payment_status": order.payment_status,
    }


@router.get(
    "/offline/pending",
    response_model=List[OfflinePendingOrderResponse],
    summary="List Pending Offline Payments (Admin)",
)
def list_pending_offline_orders(admin_id: int, db: Session = Depends(get_db)):
    """Returns all offline orders with payment_status=pending for admin review."""
    _require_admin(admin_id, db)

    orders = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .filter(Order.payment_method == "offline", Order.payment_status == "pending")
        .order_by(Order.created_at.desc())
        .all()
    )

    result = []
    for order in orders:
        user = db.query(User).filter(User.id == order.user_id).first()
        base = OrderResponse.model_validate(order).model_dump()
        base["customer_name"] = f"{user.name} {user.surname}".strip() if user else "Unknown"
        base["customer_email"] = user.email if user else ""
        result.append(OfflinePendingOrderResponse(**base))

    return result


@router.patch(
    "/offline/{order_id}",
    summary="Approve or Reject Offline Payment (Admin)",
)
def update_offline_payment_status(
    order_id: int,
    body: OfflinePaymentStatusUpdate,
    db: Session = Depends(get_db),
):
    """Admin approves or rejects a pending offline payment."""
    _require_admin(body.admin_id, db)

    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    approved = body.payment_status == "approved"
    result_status = _apply_offline_decision(order, approved, db)

    queue_service.publish_message({
        "event": "offline_payment_reviewed",
        "order_id": order_id,
        "payment_status": result_status,
        "order_status": order.status,
        "admin_id": body.admin_id,
    })

    return {
        "status": "success",
        "message": f"Order {order_id} payment {result_status}",
        "payment_status": order.payment_status,
        "order_status": order.status,
    }


@router.post("/offline/approve", summary="Approve Offline Payment (Admin, legacy)")
def approve_offline_payment(request: OfflinePaymentApproval, db: Session = Depends(get_db)):
    """Backward-compatible endpoint; prefer PATCH /payments/offline/{order_id}."""
    _require_admin(request.admin_id, db)

    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == request.order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    result_status = _apply_offline_decision(order, request.approved, db)

    queue_service.publish_message({
        "event": "offline_payment_reviewed",
        "order_id": request.order_id,
        "payment_status": result_status,
        "order_status": order.status,
        "admin_id": request.admin_id,
    })

    status_str = "confirmed" if request.approved else "cancelled"
    return {
        "status": "success",
        "message": f"Order {request.order_id} status updated to {status_str}.",
        "payment_status": order.payment_status,
    }
