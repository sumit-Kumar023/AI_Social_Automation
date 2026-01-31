from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.metric import Metric
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/monitor", tags=["Dashboard"])

@router.get("/metrics")
def get_metrics(
    platform: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return (
        db.query(Metric)
        .filter(
            Metric.user_id == current_user.id,
            Metric.platform == platform,
        )
        .order_by(Metric.created_at)
        .all()
    )
