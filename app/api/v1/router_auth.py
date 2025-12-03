import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.schemas_requests import UserLogin, Token, TokenRefresh
from app.controllers.auth_controller import login_user, refresh_user_tokens
from app.schemas.schemas_response import TokenResponse

router = APIRouter()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    return login_user(login_data, session)

@router.post("/refresh", response_model=TokenResponse)
def refresh(token_data: TokenRefresh):
    return refresh_user_tokens(token_data.refresh_token)