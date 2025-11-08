from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.route_stops_controller import *
from app.db.session import get_session
from app.models.route_stops import RouteStop

router = APIRouter()


@router.get('/route_stop/{route_stop_id}', description='Поиск остановки на маршруте по ID')
def router_get_employee_by_id(route_stop_id: int, session: Session = Depends(get_session)):
    return get_route_stop_by_id(route_stop_id, session)


@router.post('/route_stop', status_code=status.HTTP_201_CREATED, description='Добавление остановки на маршруте')
def router_add_employee(data: RouteStop, session: Session = Depends(get_session)):
    return add_route_stop(data, session)


@router.delete('/route_stop/{route_stop_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление остановки на маршруте')
def router_delete_employee(route_stop_id: int, session: Session = Depends(get_session)):
    return delete_route_stop_by_id(route_stop_id, session)


@router.put('/route_stop/{route_stop_id}', status_code=status.HTTP_200_OK, description='Изменение остановки на маршруте')
def router_update_employee(route_stop_id: int, data: RouteStop, session: Session = Depends(get_session)):
    return update_route_stop(route_stop_id, data, session)


@router.get('/route_stop', description='Вывод остановки на маршруте', response_model=Page[RouteStop])
def router_show_employee(session: Session = Depends(get_session), page: int = 1, size: int = 10):
    return show_route_stop(session, page, size)