from fastapi import APIRouter
from typing import Optional
import requests

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["oauth"]
)


@oauth_router.get("/authorize")
async def initiate_oauth_login(client_id: str, redirect_uri: str, response_type: str = "code", scope: str = "", state: str = ""):
    authorization_url = f"https://oauth.provider.com/authorize?client_id={client_id}&redirect_uri={
        redirect_uri}&response_type={response_type}&scope={scope}&state={state}"
    return {"redirect_url": authorization_url}


@oauth_router.post("/token")
async def exchange_code_for_token(grant_type: str, code: Optional[str] = None, redirect_uri: Optional[str] = None, refresh_token: Optional[str] = None, client_id: str = "", client_secret: str = ""):
    token_url = "https://oauth.provider.com/token"
    payload = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": redirect_uri,
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(token_url, data=payload)
    return response.json()
