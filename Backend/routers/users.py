"""
==============================================
routers/users.py - User CRUD Endpoints
==============================================

GET    /users                  → List all users
GET    /users/{id}             → Get single user
GET    /users/by-email/{email} → Find user by email
POST   /users                  → Create new user
PUT    /users/{id}             → Update user
DELETE /users/{id}             → Delete user
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import User
from schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[UserResponse], summary="List all users")
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Returns all registered users."""
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserResponse, summary="Get single user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Returns a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found (ID: {user_id})")
    return user


@router.get("/by-email/{email}", response_model=UserResponse, summary="Find user by email")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Finds a user by their email address."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


import bcrypt

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create new user")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user account.

    The email address must be unique.
    """
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user dict without 'password'
    user_dict = user_data.model_dump(exclude={"password"})
    user_dict["password_hash"] = hashed_password

    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserResponse, summary="Update user")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Updates user information."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found (ID: {user_id})")

    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Permanently deletes a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found (ID: {user_id})")

    db.delete(user)
    db.commit()
    return None
