"""
Test: Product CRUD Endpoints
Validates listing, detail, create, update, soft-delete, and category filtering.
"""
import pytest
from models import Product


# ─────────────────────── READ ───────────────────────

def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_not_found(client):
    response = client.get("/products/9999")
    assert response.status_code == 404


def test_get_product_by_id(client, db_session):
    product = Product(name="Espresso", price=30.0, stock=10, is_active=True)
    db_session.add(product)
    db_session.commit()

    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Espresso"


# ─────────────────────── CREATE ───────────────────────

def test_create_product(client):
    response = client.post("/products/", json={
        "name": "New Blend",
        "price": 45.0,
        "category": "Coffee",
        "stock": 20,
        "description": "A new coffee blend"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Blend"
    assert data["is_active"] is True
    assert "id" in data


# ─────────────────────── UPDATE ───────────────────────

def test_update_product(client, db_session):
    product = Product(name="Old Name", price=10.0, stock=5, is_active=True)
    db_session.add(product)
    db_session.commit()

    response = client.put(f"/products/{product.id}", json={
        "name": "Updated Name",
        "price": 99.0
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["price"] == 99.0


def test_update_product_not_found(client):
    response = client.put("/products/9999", json={"name": "Ghost"})
    assert response.status_code == 404


# ─────────────────────── DELETE (SOFT) ───────────────────────

def test_soft_delete_product(client, db_session):
    product = Product(name="To Delete", price=5.0, stock=1, is_active=True)
    db_session.add(product)
    db_session.commit()

    response = client.delete(f"/products/{product.id}")
    assert response.status_code == 204

    # Verify soft deleted (is_active=False)
    db_session.refresh(product)
    assert product.is_active is False


def test_delete_product_not_found(client):
    response = client.delete("/products/9999")
    assert response.status_code == 404


# ─────────────────────── CATEGORY FILTER ───────────────────────

def test_filter_products_by_category(client, db_session):
    db_session.add(Product(name="Coffee A", price=10.0, category="Coffee", stock=5, is_active=True))
    db_session.add(Product(name="Tea B", price=8.0, category="Tea", stock=5, is_active=True))
    db_session.commit()

    response = client.get("/products/?category=Coffee")
    assert response.status_code == 200
    data = response.json()
    assert all(p["category"] == "Coffee" for p in data)

