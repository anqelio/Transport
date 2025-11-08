from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.stops_controller import *
from app.db.session import get_session
from app.models.stops import Stop

router = APIRouter()


@router.get('/stop/{stop_id}', description='Поиск остановки по ID')
def router_get_stop_by_id(stop_id: int, session: Session = Depends(get_session)):
    return get_stop_by_id(stop_id, session)


@router.post('/stop', status_code=status.HTTP_201_CREATED, description='Добавление остановки')
def router_add_stop(data: Stop, session: Session = Depends(get_session)):
    return add_stop(data, session)


@router.delete('/stop/{stop_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление остановки')
def router_delete_stop(stop_id: int, session: Session = Depends(get_session)):
    return delete_stop_by_id(stop_id, session)


@router.put('/stop/{stop_id}', status_code=status.HTTP_200_OK, description='Изменение остановки')
def router_update_stop(stop_id: int, data: Stop, session: Session = Depends(get_session)):
    return update_stop(stop_id, data, session)


@router.get('/stop', description='Вывод информации о остановках', response_model=Page[Stop])
def router_show_stop(session: Session = Depends(get_session), page: int = 1, size: int = 10):
    return show_stops(session, page, size)
