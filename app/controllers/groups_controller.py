from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models import User
from app.models.groups import UserGroup


def get_group_by_id(id, session, current_user) -> UserGroup:
    '''
    Поиск остановки на маршруте по ID
    :param id:
    :param session:
    :return: UserGroup
    '''
    try:
        result = session.get(UserGroup, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_group(data, session, current_user) -> Optional[UserGroup]:
    '''
    Добавление остановки на маршруте
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = UserGroup(
            route_id=data.route_id,
            stop_id=data.stop_id,
            minutes_to_next_stop=data.minutes_to_next_stop
        )
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Ошибка: нарушение целостности данных")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


def delete_group_by_id(id, session, current_user) -> str:
    '''
    Удаление остановки на маршруте
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(UserGroup, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_group(id, data, session, current_user) -> UserGroup:
    '''
    Изменение остановки на маршруте
    :param data:
    :param session:
    :return: UserGroup
    '''
    try:
        result = session.get(UserGroup, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(result, key, value)
        session.commit()
        session.refresh(result)
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def show_group(session: Session = Depends(get_session), page: int = 1, size: int = 10, current_user: User = None) -> Page[UserGroup]:
    '''
    Вывод остановки на маршруте
    :param session:
    :param page
    :param size
    :return: Page[UserGroup]
    '''
    try:
        sql = select(UserGroup)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")