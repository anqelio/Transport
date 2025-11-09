from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.users import User
from app.schemas.schemas_requests import UserLogin, Token
from app.security.auth_utils import verify_password, create_access_token


def login_user(login_data, session):
    try:
        sql = select(User).where(User.login == login_data.login)
        user = session.exec(sql).first()

        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный логин или пароль"
            )

        access_token = create_access_token(data={"sub": user.login})
        return Token(access_token=access_token, token_type="bearer")
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Ошибка: нарушение целостности данных")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")