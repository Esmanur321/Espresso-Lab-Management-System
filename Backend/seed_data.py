# -*- coding: utf-8 -*-
"""
seed_data.py - Demo Data

This script adds demo products and users since 
the database is empty upon initial setup.

Run: py seed_data.py
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import SessionLocal, engine, Base
from models import Product, User

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Do not add if data already exists
if db.query(Product).count() > 0:
    print("Products already exist in the database, seed skipped.")
    db.close()
    exit()

# ==================== DEMO PRODUCTS ====================
demo_products = [
    Product(
        name="Red Straw Mug Thermos 500 ml",
        price=599.99,
        original_price=750.00,
        image_url="/images/kirmizi-termos.jpg",
        description="Volume: 500 ml | Material: Stainless Steel | Color: Red | Feature: Leakproof Lid",
        category="Thermos",
        stock=50
    ),
    Product(
        name="Practical Filter Coffee - Colombia",
        price=195.00,
        original_price=220.00,
        image_url="/images/filtre-kahve.jpg",
        description="Origin: Colombia | Type: 100% Arabica | Roast: Medium | Notes: Hazelnut, Caramel",
        category="Coffee",
        stock=200
    ),
    Product(
        name="Espresso Blend - Espressolab Signature",
        price=285.00,
        original_price=None,
        image_url="/images/espresso-blend.jpg",
        description="Espressolab's special blend | Intense and balanced flavor | 250g",
        category="Coffee",
        stock=150
    ),
    Product(
        name="Steel Mug 350 ml - Black",
        price=349.00,
        original_price=420.00,
        image_url="/images/siyah-mug.jpg",
        description="Special coating | Thermal insulation | Leakproof lid | 350 ml",
        category="Thermos",
        stock=75
    ),
    Product(
        name="Coffee Grinder - Manual",
        price=899.00,
        original_price=None,
        image_url="/images/kahve-ogutucusu.jpg",
        description="Manual coffee grinder | Adjustable grind | Stainless steel blades",
        category="Accessories",
        stock=30
    ),
    Product(
        name="Earl Grey Tea - Premium",
        price=125.00,
        original_price=150.00,
        image_url="/images/earl-grey.jpg",
        description="Bergamot flavored Earl Grey | 100g | 50 bags",
        category="Teas",
        stock=100
    ),
    Product(
        name="Hazelnut Cookie - Handmade",
        price=85.00,
        original_price=None,
        image_url="/images/findikli-kurabiye.jpg",
        description="Freshly baked daily | 6-pack | Gluten-free",
        category="Snacks",
        stock=40
    ),
    Product(
        name="V60 Dripper Set",
        price=450.00,
        original_price=550.00,
        image_url="/images/v60-dripper.jpg",
        description="Hario V60 | Glass dripper | Filter paper included | For pour-over coffee",
        category="Accessories",
        stock=25
    ),
]

# ==================== DEMO USERS ====================
import bcrypt

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

demo_users = [
    User(
        name="Admin",
        surname="User",
        email="admin@espressolab.com",
        phone="5551112233",
        gender="belirtmem",
        birth_date="1985-01-01",
        password_hash=get_password_hash("Admin123"),
        is_admin=True
    ),
    User(
        name="Standard",
        surname="User",
        email="user@espressolab.com",
        phone="5554445566",
        gender="belirtmem",
        birth_date="1990-01-01",
        password_hash=get_password_hash("Password123"),
        is_admin=False
    ),
    User(
        name="Ahmet",
        surname="Yilmaz",
        email="ahmet@example.com",
        phone="5551234567",
        gender="male",
        birth_date="1990-05-15",
        password_hash=get_password_hash("Password123")
    ),
    User(
        name="Ayse",
        surname="Kaya",
        email="ayse@example.com",
        phone="5559876543",
        gender="female",
        birth_date="1995-08-22",
        password_hash=get_password_hash("Password123")
    ),
]

# Add to database
for product in demo_products:
    db.add(product)

for user in demo_users:
    db.add(user)

db.commit()
db.close()

print("Demo data added successfully!")
print(f"   - {len(demo_products)} products added")
print(f"   - {len(demo_users)} users added")
print("")
print("To start the API: py -m uvicorn main:app --reload")
print("Swagger UI: http://localhost:8000/docs")
