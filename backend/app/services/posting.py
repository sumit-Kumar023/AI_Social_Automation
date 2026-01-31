from sqlalchemy.orm import Session
from app.models.social_account import SocialAccount

def get_social_account(db: Session, user_id: int, platform: str):
    return (
        db.query(SocialAccount)
        .filter(
            SocialAccount.user_id == user_id,
            SocialAccount.platform == platform,
        )
        .first()
    )
