import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import select, Session
from app.models.users import User
from app.db.session import get_session

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()


async def get_current_user(
        credentials=Depends(security),
        session: Session = Depends(get_session)
) -> User:
    try:
        token = credentials.credentials

        # Remove redundant load_dotenv() calls
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    # Find user by login
    sql = select(User).where(User.login == username)
    user = session.exec(sql).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def require_roles(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user

    return role_checker