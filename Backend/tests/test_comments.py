import pytest
from models import Product, User, Comment


def test_create_comment_success(client, db_session):
    # Create product and user
    product = Product(name="Mocha", price=35.0, stock=10, is_active=True)
    user = User(name="John", surname="Doe", email="john@example.com", is_admin=False)
    db_session.add(product)
    db_session.add(user)
    db_session.commit()

    response = client.post("/comments/", json={
        "product_id": product.id,
        "user_id": user.id,
        "rating": 5,
        "content": "Excellent coffee!"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 5
    assert data["content"] == "Excellent coffee!"
    assert data["is_approved"] is False


def test_create_comment_invalid_rating(client, db_session):
    product = Product(name="Mocha", price=35.0, stock=10, is_active=True)
    user = User(name="John", surname="Doe", email="john@example.com", is_admin=False)
    db_session.add(product)
    db_session.add(user)
    db_session.commit()

    response = client.post("/comments/", json={
        "product_id": product.id,
        "user_id": user.id,
        "rating": 6,  # Invalid
        "content": "Too good!"
    })
    assert response.status_code == 400


def test_get_product_comments_filtering(client, db_session):
    product = Product(name="Mocha", price=35.0, stock=10, is_active=True)
    user = User(name="John", surname="Doe", email="john@example.com", is_admin=False)
    db_session.add(product)
    db_session.add(user)
    db_session.commit()

    # Create approved comment
    c1 = Comment(product_id=product.id, user_id=user.id, rating=4, content="Approved Review", is_approved=True)
    # Create pending comment
    c2 = Comment(product_id=product.id, user_id=user.id, rating=2, content="Pending Review", is_approved=False)
    db_session.add(c1)
    db_session.add(c2)
    db_session.commit()

    response = client.get(f"/comments/product/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["content"] == "Approved Review"


def test_admin_endpoints_authorization(client, db_session):
    product = Product(name="Mocha", price=35.0, stock=10, is_active=True)
    user = User(name="John", surname="Doe", email="john@example.com", is_admin=False)
    admin = User(name="Admin", surname="User", email="admin@example.com", is_admin=True)
    db_session.add(product)
    db_session.add(user)
    db_session.add(admin)
    db_session.commit()

    comment = Comment(product_id=product.id, user_id=user.id, rating=3, content="Review", is_approved=False)
    db_session.add(comment)
    db_session.commit()

    # Unauthorized access to get pending
    response = client.get(f"/comments/pending?admin_id={user.id}")
    assert response.status_code == 403

    # Authorized access to get pending
    response = client.get(f"/comments/pending?admin_id={admin.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Unauthorized access to approve
    response = client.patch(f"/comments/{comment.id}/approve?admin_id={user.id}")
    assert response.status_code == 403

    # Authorized access to approve
    response = client.patch(f"/comments/{comment.id}/approve?admin_id={admin.id}")
    assert response.status_code == 200
    assert response.json()["is_approved"] is True

    # Reject / delete comment
    response = client.delete(f"/comments/{comment.id}?admin_id={admin.id}")
    assert response.status_code == 204
