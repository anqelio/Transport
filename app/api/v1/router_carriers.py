from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.carriers_controller import *
from app.db.session import get_session
from app.models.carriers import Carrier
from app.schemas.schemas_requests import CarrierCreate

router = APIRouter()


@router.get('/carrier/{carrier_id}', description='Поиск перевозчика по ID')
def router_get_carrier_by_id(carrier_id: int, session: Session = Depends(get_session)):
    return get_carrier_by_id(carrier_id, session)


@router.post('/carrier', status_code=status.HTTP_201_CREATED, description='Добавление перевозчика')
def router_add_carrier(data: CarrierCreate, session: Session = Depends(get_session)):
    return add_carrier(data, session)


@router.delete('/carrier/{carrier_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление перевозчика')
def router_delete_carrier(carrier_id: int, session: Session = Depends(get_session)):
    return delete_carrier_by_id(carrier_id, session)


@router.put('/carrier/{carrier_id}', status_code=status.HTTP_200_OK, description='Изменение перевозчика')
def router_update_carrier(carrier_id: int, data: Carrier, session: Session = Depends(get_session)):
    return update_carrier(carrier_id, data, session)


@router.get('/carrier', description='Вывод информации о перевозчиках', response_model=Page[Carrier])
def router_show_carrier(session: Session = Depends(get_session), page: int = 1, size: int = 10):
    return show_carrier(session)
