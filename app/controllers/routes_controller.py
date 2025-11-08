from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.routes import Routes


def get_route_by_id(id, session) -> Routes:
    '''
    Поиск маршрута по ID
    :param id:
    :param session:
    :return: Routes
    '''
    try:
        result = session.get(Routes, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_route(data, session) -> Optional[Routes]:
    '''
    Добавление маршрута
    :param data:
    :param session:
    :return: data
    '''
    try:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Ошибка: дубликат или нарушение целостности данных")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Не удалось добавить остановку, ошибка: {str(e)}")


def delete_route_by_id(id, session) -> str:
    '''
    Удаление маршрута
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Routes, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_route(id, data, session) -> Routes:
    '''
    Изменение маршрута
    :param data:
    :param session:
    :return: Routes
    '''
    try:
        result = session.get(Routes, id)
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


def show_routes(session: Session = Depends(get_session), page: int = 1, size: int = 10) -> Page[Routes]:
    '''
    Вывод информации по маршрутам
    :param session:
    :param page
    :param size
    :return: Page[Routes]
    '''
    try:
        sql = select(Routes)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
