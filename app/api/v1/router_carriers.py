from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.carriers_controller import *
from app.db.session import get_session
from app.models import User
from app.models.carriers import Carrier
from app.schemas.schemas_requests import CarrierCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/carrier/{title}', description='Поиск перевозчика по названию')
def router_get_carrier_by_title(title: str,
                             session: Session = Depends(get_session),
                             current_user: User = Depends(require_roles(["operator", "admin", "superadmin"]))):
    return get_carrier_by_title(title, session, current_user)


@router.post('/carrier', status_code=status.HTTP_201_CREATED, description='Добавление перевозчика')
def router_add_carrier(data: CarrierCreate,
                       session: Session = Depends(get_session),
                       current_user: User = Depends(require_roles(["superadmin"]))):
    return add_carrier(data, session, current_user)


@router.delete('/carrier/{carrier_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление перевозчика')
def router_delete_carrier(carrier_id: int,
                          session: Session = Depends(get_session),
                          current_user: User = Depends(require_roles(["superadmin"]))):
    return delete_carrier_by_id(carrier_id, session, current_user)


@router.put('/carrier/{carrier_id}', status_code=status.HTTP_200_OK, description='Изменение перевозчика')
def router_update_carrier(carrier_id: int,
                          data: Carrier,
                          session: Session = Depends(get_session),
                          current_user: User = Depends(require_roles(["superadmin"]))):
    return update_carrier(carrier_id, data, session, current_user)


@router.get('/carrier', description='Вывод информации о перевозчиках', response_model=Page[Carrier])
def router_show_carrier(session: Session = Depends(get_session),
                        page: int = 1,
                        size: int = 10,
                        current_user: User = Depends(require_roles(["operator", "admin", "superadmin"]))):
    return show_carrier(session, page, size, current_user)
