from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.employees import Employee


def get_employee_by_id(id, session) -> Employee:
    '''
    Поиск сотрудника по ID
    :param id:
    :param session:
    :return: Employee
    '''
    try:
        result = session.get(Employee, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_employee(data, session) -> Optional[Employee]:
    '''
    Добавление сотрудника
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
                            detail=f"Не удалось добавить сотрудника, ошибка: {str(e)}")


def delete_employee_by_id(id, session) -> str:
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


def update_employee(id, data, session) -> Employee:
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


def show_employee(session) -> List[Employee]:
    '''
    Вывод информации по сотрудникам
    :param session:
    :return: List[Employee]
    '''
    try:
        sql = select(Employee)
        result = session.exec(sql).all()
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
