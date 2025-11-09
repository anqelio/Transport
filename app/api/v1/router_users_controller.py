from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.users_controller import *
from app.db.session import get_session
from app.models.users import User
from app.schemas.schemas_requests import UserCreate
from app.security.auth_deps import require_roles, get_current_user

router = APIRouter()

@router.get('/user/{user_id}', description='Поиск пользователя по ID')
def router_get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # Добавлена аутентификация
):
    return get_user_by_id(user_id, session)

@router.post('/user', status_code=status.HTTP_201_CREATED, description='Добавление пользователя')
def router_add_user(
    data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["admin", "superadmin"]))
):
    return add_user(data, session)

@router.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление пользователя')
def router_delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["admin", "superadmin"]))
):
    return delete_user(user_id, session, current_user)

@router.put('/user/{user_id}', status_code=status.HTTP_200_OK, description='Изменение пользователя')
def router_update_user(
    user_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["admin", "superadmin"]))
):
    return update_user(user_id, data, session, current_user)

@router.get('/user', description='Вывод информации о пользователях', response_model=Page[User])
def router_show_user(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["superadmin"]))
):
    return show_users(session, page, size, current_user)
