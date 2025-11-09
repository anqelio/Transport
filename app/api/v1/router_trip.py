from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.trip_controller import *
from app.db.session import get_session
from app.models.trips import Trip
from app.schemas.schemas_requests import TripCreate

router = APIRouter()


@router.get('/trip/{trip_id}', description='Поиск поездки по ID')
def router_get_trip_by_id(trip_id: int, session: Session = Depends(get_session)):
    return get_trip_by_id(trip_id, session)


@router.post('/trip', status_code=status.HTTP_201_CREATED, description='Добавление поездки')
def router_add_trip(data: TripCreate, session: Session = Depends(get_session)):
    return add_trip(data, session)


@router.delete('/trip/{trip_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление поездки')
def router_delete_trip(trip_id: int, session: Session = Depends(get_session)):
    return delete_trip(trip_id, session)


@router.put('/trip/{trip_id}', status_code=status.HTTP_200_OK, description='Изменение поездки')
def router_update_trip(trip_id: int, data: Trip, session: Session = Depends(get_session)):
    return update_trip(trip_id, data, session)


@router.get('/trip', description='Вывод информации о остановках', response_model=Page[Trip])
def router_show_trip(session: Session = Depends(get_session), page: int = 1, size: int = 10):
    return show_trip(session, page, size)
