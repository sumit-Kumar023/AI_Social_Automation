from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.metric import Metric
from app.models.social_account import SocialAccount
from app.services.social_api import (
    get_facebook_page_metrics,
    get_instagram_metrics,
)

def fetch_and_store_metrics():
    db: Session = SessionLocal()

    try:
        accounts = db.query(SocialAccount).all()

        for acc in accounts:
            if acc.platform == "facebook":
                data = get_facebook_page_metrics(
                    acc.account_id, acc.access_token
                )

                metric = Metric(
                    user_id=acc.user_id,
                    platform="facebook",
                    account_id=acc.account_id,
                    followers=data["followers"],
                )

            elif acc.platform == "instagram":
                data = get_instagram_metrics(
                    acc.account_id, acc.access_token
                )

                metric = Metric(
                    user_id=acc.user_id,
                    platform="instagram",
                    account_id=acc.account_id,
                    followers=data["followers"],
                )

            else:
                continue

            db.add(metric)

        db.commit()

    finally:
        db.close()
