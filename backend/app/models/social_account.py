from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    platform = Column(String, nullable=False)  # instagram | facebook | threads
    account_id = Column(String, nullable=False)  # Meta page / IG ID
    account_name = Column(String)

    access_token = Column(String, nullable=False)
    token_expires_at = Column(DateTime)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
