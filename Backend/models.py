"""
==============================================
MODELS.PY - Database Tables
==============================================

SQLAlchemy ORM models.
Each class corresponds to a database table.

Tables:
- Product   → products table
- User      → users table
- CartItem  → cart_items table
- Order     → orders table
- OrderItem → order_items table
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Product(Base):
    """products table — Product information"""
    __tablename__ = "products"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(255), nullable=False)
    price          = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)   # Original price for discounted products
    image_url      = Column(String(500), nullable=True)
    description    = Column(Text, nullable=True)
    category       = Column(String(100), nullable=True)
    stock          = Column(Integer, default=100)
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    cart_items  = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    comments    = relationship("Comment", back_populates="product", cascade="all, delete-orphan")


class User(Base):
    """users table — User information"""
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    surname    = Column(String(100), nullable=False)
    email      = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True) # EKLENDİ
    phone      = Column(String(20), nullable=True)
    gender     = Column(String(20), nullable=True)
    birth_date = Column(String(20), nullable=True)
    is_admin   = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    cart_items = relationship("CartItem", back_populates="user")
    orders     = relationship("Order", back_populates="user")
    comments   = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    feedbacks  = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")


class CartItem(Base):
    """
    cart_items table — Cart contents.
    Each row represents: which user's cart, which product, and quantity.
    """
    __tablename__ = "cart_items"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, default=1, nullable=False)
    added_at   = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user    = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Order(Base):
    """orders table — Order headers"""
    __tablename__ = "orders"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    total           = Column(Float, nullable=False)
    status          = Column(String(50), default="pending")   # pending, confirmed, shipped, delivered, cancelled
    payment_method  = Column(String(20), default="online")    # online, offline
    payment_status  = Column(String(20), default="pending")   # pending, approved, rejected
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user  = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """
    order_items table — Order line items.
    Stores which product, quantity, and unit price at the time of order.
    """
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Price stored at order time

    # Relationships
    order   = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Comment(Base):
    """comments table — User reviews and ratings on products"""
    __tablename__ = "comments"

    id          = Column(Integer, primary_key=True, index=True)
    product_id  = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating      = Column(Integer, nullable=False)
    content     = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    product     = relationship("Product", back_populates="comments")
    user        = relationship("User", back_populates="comments")

    @property
    def user_name(self) -> str:
        return f"{self.user.name} {self.user.surname}" if self.user else "Anonymous"


class Feedback(Base):
    """feedbacks table — User feedback and suggestions"""
    __tablename__ = "feedbacks"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    type       = Column(String(50), nullable=False)
    message    = Column(Text, nullable=False)
    is_read    = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user       = relationship("User", back_populates="feedbacks")

    @property
    def user_name(self) -> str:
        return f"{self.user.name} {self.user.surname}" if self.user else "Anonymous"

    @property
    def user_email(self) -> str:
        return self.user.email if self.user else ""
