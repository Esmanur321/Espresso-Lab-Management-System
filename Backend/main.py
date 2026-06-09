"""
==============================================
MAIN.PY - FastAPI Application Entry Point
==============================================

Espressolab Backend API
- FastAPI framework
- SQLite database
- CORS middleware (for frontend connection)
- Auto Swagger UI: http://localhost:8000/docs
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Trigger reload to pick up new redirect URI in .env
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from database import engine, Base


def run_migrations():
    """Add new columns to existing SQLite databases without dropping data."""
    from sqlalchemy import inspect, text

    inspector = inspect(engine)
    if "orders" not in inspector.get_table_names():
        return

    existing = {col["name"] for col in inspector.get_columns("orders")}
    statements = []
    if "payment_method" not in existing:
        statements.append(
            "ALTER TABLE orders ADD COLUMN payment_method VARCHAR(20) DEFAULT 'online'"
        )
    if "payment_status" not in existing:
        statements.append(
            "ALTER TABLE orders ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending'"
        )

    if not statements:
        return

    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
        conn.execute(text(
            "UPDATE orders SET payment_method = 'online' WHERE payment_method IS NULL"
        ))
        conn.execute(text(
            "UPDATE orders SET payment_status = 'pending' WHERE payment_status IS NULL"
        ))
from routers import products, users, cart, orders, auth, payments, comments, feedbacks

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)
run_migrations()

# FastAPI application
app = FastAPI(
    title="Espressolab Backend API",
    description="""
## Espressolab E-Commerce Platform Backend API

This API manages all backend operations for the Espressolab online store.

### Features:
- 🛍️ **Product** management (CRUD)
- 👤 **User** management (CRUD)
- 🛒 **Cart** management (CRUD)
- 📦 **Order** management (CRUD + Business Logic)
- 🔐 **Auth** (Social Login)
- 💳 **Payments** (Online / Offline + RabbitMQ integration)

### Tech Stack:
- **FastAPI** — Modern Python REST API framework
- **SQLAlchemy** — ORM (Object Relational Mapper)
- **SQLite** — Database
- **Pydantic** — Data validation
    """,
    version="1.0.0",
    contact={
        "name": "Espressolab Dev Team",
        "email": "dev@espressolab.com"
    }
)

# ==================== SESSION MIDDLEWARE ====================
# Required for Google OAuth2 state checking
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("OAUTH_SECRET_KEY", "espressolab-super-secret-oauth-key-998877")
)

# ==================== CORS MIDDLEWARE ====================
# Required for Frontend (localhost:3000) → Backend (localhost:8000) communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ROUTER REGISTRATION ====================
app.include_router(products.router)
app.include_router(users.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(payments.router)
app.include_router(comments.router)
app.include_router(feedbacks.router)


# ==================== ROOT ENDPOINTS ====================
@app.get("/", tags=["Health"], summary="API Status")
def root():
    """Check if the API is running."""
    return {
        "status": "Espressolab Backend API is running",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs",
        "endpoints": {
            "products": "http://localhost:8000/products",
            "users":    "http://localhost:8000/users",
            "cart":     "http://localhost:8000/cart",
            "orders":   "http://localhost:8000/orders"
        }
    }


@app.get("/health", tags=["Health"], summary="Health Check")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "espressolab-backend"}
