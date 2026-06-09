"""
==============================================
SCHEMAS.PY - Pydantic Data Schemas
==============================================

Pydantic models validate API input and output data.
Similar to interface/type definitions in TypeScript.

Three schemas per model:
- Base:     Shared fields
- Create:   Creation request (POST)
- Response: API response (GET)
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ==================== PRODUCT ====================

class ProductBase(BaseModel):
    name: str
    price: float
    original_price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = 100


class ProductCreate(ProductBase):
    """Schema for POST /products request"""
    pass


class ProductUpdate(BaseModel):
    """Schema for PUT /products/{id} — all fields optional"""
    name: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for GET /products response"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Required to read SQLAlchemy objects


# ==================== USER ====================

class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None


class UserCreate(UserBase):
    """Schema for POST /users request"""
    password: str


class UserUpdate(BaseModel):
    """Schema for PUT /users/{id} request"""
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None


class UserResponse(UserBase):
    """Schema for GET /users response"""
    id: int
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== CART ====================

class CartItemProductInfo(BaseModel):
    """Nested schema for product info inside cart"""
    id: int
    name: str
    price: float
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    """Schema for POST /cart/{user_id}/items request"""
    pass


class CartItemUpdate(BaseModel):
    """Schema for PUT /cart/{user_id}/items/{item_id} request"""
    quantity: int


class CartItemResponse(BaseModel):
    """Schema for GET /cart/{user_id} response"""
    id: int
    product_id: int
    quantity: int
    product: CartItemProductInfo

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Cart summary response"""
    items: List[CartItemResponse]
    total_items: int
    subtotal: float


# ==================== ORDER ====================

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class OrderCreate(BaseModel):
    """Schema for POST /orders request"""
    user_id: int
    items: List[OrderItemCreate]
    payment_method: Optional[str] = "online"  # online | offline


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product: CartItemProductInfo

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Schema for GET /orders response"""
    id: int
    user_id: int
    total: float
    status: str
    payment_method: str = "online"
    payment_status: str = "pending"
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class OfflinePendingOrderResponse(OrderResponse):
    """Offline order with customer info for admin panel."""
    customer_name: str
    customer_email: str


# ==================== COMMENT ====================

class CommentBase(BaseModel):
    rating: int  # 1 to 5
    content: str


class CommentCreate(CommentBase):
    product_id: int
    user_id: int


class CommentResponse(CommentBase):
    id: int
    product_id: int
    user_id: int
    user_name: str
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== FEEDBACK ====================

class FeedbackBase(BaseModel):
    type: str
    message: str


class FeedbackCreate(FeedbackBase):
    user_id: int


class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    user_name: str
    user_email: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
