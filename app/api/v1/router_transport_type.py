from fastapi import Depends, status, APIRouter
from sqlmodel import Session
from app.controllers.transport_type_controller import *
from app.db.session import get_session
from app.models.transport_types import Transport

router = APIRouter()


@router.get('/get/{transport_id}', description='Поиск вида транспорта по ID')
def router_get_transport_type_by_id(transport_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для поиска вида транспорта по ID
    :param transport_id:
    :param session:
    :return: get_transport_type_by_id(transport_id, session)
    '''
    return get_transport_type_by_id(transport_id, session)


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Добавление вида транспорта')
def router_add_transport_type(data: Transport, session: Session = Depends(get_session)):
    '''
    Ручка для создания вида транпорта
    :param data:
    :param session:
    :return: add_transport_type(data, session)
    '''
    return add_transport_type(data, session)


@router.delete('/delete/{transport_id}', status_code=status.HTTP_200_OK, description='Удаление вида транспорта')
def router_delete_transport_type(transport_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для удаления вида транспорта
    :param transport_id:
    :param session:
    :return: delete_transport_type(transport_id, session)
    '''
    return delete_transport_type_id(transport_id, session)

@router.put('/update', status_code=status.HTTP_200_OK, description='Изменение вида транспорта')
def router_update_transport_type(transport_id: int, data: Transport, session: Session = Depends(get_session)):
    '''
    Ручка для изменения вида транспорта
    :param transport_id:
    :param session:
    :return: update_transport_type(id, session)
    '''
    update_transport_type(transport_id, data, session)

@router.get('/show', description='Вывод информации о видах транспорта')
def router_show_transport_type(session: Session = Depends(get_session)):
    '''
    Ручка для вывода вида транспорта
    :param session:
    :return: show_transport_type(session)
    '''
    return show_transport_type(session)