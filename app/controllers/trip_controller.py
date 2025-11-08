from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.trips import Trip


def get_trip_by_id(id, session) -> Trip:
    '''
    Поиск поездок по ID
    :param id:
    :param session:
    :return: Trip
    '''
    try:
        result = session.get(Trip, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_trip(data, session) -> Optional[Trip]:
    '''
    Добавление поездки
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
                            detail=f"Не удалось добавить поездку, ошибка: {str(e)}")


def delete_trip(id, session) -> str:
    '''
    Удаление поездки
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Trip, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_trip(id, data, session) -> Trip:
    '''
    Изменение поездки
    :param data:
    :param session:
    :return: Trip
    '''
    try:
        result = session.get(Trip, id)
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


def show_trip(session: Session = Depends(get_session), page: int = 1, size: int = 10) -> Page[Trip]:
    '''
    Вывод информации по поездке
    :param session:
    :param page
    :param size
    :return: List[Trip]
    '''
    try:
        sql = select(Trip)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
