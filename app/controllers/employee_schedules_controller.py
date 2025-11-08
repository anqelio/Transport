from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.employee_schedules import EmployeeSchedules


def get_employee_schedule_by_id(id, session) -> EmployeeSchedules:
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


def add_employee_schedule(data, session) -> Optional[EmployeeSchedules]:
    '''
    Добавление расписания рабочих
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
                            detail=f"Не удалось добавить расписание рабочих, ошибка: {str(e)}")


def delete_employee_schedule_by_id(id, session) -> str:
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


def update_employee_schedule(id, data, session) -> EmployeeSchedules:
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


def show_employee_schedule(session: Session = Depends(get_session), page: int = 1, size: int = 10) -> Page[EmployeeSchedules]:
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
