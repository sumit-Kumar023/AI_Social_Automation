from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import SessionLocal
from app.models.post import Post
from app.services.posting import get_social_account
from app.services.social_api import (
    post_to_facebook_page,
    create_instagram_container,
    publish_instagram_container,
)


def check_and_post_scheduled_posts():
    
    """
    This function runs periodically.
    It finds due posts and publishes them to the correct platform.
    """
    db: Session = SessionLocal()

    try:
        now = datetime.now(timezone.utc)

        due_posts = (
            db.query(Post)
            .filter(Post.status == "scheduled")
            .filter(Post.scheduled_at <= now)
            .all()
        )
        for post in due_posts:
            try:
                social_account = get_social_account(
                    db=db,
                    user_id=post.user_id,
                    platform=post.platform,
                )

                if not social_account:
                    raise Exception("No connected social account found")

                # ---------------- FACEBOOK ----------------
                if post.platform == "facebook":
                    post_to_facebook_page(
                        page_id=social_account.account_id,
                        page_token=social_account.access_token,
                        message=post.content,
                    )

                # ---------------- INSTAGRAM ----------------
                elif post.platform == "instagram":
                    creation_id = create_instagram_container(
                        ig_user_id=social_account.account_id,
                        access_token=social_account.access_token,
                        caption=post.content,
                        image_url=post.media_url,
                    )

                    publish_instagram_container(
                        ig_user_id=social_account.account_id,
                        creation_id=creation_id,
                        access_token=social_account.access_token,
                    )

                # ---------------- THREADS (OPTIONAL PLACEHOLDER) ----------------
                elif post.platform == "threads":
                    # Threads posting API is limited.
                    # We mark as failed or treat as IG text-only if required.
                    raise Exception("Threads posting not implemented yet")

                else:
                    raise Exception(f"Unsupported platform: {post.platform}")

                # If everything succeeds
                post.status = "posted"

            except Exception as e:
                post.status = "failed"
                print(f"[Scheduler] Post {post.id} failed:", e)

        db.commit()

    finally:
        db.close()


def start_scheduler():
    """
    Starts APScheduler when FastAPI app boots.
    """
    scheduler = BackgroundScheduler(timezone=timezone.utc)

    scheduler.add_job(
        check_and_post_scheduled_posts,
        trigger="interval",
        seconds=60,
        id="post_scheduler",
        replace_existing=True,
        max_instances=1,   # prevents overlapping runs
    )

    scheduler.start()
    print("[Scheduler] Started successfully")
