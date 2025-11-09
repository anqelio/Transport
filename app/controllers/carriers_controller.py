from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.carriers import Carrier


def get_carrier_by_id(id, session) -> Carrier:
    '''
    Поиск перевозчика по ID
    :param id:
    :param session:
    :return: Carrier
    '''
    try:
        result = session.get(Carrier, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_carrier(data, session) -> Optional[Carrier]:
    '''
    Добавление перевозчика
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Carrier(
            name_company=data.name_company,
            contact_info=data.contact_info
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


def delete_carrier_by_id(id, session) -> str:
    '''
    Удаление перевозчика
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Carrier, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_carrier(id, data, session) -> Carrier:
    '''
    Изменение перевозчика
    :param data:
    :param session:
    :return: Routes
    '''
    try:
        result = session.get(Carrier, id)
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


def show_carrier(session: Session = Depends(get_session), page: int = 1, size: int = 1) -> Page[Carrier]:
    '''
    Вывод информации по перевозчикам
    :param session:
    :param page
    :param size
    :return: Page[Carrier]
    '''
    try:
        sql = select(Carrier)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
