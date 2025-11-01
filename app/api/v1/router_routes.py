from fastapi import Depends, status, APIRouter
from sqlmodel import Session
from app.controllers.routes_controller import *
from app.db.session import get_session
from app.models.routes import Routes

router = APIRouter()


@router.get('/get/{route_id}', description='Поиск маршрута по ID')
def router_get_route_by_id(route_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для поиска маршрута по ID
    :param route_id:
    :param session:
    :return: get_route_by_id(route_id, session)
    '''
    return get_route_by_id(route_id, session)


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Добавление маршрута')
def router_add_route(data: Routes, session: Session = Depends(get_session)):
    '''
    Ручка для создания маршрута
    :param data:
    :param session:
    :return: add_route(data, session)
    '''
    return add_route(data, session)


@router.delete('/delete/{route_id}', status_code=status.HTTP_200_OK, description='Удаление маршрута')
def router_delete_route(route_id: int, session: Session = Depends(get_session)):
    '''
    Ручка для удаления маршрута
    :param route_id:
    :param session:
    :return: delete_route_by_id(route_id, session)
    '''
    return delete_route_by_id(route_id, session)


@router.put('/update/{route_id}', status_code=status.HTTP_200_OK, description='Изменение маршрута')
def router_update_stop(route_id: int, data: Routes, session: Session = Depends(get_session)):
    '''
    Ручка для изменения маршрута
    :param route_id:
    :param session:
    :return: update_route(route_id, data, session)
    '''
    return update_route(route_id, data, session)


@router.get('/show', description='Вывод информации о маршрутах')
def router_show_route(session: Session = Depends(get_session)):
    '''
    Ручка для вывода маршрутов
    :param session:
    :return: show_routes(session)
    '''
    return show_routes(session)