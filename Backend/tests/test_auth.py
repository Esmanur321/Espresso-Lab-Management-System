from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.responses import RedirectResponse


def test_standard_login(client):
    # Register first
    client.post("/users/", json={
        "name": "Auth",
        "surname": "User",
        "email": "auth@example.com",
        "phone": "123",
        "gender": "male",
        "password": "AuthPassword123"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "auth@example.com",
        "password": "AuthPassword123"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "token" in response.json()

def test_login_invalid_password(client):
    response = client.post("/auth/login", json={
        "email": "auth@example.com",
        "password": "WrongPassword"
    })
    assert response.status_code == 401

def test_social_login_new_user(client):
    response = client.post("/auth/social-login", json={
        "provider": "google",
        "access_token": "googleuser@gmail.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "googleuser@gmail.com"
    assert "token" in data

def test_social_login_existing_user(client):
    # Mock creating it first via standard or social
    client.post("/auth/social-login", json={
        "provider": "google",
        "access_token": "googleuser2@gmail.com"
    })
    # Login again
    response = client.post("/auth/social-login", json={
        "provider": "google",
        "access_token": "googleuser2@gmail.com"
    })
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "googleuser2@gmail.com"


def test_google_login_redirect(client):
    with patch("routers.auth.oauth.google.authorize_redirect") as mock_redirect:
        mock_redirect.return_value = RedirectResponse(url="https://accounts.google.com/o/oauth2/v2/auth")
        response = client.get("/auth/google/login", follow_redirects=False)
        assert response.status_code in [302, 307]
        assert response.headers["location"] == "https://accounts.google.com/o/oauth2/v2/auth"

def test_google_callback_success(client):
    mock_token = {
        "userinfo": {
            "email": "test-google-user@gmail.com",
            "given_name": "GoogleTest",
            "family_name": "User"
        }
    }
    with patch("routers.auth.oauth.google.authorize_access_token") as mock_access_token:
        mock_access_token.return_value = mock_token
        response = client.get("/auth/google/callback", follow_redirects=False)
        assert response.status_code in [302, 307]
        location = response.headers["location"]
        assert "auth_success=true" in location
        assert "token=" in location
        assert "email=" not in location  # session carried in JWT only

def test_google_callback_failure(client):
    with patch("routers.auth.oauth.google.authorize_access_token", side_effect=Exception("OAuth Error")):
        response = client.get("/auth/google/callback", follow_redirects=False)
        assert response.status_code in [302, 307]
        assert "auth_error=google_auth_failed" in response.headers["location"]


def test_google_callback_userinfo_http_fallback(client):
    """When Authlib omits userinfo, profile is loaded via Google's userinfo endpoint."""
    mock_token = {"access_token": "fake-google-access-token"}

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "email": "http-fallback@gmail.com",
        "given_name": "Api",
        "family_name": "Test",
    }

    class FakeHttp:
        async def get(self, url, headers=None, timeout=None):
            return mock_resp

    class FakeAsyncClient:
        async def __aenter__(self):
            return FakeHttp()

        async def __aexit__(self, exc_type, exc, tb):
            return False

    with patch("routers.auth.oauth.google.authorize_access_token", new_callable=AsyncMock) as m_tok:
        m_tok.return_value = mock_token
        with patch("routers.auth.httpx.AsyncClient", return_value=FakeAsyncClient()):
            response = client.get("/auth/google/callback", follow_redirects=False)
    assert response.status_code in [302, 307]
    loc = response.headers["location"]
    assert "auth_success=true" in loc
    assert "token=" in loc

