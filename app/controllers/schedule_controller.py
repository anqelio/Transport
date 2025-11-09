from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.schedules import Schedule


def get_schedule_by_id(id, session) -> Schedule:
    '''
    Поиск расписания по ID
    :param id:
    :param session:
    :return: Schedule
    '''
    try:
        result = session.get(Schedule, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_schedule(data, session) -> Optional[Schedule]:
    '''
    Добавление расписания
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Schedule(
            route_id=data.route_id,
            departure_time=data.departure_time,
            is_weekend=data.is_weekend
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


def delete_schedule_by_id(id, session) -> str:
    '''
    Удаление расписания
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Schedule, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_schedule(id, data, session) -> Schedule:
    '''
    Изменение расписания
    :param data:
    :param session:
    :return: Schedule
    '''
    try:
        result = session.get(Schedule, id)
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


def show_schedules(session: Session = Depends(get_session), page: int = 1, size: int = 10) -> Page[Schedule]:
    '''
    Вывод расписания
    :param session:
    :param page
    :param size
    :return: Page[Schedule]
    '''
    try:
        sql = select(Schedule)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")