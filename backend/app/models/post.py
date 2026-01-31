from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    platform = Column(String, nullable=False)  
    # instagram | facebook | threads

    content = Column(Text, nullable=False)
    media_url = Column(String, nullable=True)

    scheduled_at = Column(DateTime, nullable=False)

    status = Column(String, default="scheduled")
    # scheduled | posted | failed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
