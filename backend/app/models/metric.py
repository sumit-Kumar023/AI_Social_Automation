from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    platform = Column(String, nullable=False)     # facebook | instagram
    account_id = Column(String, nullable=False)

    followers = Column(Integer)
    likes = Column(Integer)
    comments = Column(Integer)
    reach = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
