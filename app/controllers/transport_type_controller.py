from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_session
from app.models.transport_types import Transport


def add_transport_type(data, session) -> Optional[Transport]:
    """
    Добавление вида транспорта
    :param data:
    :param session:
    :return: data
    """
    try:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка: дубликат или нарушение целостности данных")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Не удалось добавить цвет, ошибка: {str(e)}")