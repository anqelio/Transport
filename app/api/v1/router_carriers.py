from fastapi import Depends, status, APIRouter
from sqlmodel import Session
from app.controllers.carriers_controller import *
from app.db.session import get_session
from app.models.carriers import Carrier

router = APIRouter()


@router.get('/get/{carrier_id}', description='Поиск перевозчика по ID')
def router_get_carrier_by_id(carrier_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для поиска перевозчика по ID
    :param carrier_id:
    :param session:
    :return: get_route_by_id(carrier_id, session)
    '''
    return get_carrier_by_id(carrier_id, session)


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Добавление перевозчика')
def router_add_carrier(data: Carrier, session: Session = Depends(get_session)):
    '''
    Ручка для создания перевозчика
    :param data:
    :param session:
    :return: add_carrier(data, session)
    '''
    return add_carrier(data, session)


@router.delete('/delete/{carrier_id}', status_code=status.HTTP_200_OK, description='Удаление перевозчика')
def router_delete_carrier(carrier_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для удаления перевозчика
    :param carrier_id:
    :param session:
    :return: delete_carrier_by_id(carrier_id, session)
    '''
    return delete_carrier_by_id(carrier_id, session)


@router.put('/update/{carrier_id}', status_code=status.HTTP_200_OK, description='Изменение перевозчика')
def router_update_carrier(carrier_id: int, data: Carrier, session: Session = Depends(get_session)):
    '''
    Ручка для изменения перевозчика
    :param carrier_id:
    :param session:
    :return: update_carrier(carrier_id, data, session)
    '''
    return update_carrier(carrier_id, data, session)


@router.get('/show', description='Вывод информации о перевозчиках')
def router_show_carrier(session: Session = Depends(get_session)):
    '''
    Ручка для вывода перевозчиков
    :param session:
    :return: show_carrier(session)
    '''
    return show_carrier(session)