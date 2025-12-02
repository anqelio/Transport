from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models import User
from app.models.schedule_changes import ScheduleChanges


def get_schedule_changes_by_id(id, session, current_user) -> ScheduleChanges:
    '''
    Поиск изменений расписания по ID
    :param id:
    :param session:
    :return: ScheduleChanges
    '''
    try:
        result = session.get(ScheduleChanges, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_schedule_changes(data, session, current_user) -> Optional[ScheduleChanges]:
    '''
    Добавление изменения расписания
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = ScheduleChanges(
            trip_id=data.trip_id,
            reason=data.reason,
            date_trip=data.date_trip,
            old_time_trip=data.old_time_trip,
            time_new_trip=data.time_new_trip
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


def delete_schedule_changes_by_id(id, session, current_user) -> str:
    '''
    Удаление изменения расписания
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(ScheduleChanges, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_schedule_changes(id, data, session, current_user) -> ScheduleChanges:
    '''
    Изменение изменения расписания
    :param data:
    :param session:
    :return: ScheduleChanges
    '''
    try:
        result = session.get(ScheduleChanges, id)
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


def show_schedule_changes(session: Session = Depends(get_session), page: int = 1, size: int = 10, current_user: User = None) -> Page[ScheduleChanges]:
    '''
    Вывод изменений расписания
    :param session:
    :param page
    :param size
    :return: Page[ScheduleChanges]
    '''
    try:
        sql = select(ScheduleChanges)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
