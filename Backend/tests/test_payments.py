import pytest
from models import Order, User, Product


def test_online_payment_success(client, db_session):
    user = User(name="Pay", surname="Test", email="pay@example.com")
    db_session.add(user)
    db_session.commit()

    order = Order(
        user_id=user.id,
        total=100.0,
        status="pending",
        payment_method="online",
        payment_status="pending",
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    response = client.post("/payments/online", json={
        "order_id": order.id,
        "amount": 10000,
        "currency": "try",
        "source": "pm_card_visa",
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    db_session.refresh(order)
    assert order.status == "confirmed"
    assert order.payment_status == "approved"


def test_online_payment_failure(client, db_session):
    user = User(name="Fail", surname="User", email="fail@example.com")
    product = Product(name="Mug", price=50.0, stock=10, is_active=True)
    db_session.add_all([user, product])
    db_session.commit()

    order = Order(
        user_id=user.id,
        total=50.0,
        status="pending",
        payment_method="online",
        payment_status="pending",
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    response = client.post("/payments/online", json={
        "order_id": order.id,
        "amount": 5000,
        "currency": "try",
        "source": "pm_card_chargeDeclined",
    })

    assert response.status_code == 402

    db_session.refresh(order)
    assert order.status == "cancelled"
    assert order.payment_status == "rejected"


def test_create_offline_order(client, db_session):
    user = User(name="Offline", surname="Buyer", email="offline@example.com")
    product = Product(name="Tea", price=25.0, stock=5, is_active=True)
    db_session.add_all([user, product])
    db_session.commit()

    response = client.post("/orders/", json={
        "user_id": user.id,
        "payment_method": "offline",
        "items": [
            {"product_id": product.id, "quantity": 1, "unit_price": 25.0},
        ],
    })

    assert response.status_code == 201
    data = response.json()
    assert data["payment_method"] == "offline"
    assert data["payment_status"] == "pending"
    assert data["status"] == "pending"


def test_register_offline_payment(client, db_session):
    user = User(name="Offline", surname="Buyer", email="offline2@example.com")
    db_session.add(user)
    db_session.commit()

    order = Order(
        user_id=user.id,
        total=120.0,
        status="pending",
        payment_method="offline",
        payment_status="pending",
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    response = client.post(f"/payments/offline?order_id={order.id}")
    assert response.status_code == 200
    assert response.json()["payment_status"] == "pending"


def test_list_pending_offline_orders(client, db_session):
    admin = User(name="Admin", surname="User", email="admin-pending@example.com", is_admin=True)
    customer = User(name="Cust", surname="User", email="cust@example.com")
    db_session.add_all([admin, customer])
    db_session.commit()

    pending = Order(
        user_id=customer.id,
        total=200.0,
        status="pending",
        payment_method="offline",
        payment_status="pending",
    )
    online = Order(
        user_id=customer.id,
        total=50.0,
        status="pending",
        payment_method="online",
        payment_status="pending",
    )
    db_session.add_all([pending, online])
    db_session.commit()

    response = client.get(f"/payments/offline/pending?admin_id={admin.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["payment_method"] == "offline"
    assert data[0]["customer_email"] == "cust@example.com"


def test_patch_offline_payment_approve(client, db_session):
    admin = User(name="Admin", surname="User", email="admin-patch@example.com", is_admin=True)
    customer = User(name="Cust", surname="User", email="cust2@example.com")
    product = Product(name="Coffee", price=30.0, stock=10, is_active=True)
    db_session.add_all([admin, customer, product])
    db_session.commit()

    order = Order(
        user_id=customer.id,
        total=60.0,
        status="pending",
        payment_method="offline",
        payment_status="pending",
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    response = client.patch(f"/payments/offline/{order.id}", json={
        "admin_id": admin.id,
        "payment_status": "approved",
    })

    assert response.status_code == 200
    db_session.refresh(order)
    assert order.payment_status == "approved"
    assert order.status == "confirmed"


def test_offline_payment_approve_legacy(client, db_session):
    admin = User(name="Admin", surname="User", email="admin-test@example.com", is_admin=True)
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)

    order = Order(
        user_id=admin.id,
        total=200.0,
        status="pending",
        payment_method="offline",
        payment_status="pending",
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    response = client.post("/payments/offline/approve", json={
        "order_id": order.id,
        "admin_id": admin.id,
        "approved": True,
    })

    assert response.status_code == 200
    db_session.refresh(order)
    assert order.status == "confirmed"
    assert order.payment_status == "approved"
