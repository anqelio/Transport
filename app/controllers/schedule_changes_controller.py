from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.schedule_changes import ScheduleChanges


def get_schedule_changes_by_id(id, session) -> ScheduleChanges:
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


def add_schedule_changes(data, session) -> Optional[ScheduleChanges]:
    '''
    Добавление изменения расписания
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
                            detail=f"Не удалось добавить изменение расписания, ошибка: {str(e)}")


def delete_schedule_changes_by_id(id, session) -> str:
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


def update_schedule_changes(id, data, session) -> ScheduleChanges:
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


def show_schedule_changes(session: Session = Depends(get_session), page: int = 1, size: int = 10) -> Page[ScheduleChanges]:
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
