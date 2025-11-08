from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.transport_types import Transport


def get_transport_type_by_id(id, session) -> Transport:
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


def add_transport_type(data, session) -> Optional[Transport]:
    '''
    Добавление вида транспорта
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
                            detail=f"Не удалось добавить вид транспорта, ошибка: {str(e)}")


def delete_transport_type_id(id, session) -> str:
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


def update_transport_type(id, data, session) -> Transport:
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


def show_transport_type(session: Session = Depends(get_session), page: int = 1, size: int = 10) -> Page[Transport]:
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
