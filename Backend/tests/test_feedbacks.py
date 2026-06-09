import pytest
from models import User, Feedback


def test_create_feedback_success(client, db_session):
    # Create user
    user = User(name="Jane", surname="Doe", email="jane@example.com", is_admin=False)
    db_session.add(user)
    db_session.commit()

    response = client.post("/feedbacks/", json={
        "user_id": user.id,
        "type": "sikayet",
        "message": "The coffee was cold."
    })

    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "sikayet"
    assert data["message"] == "The coffee was cold."
    assert data["is_read"] is False
    assert data["user_name"] == "Jane Doe"
    assert data["user_email"] == "jane@example.com"


def test_create_feedback_user_not_found(client):
    response = client.post("/feedbacks/", json={
        "user_id": 9999,  # Non-existent user
        "type": "oneri",
        "message": "Add more cake varieties."
    })
    assert response.status_code == 404


def test_admin_feedback_endpoints_authorization(client, db_session):
    user = User(name="Jane", surname="Doe", email="jane@example.com", is_admin=False)
    admin = User(name="Admin", surname="User", email="admin@example.com", is_admin=True)
    db_session.add(user)
    db_session.add(admin)
    db_session.commit()

    fb = Feedback(user_id=user.id, type="oneri", message="Good job", is_read=False)
    db_session.add(fb)
    db_session.commit()

    # Unauthorized access to get feedbacks
    response = client.get(f"/feedbacks/?admin_id={user.id}")
    assert response.status_code == 403

    # Authorized access to get feedbacks
    response = client.get(f"/feedbacks/?admin_id={admin.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["message"] == "Good job"

    # Unauthorized access to mark as read
    response = client.patch(f"/feedbacks/{fb.id}/read?admin_id={user.id}")
    assert response.status_code == 403

    # Authorized access to mark as read
    response = client.patch(f"/feedbacks/{fb.id}/read?admin_id={admin.id}")
    assert response.status_code == 200
    assert response.json()["is_read"] is True
