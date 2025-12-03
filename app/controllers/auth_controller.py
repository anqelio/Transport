from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.users import User
from app.schemas.schemas_requests import UserLogin
from app.schemas.schemas_response import TokenResponse
from app.security.auth_utils import (
    verify_password,
    create_access_token,
    create_refresh_token,
    refresh_tokens,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


def login_user(login_data: UserLogin, session: Session) -> TokenResponse:
    try:
        sql = select(User).where(User.login == login_data.login)
        user = session.exec(sql).first()

        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный логин или пароль"
            )

        access_token = create_access_token(data={"sub": user.login})
        refresh_token = create_refresh_token(data={"sub": user.login})

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # В секундах
        )
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Ошибка: нарушение целостности данных")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


def refresh_user_tokens(refresh_token: str) -> TokenResponse:
    try:
        new_access_token, new_refresh_token = refresh_tokens(refresh_token)

        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            refresh_token=new_refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Не удалось обновить токены: {str(e)}"
        )