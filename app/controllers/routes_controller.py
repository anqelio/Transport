from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models import User
from app.models.routes import Routes


def get_route_by_number(number, session, current_user) -> Routes:
    '''
    Поиск маршрута по номеру
    :param number:
    :param session:
    :return: Routes
    '''
    try:
        result = session.query(Routes).filter(
            Routes.number_route == number
        ).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{number} маршрут не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_route(data, session, current_user) -> Optional[Routes]:
    '''
    Добавление маршрута
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Routes(
            number_route=data.number_route,
            start=data.start,
            stop=data.stop,
            operating_days=data.operating_days,
            total_time=data.total_time,
            transport_type=data.transport_type,
            carrier_id=data.carrier_id
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


def delete_route_by_id(id, session, current_user) -> str:
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


def update_route(id, data, session, current_user) -> Routes:
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


def show_routes(session: Session = Depends(get_session), page: int = 1, size: int = 10, current_user: User = None) -> Page[Routes]:
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
