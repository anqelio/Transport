from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models import User
from app.models.employees import Employee


def get_employee_by_position(position, session, current_user) -> Employee:
    '''
    Поиск сотрудника по позиции
    :param position:
    :param session:
    :return: Employee
    '''
    try:
        result = session.query(Employee).filter(
            Employee.position == position
        ).all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{position} не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_employee(data, session, current_user) -> Optional[Employee]:
    '''
    Добавление сотрудника
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Employee(
            position=data.position,
            carrier_id=data.carrier_id,
            name=data.name,
            surname=data.surname
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


def delete_employee_by_id(id, session, current_user) -> str:
    '''
    Удаление сотрудника
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Employee, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_employee(id, data, session, current_user) -> Employee:
    '''
    Изменение сотрудника
    :param data:
    :param session:
    :return: Employee
    '''
    try:
        result = session.get(Employee, id)
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


def show_employee(session: Session = Depends(get_session), page: int = 1, size: int = 10, current_user: User = None) -> Page[Employee]:
    '''
    Вывод информации по сотрудникам
    :param session:
    :param page
    :param size
    :return: Page[Employee]
    '''
    try:
        sql = select(Employee)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
