from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.stops import Stop


def get_stop_by_id(id, session) -> Stop:
    '''
    Поиск остановки по ID
    :param id:
    :param session:
    :return: Stop
    '''
    try:
        result = session.get(Stop, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_stop(data, session) -> Optional[Stop]:
    '''
    Добавление остановки
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Stop(
            name_stop=data.name_stop,
            latitude=data.latitude,
            longitude=data.longitude,
            has_pavilion=data.has_pavilion
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


def delete_stop_by_id(id, session) -> str:
    '''
    Удаление остановки
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Stop, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_stop(id, data, session) -> Stop:
    '''
    Изменение остановки
    :param data:
    :param session:
    :return: Stop
    '''
    try:
        result = session.get(Stop, id)
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


def show_stops(session: Session = Depends(get_session), page: int = 1, size: int = 10) -> Page[Stop]:
    '''
    Вывод информации по остановкам
    :param session:
    :param page
    :param size
    :return: Page[Stop]
    '''
    try:
        sql = select(Stop)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
