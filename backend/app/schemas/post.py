from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    platform: str
    content: str
    media_url: Optional[str] = None
    scheduled_at: datetime

class PostResponse(BaseModel):
    id: int
    platform: str
    content: str
    media_url: Optional[str]
    scheduled_at: datetime
    status: str

    class Config:
        from_attributes = True
