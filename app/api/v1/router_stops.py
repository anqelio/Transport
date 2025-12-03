from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.stops_controller import *
from app.db.session import get_session
from app.models.stops import Stop
from app.schemas.schemas_requests import StopCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/stop/{title}', description='Поиск остановки по названию')
def router_get_stop_by_title(title: str, session: Session = Depends(get_session),
                          current_user: User = Depends(require_roles(["user", "operator", "admin", "superadmin"]))):
    return get_stop_by_title(title, session, current_user)


@router.post('/stop', status_code=status.HTTP_201_CREATED, description='Добавление остановки')
def router_add_stop(data: StopCreate, session: Session = Depends(get_session),
                    current_user: User = Depends(require_roles(["user", "operator", "admin", "superadmin"]))):
    return add_stop(data, session, current_user)


@router.delete('/stop/{stop_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление остановки')
def router_delete_stop(stop_id: int, session: Session = Depends(get_session),
                       current_user: User = Depends(require_roles(["user", "operator", "admin", "superadmin"]))):
    return delete_stop_by_id(stop_id, session, current_user)


@router.put('/stop/{stop_id}', status_code=status.HTTP_200_OK, description='Изменение остановки')
def router_update_stop(stop_id: int, data: Stop, session: Session = Depends(get_session),
                       current_user: User = Depends(require_roles(["user", "operator", "admin", "superadmin"]))):
    return update_stop(stop_id, data, session, current_user)


@router.get('/stop', description='Вывод информации о остановках', response_model=Page[Stop])
def router_show_stop(session: Session = Depends(get_session), page: int = 1, size: int = 10,
                     current_user: User = Depends(require_roles(["user", "operator", "admin", "superadmin"]))):
    return show_stops(session, page, size, current_user)
