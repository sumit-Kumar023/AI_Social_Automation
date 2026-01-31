from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.utils.dependencies import get_current_user
from app.database import get_db
from app.models.social_account import SocialAccount
from app.services.social_api import (
    build_meta_oauth_url,
    exchange_code_for_token,
    get_facebook_pages,
    get_instagram_account,
)

router = APIRouter(prefix="/social", tags=["Social Accounts"])


# -------------------------------------------------
# STEP 1: CONNECT (JWT PROTECTED)
# -------------------------------------------------
@router.get("/connect")
def connect_social_account(current_user=Depends(get_current_user)):
    """
    Generates Meta (Facebook + Instagram) OAuth URL
    Only accessible by logged-in users
    """
    oauth_url = build_meta_oauth_url(current_user.id)
    return {"auth_url": oauth_url}


# -------------------------------------------------
# STEP 2: CALLBACK (META REDIRECTS HERE)
# -------------------------------------------------
@router.get("/callback")
def meta_oauth_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    code = request.query_params.get("code")
    user_id = request.query_params.get("state")

    if not code or not user_id:
        raise HTTPException(status_code=400, detail="Invalid OAuth response")

    # 1️⃣ Exchange code → user access token
    token_data = exchange_code_for_token(code)
    user_token = token_data.get("access_token")

    if not user_token:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

    # 2️⃣ Get Facebook Pages
    pages = get_facebook_pages(user_token)

    for page in pages:
        # 3️⃣ Save Facebook Page
        fb_account = SocialAccount(
            user_id=int(user_id),
            platform="facebook",
            account_id=page["id"],
            account_name=page["name"],
            access_token=page["access_token"],
        )
        db.add(fb_account)

        # 4️⃣ Check for connected Instagram Business Account
        ig = get_instagram_account(page["id"], page["access_token"])

        if ig:
            ig_account = SocialAccount(
                user_id=int(user_id),
                platform="instagram",
                account_id=ig["id"],
                account_name=page["name"],
                access_token=page["access_token"],
            )
            db.add(ig_account)

    db.commit()

    # 5️⃣ Redirect back to frontend dashboard
    return RedirectResponse(url="http://localhost:5173/")


@router.get("/accounts")
def list_social_accounts(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    accounts = (
        db.query(SocialAccount)
        .filter(SocialAccount.user_id == current_user.id)
        .all()
    )

    return [
        {
            "platform": acc.platform,
            "account_id": acc.account_id,
            "account_name": acc.account_name,
        }
        for acc in accounts
    ]