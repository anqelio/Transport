from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models import User
from app.models.employee_schedules import EmployeeSchedules


def get_employee_schedule_by_id(id, session, current_user) -> EmployeeSchedules:
    '''
    Поиск расписания рабочих по ID
    :param id:
    :param session:
    :return: EmployeeSchedules
    '''
    try:
        result = session.get(EmployeeSchedules, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_employee_schedule(data, session, current_user) -> Optional[EmployeeSchedules]:
    '''
    Добавление расписания рабочих
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = EmployeeSchedules(
            employee_id=data.employee_id,
            trip_id=data.trip_id,
            work_date=data.work_date,
            planned_start_time=data.planned_start_time,
            planned_end_time=data.planned_end_time
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


def delete_employee_schedule_by_id(id, session, current_user) -> str:
    '''
    Удаление расписания рабочих
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(EmployeeSchedules, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_employee_schedule(id, data, session, current_user) -> EmployeeSchedules:
    '''
    Изменение расписания рабочих
    :param data:
    :param session:
    :return: EmployeeSchedules
    '''
    try:
        result = session.get(EmployeeSchedules, id)
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


def show_employee_schedule(session: Session = Depends(get_session), page: int = 1, size: int = 10, current_user: User = None) -> Page[EmployeeSchedules]:
    '''
    Вывод расписания рабочих
    :param session:
    :param page
    :param size
    :return: Page[EmployeeSchedules]
    '''
    try:
        sql = select(EmployeeSchedules)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
