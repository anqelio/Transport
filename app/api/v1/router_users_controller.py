from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.users_controller import *
from app.db.session import get_session
from app.models.users import User

router = APIRouter()


@router.get('/user/{user_id}', description='Поиск пользователя по ID')
def router_get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    return get_user_by_id(user_id, session)


@router.post('/user', status_code=status.HTTP_201_CREATED, description='Добавление пользователя')
def router_add_user(data: User, session: Session = Depends(get_session)):
    return add_user(data, session)


@router.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление пользователя')
def router_delete_user(user_id: int, session: Session = Depends(get_session)):
    return delete_user(user_id, session)


@router.put('/user/{user_id}', status_code=status.HTTP_200_OK, description='Изменение пользователя')
def router_update_user(user_id: int, data: User, session: Session = Depends(get_session)):
    return update_user(user_id, data, session)


@router.get('/user', description='Вывод информации о пользователях', response_model=Page[User])
def router_show_user(session: Session = Depends(get_session), page: int = 1, size: int = 10):
    return show_users(session, page, size)
