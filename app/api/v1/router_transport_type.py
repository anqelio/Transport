from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.transport_type_controller import *
from app.db.session import get_session
from app.models.transport_types import Transport
from app.schemas.schemas_requests import TransportCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/transport_type/{transport_id}', description='Поиск вида транспорта по ID')
def router_get_transport_type_by_id(transport_id: int, session: Session = Depends(get_session),
                                    current_user: User = Depends(require_roles(["user", "operator", "admin", "superadmin"]))):
    return get_transport_type_by_id(transport_id, session, current_user)


@router.post('/transport_type', status_code=status.HTTP_201_CREATED, description='Добавление вида транспорта')
def router_add_transport_type(data: TransportCreate, session: Session = Depends(get_session),
                              current_user: User = Depends(require_roles(["admin", "superadmin"]))):
    return add_transport_type(data, session, current_user)


@router.delete('/transport_type/{transport_id}', status_code=status.HTTP_204_NO_CONTENT,
               description='Удаление вида транспорта')
def router_delete_transport_type(transport_id: int, session: Session = Depends(get_session),
                                 current_user: User = Depends(require_roles(["admin", "superadmin"]))):
    return delete_transport_type_id(transport_id, session, current_user)


@router.put('/transport_type/{transport_id}', status_code=status.HTTP_200_OK, description='Изменение вида транспорта')
def router_update_transport_type(transport_id: int, data: Transport, session: Session = Depends(get_session),
                                 current_user: User = Depends(require_roles(["admin", "superadmin"]))):
    return update_transport_type(transport_id, data, session, current_user)


@router.get('/transport_type', description='Вывод информации о видах транспорта', response_model=Page[Transport])
def router_show_transport_type(session: Session = Depends(get_session), page: int = 1, size: int = 10,
                               current_user: User = Depends(require_roles(["user", "operator", "admin", "superadmin"]))):
    return show_transport_type(session, page, size, current_user)
