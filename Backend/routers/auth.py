import os
import urllib.parse
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import httpx
from database import get_db
from authlib.integrations.starlette_client import OAuth
from jwt_tokens import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

_google_client_id = os.getenv("GOOGLE_CLIENT_ID", "")
_google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
_frontend_oauth_base = os.getenv("FRONTEND_OAUTH_REDIRECT_BASE", "http://localhost:3000").rstrip("/")

oauth = OAuth()
if _google_client_id and _google_client_secret:
    oauth.register(
        name='google',
        client_id=_google_client_id,
        client_secret=_google_client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
else:
    logger.warning(
        "GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET not set; /auth/google/* will fail until configured."
    )

class OAuth2Request(BaseModel):
    provider: str  # e.g. "google" or "facebook"
    access_token: str

class StandardLoginRequest(BaseModel):
    email: str
    password: str

from routers.users import verify_password
from models import User

@router.post("/login", summary="Standard Login (Email & Password)")
def login(request: StandardLoginRequest, db: Session = Depends(get_db)):
    """
    Standard Email & Password login endpoint.
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz e-posta veya şifre")

    if not user.password_hash or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz e-posta veya şifre")

    logger.info(f"User {user.email} logged in successfully.")

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        name=user.name,
        surname=user.surname or "",
        phone=user.phone or "",
        is_admin=bool(user.is_admin),
    )

    return {
        "status": "success",
        "message": "Giriş başarılı",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "phone": user.phone,
            "is_admin": user.is_admin or False
        },
        "token": access_token
    }

@router.post("/social-login", summary="Social Media Login (OAuth2)")
def social_login(request: OAuth2Request, db: Session = Depends(get_db)):
    """
    Mock endpoint for Social Media login.
    Creates or fetches user in DB so orders can link to a real user_id.
    """
    if request.provider not in ["google", "facebook"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported provider")
    
    if not request.access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing access token")

    # The frontend passes the mock email as access_token for simulation
    email = request.access_token if "@" in request.access_token else f"mockuser@{request.provider}.com"

    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Create a new user in DB
        user = User(
            name=f"{request.provider.capitalize()} User",
            surname="",
            email=email,
            phone="",
            gender="belirtmem",
            password_hash="" # No password since social login
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    logger.info(f"User logged in via {request.provider} with email {email}")

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        name=user.name,
        surname=user.surname or "",
        phone=user.phone or "",
        is_admin=bool(user.is_admin),
    )

    return {
        "status": "success",
        "message": f"Successfully authenticated with {request.provider}",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "phone": user.phone,
            "is_admin": user.is_admin or False
        },
        "token": access_token
    }

@router.get("/google/login", summary="Google Login Redirect")
async def google_login(request: Request):
    """
    Redirect the user to Google OAuth2 authorization screen.
    """
    if not _google_client_id or not _google_client_secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured (missing GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET).",
        )
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

async def _google_user_profile(google_token: dict) -> dict | None:
    """
    Authlib sometimes omits `userinfo` on the token dict for Google.
    Fall back to Google's userinfo endpoint using the access_token.
    """
    user_info = google_token.get("userinfo")
    if isinstance(user_info, dict) and user_info.get("email"):
        return user_info

    access_token = google_token.get("access_token")
    if not access_token:
        logger.error("Google token has no userinfo and no access_token")
        return None

    try:
        async with httpx.AsyncClient() as http:
            response = await http.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=15.0,
            )
        if response.status_code != 200:
            logger.error(
                "Google userinfo request failed: %s %s",
                response.status_code,
                response.text[:500],
            )
            return None
        data = response.json()
        if not isinstance(data, dict) or not data.get("email"):
            logger.error("Google userinfo response missing email: %r", data)
            return None
        return data
    except Exception as e:
        logger.error("Failed to fetch Google userinfo: %s", e)
        return None


@router.get("/google/callback", summary="Google Auth Callback", name="auth_google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle Google OAuth2 redirect callback.
    Verify the auth state, fetch user info, log them in, and redirect back to the Frontend.
    """
    if not _google_client_id or not _google_client_secret:
        return RedirectResponse(url=f"{_frontend_oauth_base}/login?auth_error=oauth_not_configured")

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        logger.error(f"Failed to authorize Google access token: {e}")
        return RedirectResponse(url=f"{_frontend_oauth_base}/login?auth_error=google_auth_failed")

    user_info = await _google_user_profile(token)
    if not user_info:
        return RedirectResponse(url=f"{_frontend_oauth_base}/login?auth_error=no_user_info")

    email = user_info.get('email')
    name = user_info.get('given_name') or user_info.get('name') or "Google"
    surname = user_info.get('family_name') or ""

    if not email:
        logger.error("Google userinfo does not contain email")
        return RedirectResponse(url=f"{_frontend_oauth_base}/login?auth_error=email_required")

    # Fetch or create the user in database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            name=name,
            surname=surname,
            email=email,
            phone="",
            gender="belirtmem",
            password_hash="",
            is_admin=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    logger.info(f"User {email} successfully authenticated via Google OAuth2")

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        name=user.name,
        surname=user.surname or "",
        phone=user.phone or "",
        is_admin=bool(user.is_admin),
    )

    params = {"auth_success": "true", "token": access_token}
    query_string = urllib.parse.urlencode(params)
    redirect_url = f"{_frontend_oauth_base}/login?{query_string}"
    return RedirectResponse(url=redirect_url)
