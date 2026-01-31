from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.post import Post
from app.schemas.post import PostCreate
from zoneinfo import ZoneInfo


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/")
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Create a scheduled post for a platform (instagram/facebook).
    """

    IST = ZoneInfo("Asia/Kolkata")
    scheduled_at = post.scheduled_at

    # 🔧 FIX: normalize naive datetime to UTC
    if scheduled_at.tzinfo is None:
        scheduled_at = scheduled_at.replace(tzinfo=IST).astimezone(timezone.utc)
    # Validate scheduled time
    if scheduled_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Scheduled time must be in the future",
        )

    new_post = Post(
        user_id=current_user.id,
        platform=post.platform,
        content=post.content,
        media_url=post.media_url,
        scheduled_at=scheduled_at,
        status="scheduled",
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/")
def list_posts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    List all posts for the logged-in user.
    """

    posts = (
        db.query(Post)
        .filter(Post.user_id == current_user.id)
        .order_by(Post.scheduled_at.desc())
        .all()
    )

    return posts
