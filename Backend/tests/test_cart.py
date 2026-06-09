"""
Test: Cart CRUD Endpoints
Validates cart add, update, remove, clear, and stock-check business logic.
"""
import pytest
from models import Product, User, CartItem


def _seed_user_and_product(db_session, email="cart@example.com", stock=50):
    """Helper: create a user and a product for cart tests."""
    user = User(name="Cart", surname="Tester", email=email, password_hash="x")
    product = Product(name="Test Coffee", price=25.0, stock=stock, is_active=True)
    db_session.add(user)
    db_session.add(product)
    db_session.commit()
    return user, product


# ─────────────────────── GET ───────────────────────

def test_get_cart_empty(client, db_session):
    """An empty cart should return zero items and 0.0 subtotal."""
    user, _ = _seed_user_and_product(db_session)
    response = client.get(f"/cart/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 0
    assert data["subtotal"] == 0.0
    assert data["items"] == []


def test_get_cart_user_not_found(client):
    """Requesting a cart for a non-existent user returns 404."""
    response = client.get("/cart/9999")
    assert response.status_code == 404


# ─────────────────────── ADD ITEM ───────────────────────

def test_add_item_to_cart(client, db_session):
    """Adding a valid product creates a cart item."""
    user, product = _seed_user_and_product(db_session, email="add@example.com")
    response = client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id,
        "quantity": 2
    })
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == product.id
    assert data["quantity"] == 2


def test_add_item_merges_quantity(client, db_session):
    """Adding the same product again should merge quantities."""
    user, product = _seed_user_and_product(db_session, email="merge@example.com")
    client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id, "quantity": 1
    })
    response = client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id, "quantity": 3
    })
    assert response.status_code == 201
    assert response.json()["quantity"] == 4  # 1 + 3


def test_add_item_insufficient_stock(client, db_session):
    """Adding more than available stock returns 400."""
    user, product = _seed_user_and_product(
        db_session, email="nostock@example.com", stock=2
    )
    response = client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id,
        "quantity": 5
    })
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


def test_add_item_product_not_found(client, db_session):
    """Adding a non-existent product returns 404."""
    user, _ = _seed_user_and_product(db_session, email="noprod@example.com")
    response = client.post(f"/cart/{user.id}/items", json={
        "product_id": 9999,
        "quantity": 1
    })
    assert response.status_code == 404


def test_add_item_user_not_found(client):
    """Adding to a non-existent user's cart returns 404."""
    response = client.post("/cart/9999/items", json={
        "product_id": 1,
        "quantity": 1
    })
    assert response.status_code == 404


# ─────────────────────── UPDATE ───────────────────────

def test_update_cart_item_quantity(client, db_session):
    """Updating quantity of an existing cart item works."""
    user, product = _seed_user_and_product(db_session, email="update@example.com")
    add_res = client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id, "quantity": 1
    })
    item_id = add_res.json()["id"]

    response = client.put(f"/cart/{user.id}/items/{item_id}", json={
        "quantity": 5
    })
    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_update_cart_item_not_found(client, db_session):
    """Updating a non-existent cart item returns 404."""
    user, _ = _seed_user_and_product(db_session, email="upd404@example.com")
    response = client.put(f"/cart/{user.id}/items/9999", json={
        "quantity": 2
    })
    assert response.status_code == 404


# ─────────────────────── DELETE ───────────────────────

def test_remove_cart_item(client, db_session):
    """Removing a specific item from the cart returns 204."""
    user, product = _seed_user_and_product(db_session, email="remove@example.com")
    add_res = client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id, "quantity": 1
    })
    item_id = add_res.json()["id"]

    response = client.delete(f"/cart/{user.id}/items/{item_id}")
    assert response.status_code == 204

    # Verify cart is now empty
    cart = client.get(f"/cart/{user.id}")
    assert cart.json()["total_items"] == 0


def test_remove_cart_item_not_found(client, db_session):
    """Removing a non-existent item returns 404."""
    user, _ = _seed_user_and_product(db_session, email="rm404@example.com")
    response = client.delete(f"/cart/{user.id}/items/9999")
    assert response.status_code == 404


def test_clear_cart(client, db_session):
    """Clearing the entire cart removes all items."""
    user, product = _seed_user_and_product(db_session, email="clear@example.com")
    client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id, "quantity": 3
    })

    response = client.delete(f"/cart/{user.id}")
    assert response.status_code == 204

    # Verify empty
    cart = client.get(f"/cart/{user.id}")
    assert cart.json()["total_items"] == 0


# ─────────────────────── GET WITH ITEMS ───────────────────────

def test_get_cart_with_items(client, db_session):
    """After adding items, GET cart returns correct totals."""
    user, product = _seed_user_and_product(db_session, email="full@example.com")
    client.post(f"/cart/{user.id}/items", json={
        "product_id": product.id, "quantity": 4
    })

    response = client.get(f"/cart/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 4
    assert data["subtotal"] == 100.0  # 4 * 25.0
    assert len(data["items"]) == 1
