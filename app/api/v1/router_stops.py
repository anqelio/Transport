from fastapi import Depends, status, APIRouter
from sqlmodel import Session
from app.controllers.stops_controller import *
from app.db.session import get_session
from app.models.stops import Stop

router = APIRouter()


@router.get('/get/{stop_id}', description='Поиск остановки по ID')
def router_get_stop_by_id(stop_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для поиска вида транспорта по ID
    :param stop_id:
    :param session:
    :return: get_stop_by_id(stop_id, session)
    '''
    return get_stop_by_id(stop_id, session)


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Добавление остановки')
def router_add_stop(data: Stop, session: Session = Depends(get_session)):
    '''
    Ручка для создания остановки
    :param data:
    :param session:
    :return: add_stop(data, session)
    '''
    return add_stop(data, session)


@router.delete('/delete/{stop_id}', status_code=status.HTTP_200_OK, description='Удаление остановки')
def router_delete_stop(stop_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для удаления остановки
    :param stop_id:
    :param session:
    :return: delete_stop_by_id(stop_id, session)
    '''
    return delete_stop_by_id(stop_id, session)


@router.put('/update/{stop_id}', status_code=status.HTTP_200_OK, description='Изменение остановки')
def router_update_stop(stop_id: int, data: Stop, session: Session = Depends(get_session)):
    '''
    Ручка для изменения остановки
    :param stop_id:
    :param session:
    :return: update_transport_type(id, session)
    '''
    update_stop(stop_id, data, session)


@router.get('/show', description='Вывод информации о остановках')
def router_show_stop(session: Session = Depends(get_session)):
    '''
    Ручка для вывода остановок
    :param session:
    :return: show_stops(session)
    '''
    return show_stops(session)
