from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Comment, User, Product
from schemas import CommentCreate, CommentResponse

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


def _require_admin(admin_id: int, db: Session) -> User:
    admin_user = db.query(User).filter(User.id == admin_id).first()
    if not admin_user or not admin_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return admin_user


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, summary="Create new product review")
def create_comment(comment_data: CommentCreate, db: Session = Depends(get_db)):
    """
    Creates a new product comment/rating.
    Starts with is_approved=False by default.
    """
    # Verify user exists
    user = db.query(User).filter(User.id == comment_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found (ID: {comment_data.user_id})"
        )

    # Verify product exists
    product = db.query(Product).filter(Product.id == comment_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found (ID: {comment_data.product_id})"
        )

    # Verify rating is between 1 and 5
    if comment_data.rating < 1 or comment_data.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    new_comment = Comment(
        product_id=comment_data.product_id,
        user_id=comment_data.user_id,
        rating=comment_data.rating,
        content=comment_data.content,
        is_approved=False
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/product/{product_id}", response_model=List[CommentResponse], summary="Get approved comments for a product")
def get_product_comments(product_id: int, db: Session = Depends(get_db)):
    """Returns only approved comments/reviews for a given product."""
    return db.query(Comment).filter(
        Comment.product_id == product_id,
        Comment.is_approved == True
    ).order_by(Comment.created_at.desc()).all()


@router.get("/pending", response_model=List[CommentResponse], summary="List all comments waiting for approval")
def get_pending_comments(
    admin_id: int = Query(..., description="Admin user ID to authorize"),
    db: Session = Depends(get_db)
):
    """Returns all comments with is_approved=False (Requires admin)."""
    _require_admin(admin_id, db)
    return db.query(Comment).filter(Comment.is_approved == False).order_by(Comment.created_at.desc()).all()


@router.patch("/{comment_id}/approve", response_model=CommentResponse, summary="Approve a pending comment")
def approve_comment(
    comment_id: int,
    admin_id: int = Query(..., description="Admin user ID to authorize"),
    db: Session = Depends(get_db)
):
    """Approves a review so it is displayed on the product page (Requires admin)."""
    _require_admin(admin_id, db)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    comment.is_approved = True
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Reject or delete a comment")
def delete_comment(
    comment_id: int,
    admin_id: int = Query(..., description="Admin user ID to authorize"),
    db: Session = Depends(get_db)
):
    """Deletes/rejects a comment from the database (Requires admin)."""
    _require_admin(admin_id, db)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    db.delete(comment)
    db.commit()
    return None
