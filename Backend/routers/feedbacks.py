from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Feedback, User
from schemas import FeedbackCreate, FeedbackResponse

router = APIRouter(
    prefix="/feedbacks",
    tags=["Feedbacks"]
)


def _require_admin(admin_id: int, db: Session) -> User:
    admin_user = db.query(User).filter(User.id == admin_id).first()
    if not admin_user or not admin_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return admin_user


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED, summary="Create new user feedback")
def create_feedback(feedback_data: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Creates a new user feedback/suggestion.
    Starts with is_read=False by default.
    """
    # Verify user exists
    user = db.query(User).filter(User.id == feedback_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found (ID: {feedback_data.user_id})"
        )

    new_feedback = Feedback(
        user_id=feedback_data.user_id,
        type=feedback_data.type,
        message=feedback_data.message,
        is_read=False
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


@router.get("/", response_model=List[FeedbackResponse], summary="List all user feedbacks")
def get_all_feedbacks(
    admin_id: int = Query(..., description="Admin user ID to authorize"),
    db: Session = Depends(get_db)
):
    """Returns all feedbacks sorted by unread first and then by date (Requires admin)."""
    _require_admin(admin_id, db)
    return db.query(Feedback).order_by(Feedback.is_read.asc(), Feedback.created_at.desc()).all()


@router.patch("/{feedback_id}/read", response_model=FeedbackResponse, summary="Mark a feedback as read")
def mark_feedback_as_read(
    feedback_id: int,
    admin_id: int = Query(..., description="Admin user ID to authorize"),
    db: Session = Depends(get_db)
):
    """Marks a user feedback message as read (Requires admin)."""
    _require_admin(admin_id, db)
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )

    feedback.is_read = True
    db.commit()
    db.refresh(feedback)
    return feedback
