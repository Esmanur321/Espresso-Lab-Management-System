import pytest
from models import Product, User
from database import get_db

def test_create_order_empty_cart(client):
    response = client.post("/orders/", json={
        "user_id": 1,
        "items": []
    })
    # Since we validate user first
    assert response.status_code == 404 # User not found

def test_create_order_success(client, db_session):
    # Setup Data
    user = User(name="Order", surname="Test", email="order@example.com", password_hash="123")
    product = Product(name="Coffee", price=10.0, stock=5, is_active=True)
    db_session.add(user)
    db_session.add(product)
    db_session.commit()
    
    response = client.post("/orders/", json={
        "user_id": user.id,
        "items": [
            {"product_id": product.id, "quantity": 2, "unit_price": 10.0}
        ]
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["total"] == 18.0
    assert data["status"] == "pending"
    
    # Verify stock reduced
    db_session.refresh(product)
    assert product.stock == 3

def test_create_order_insufficient_stock(client, db_session):
    user = User(name="Order", surname="Test", email="order2@example.com", password_hash="123")
    product = Product(name="Tea", price=5.0, stock=1, is_active=True)
    db_session.add(user)
    db_session.add(product)
    db_session.commit()
    
    response = client.post("/orders/", json={
        "user_id": user.id,
        "items": [
            {"product_id": product.id, "quantity": 5, "unit_price": 5.0}
        ]
    })
    
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]

def test_cancel_order_restores_stock(client, db_session):
    user = User(name="Order", surname="Test", email="order3@example.com", password_hash="123")
    product = Product(name="Mug", price=15.0, stock=10, is_active=True)
    db_session.add(user)
    db_session.add(product)
    db_session.commit()
    
    # Create order
    res = client.post("/orders/", json={
        "user_id": user.id,
        "items": [
            {"product_id": product.id, "quantity": 2, "unit_price": 15.0}
        ]
    })
    order_id = res.json()["id"]
    
    # Cancel order
    cancel_res = client.delete(f"/orders/{order_id}")
    assert cancel_res.status_code == 204
    
    # Verify stock restored
    db_session.refresh(product)
    assert product.stock == 10
