from urllib.parse import urlencode
from app.config import settings
import requests

META_OAUTH_BASE_URL = "https://www.facebook.com/v18.0/dialog/oauth"

META_SCOPES = [
    "pages_show_list",
    "pages_read_engagement",
    "pages_manage_posts",
    "instagram_basic",
    "instagram_content_publish",
]

META_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
META_GRAPH_BASE = "https://graph.facebook.com/v18.0"



def build_meta_oauth_url(user_id: int):
    params = {
        "client_id": settings.META_APP_ID,
        "redirect_uri": settings.META_REDIRECT_URI,
        "scope": ",".join(META_SCOPES),
        "response_type": "code",
        "state": str(user_id)
    }

    return f"{META_OAUTH_BASE_URL}?{urlencode(params)}"

def exchange_code_for_token(code: str):
    params = {
        "client_id": settings.META_APP_ID,
        "client_secret": settings.META_APP_SECRET,
        "redirect_uri": settings.META_REDIRECT_URI,
        "code": code,
    }

    response = requests.get(META_TOKEN_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_facebook_pages(access_token: str):
    url = f"{META_GRAPH_BASE}/me/accounts"
    params = {"access_token": access_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["data"]

def get_instagram_account(page_id: str, page_token: str):
    url = f"{META_GRAPH_BASE}/{page_id}"
    params = {
        "fields": "instagram_business_account",
        "access_token": page_token,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("instagram_business_account")

def post_to_facebook_page(page_id: str, page_token: str, message: str):
    url = f"{META_GRAPH_BASE}/{page_id}/feed"
    data = {
        "message": message,
        "access_token": page_token,
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()




def create_instagram_container(
    ig_user_id: str,
    access_token: str,
    caption: str,
    image_url: str | None = None,
):
    url = f"{META_GRAPH_BASE}/{ig_user_id}/media"

    data = {
        "caption": caption,
        "access_token": access_token,
    }

    if image_url:
        data["image_url"] = image_url

    response = requests.post(url, data=data)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()["id"]  # creation_id

def publish_instagram_container(
    ig_user_id: str,
    creation_id: str,
    access_token: str,
):
    url = f"{META_GRAPH_BASE}/{ig_user_id}/media_publish"

    data = {
        "creation_id": creation_id,
        "access_token": access_token,
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()

def get_facebook_page_metrics(page_id: str, access_token: str):
    url = f"{META_GRAPH_BASE}/{page_id}"
    params = {
        "fields": "fan_count",
        "access_token": access_token,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return {
        "followers": data.get("fan_count", 0)
    }


def get_instagram_metrics(ig_user_id: str, access_token: str):
    url = f"{META_GRAPH_BASE}/{ig_user_id}"
    params = {
        "fields": "followers_count,media_count",
        "access_token": access_token,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return {
        "followers": data.get("followers_count", 0),
        "posts": data.get("media_count", 0),
    }





