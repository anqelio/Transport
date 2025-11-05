from fastapi import Depends, status, APIRouter
from sqlmodel import Session
from app.controllers.routes_controller import *
from app.db.session import get_session
from app.models.routes import Routes

router = APIRouter()


@router.get('/route/{route_id}', description='Поиск маршрута по ID')
def router_get_route_by_id(route_id: int, session: Session = Depends(get_session)):
    return get_route_by_id(route_id, session)


@router.post('/route', status_code=status.HTTP_201_CREATED, description='Добавление маршрута')
def router_add_route(data: Routes, session: Session = Depends(get_session)):
    return add_route(data, session)


@router.delete('/route/{route_id}', status_code=status.HTTP_200_OK, description='Удаление маршрута')
def router_delete_route(route_id: int, session: Session = Depends(get_session)):
    return delete_route_by_id(route_id, session)


@router.put('/route/{route_id}', status_code=status.HTTP_200_OK, description='Изменение маршрута')
def router_update_stop(route_id: int, data: Routes, session: Session = Depends(get_session)):
    return update_route(route_id, data, session)


@router.get('/route', description='Вывод информации о маршрутах')
def router_show_route(session: Session = Depends(get_session)):
    return show_routes(session)