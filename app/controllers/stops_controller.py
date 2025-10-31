from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.stops import Stop


def get_stop_by_id(id, session) -> Stop:
    '''
    Поиск остановки по ID
    :param id:
    :param session:
    :return: Stop
    '''
    try:
        result = session.get(Stop, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_stop(data, session) -> Optional[Stop]:
    '''
    Добавление остановки
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
                            detail=f"Не удалось добавить остановку, ошибка: {str(e)}")


def delete_stop_by_id(id: int, session: Session = Depends(get_session)) -> str:
    '''
    Удаление остановки
    :param data:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Stop, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_stop(id, data, session) -> Stop:
    '''
    Изменение остановки
    :param data:
    :param session:
    :return: Stop
    '''
    try:
        result = session.get(Stop, id)
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


def show_stops(session) -> List[Stop]:
    '''
    Вывод информации по остановкам
    :param session:
    :return: List[Stop]
    '''
    try:
        sql = select(Stop)
        result = session.exec(sql).all()
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
