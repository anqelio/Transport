from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models import User
from app.models.transport_types import Transport


def get_transport_type_by_id(id, session, current_user) -> Transport:
    '''
    Поиск вида транспорта по ID
    :param id:
    :param session:
    :return: Transport
    '''
    try:
        result = session.get(Transport, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_transport_type(data, session, current_user) -> Optional[Transport]:
    '''
    Добавление вида транспорта
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Transport(
            name_transport=data.name_transport
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


def delete_transport_type_id(id, session, current_user) -> str:
    '''
    Удаление вида транспорта
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Transport, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_transport_type(id, data, session, current_user) -> Transport:
    '''
    Изменение вида транспорта
    :param data:
    :param session:
    :return: Transport
    '''
    try:
        result = session.get(Transport, id)
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


def show_transport_type(session: Session = Depends(get_session), page: int = 1, size: int = 10, current_user: User = None) -> Page[Transport]:
    '''
    Вывод информации по видам транспорта
    :param session:
    :param page
    :param size
    :return: Page[Transport]
    '''
    try:
        sql = select(Transport)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
