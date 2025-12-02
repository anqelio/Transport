from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.schedule_controller import *
from app.db.session import get_session
from app.models.schedules import Schedule
from app.schemas.schemas_requests import ScheduleCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/schedule/{schedule_id}', description='Поиск расписания по ID')
def router_get_schedule_by_id(schedule_id: int, session: Session = Depends(get_session),
                              current_user: User = Depends(require_roles(["user", "admin", "superadmin"]))):
    return get_schedule_by_id(schedule_id, session, current_user)


@router.post('/schedule', status_code=status.HTTP_201_CREATED, description='Добавление расписания')
def router_add_schedule(data: ScheduleCreate, session: Session = Depends(get_session),
                        current_user: User = Depends(require_roles(["user", "operator", "superadmin"]))):
    return add_schedule(data, session, current_user)


@router.delete('/schedule/{schedule_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление расписания')
def router_delete_schedule(schedule_id: int, session: Session = Depends(get_session),
                           current_user: User = Depends(require_roles(["user", "operator", "superadmin"]))):
    return delete_schedule_by_id(schedule_id, session, current_user)


@router.put('/schedule/{schedule_id}', status_code=status.HTTP_200_OK, description='Изменение расписания')
def router_update_schedule(schedule_id: int, data: Schedule, session: Session = Depends(get_session),
                           current_user: User = Depends(require_roles(["user", "operator", "superadmin"]))):
    update_schedule(schedule_id, data, session, current_user)


@router.get('/schedule', description='Вывод расписания', response_model=Page[Schedule])
def router_show_schedule(session: Session = Depends(get_session), page: int = 1, size: int = 10,
                         current_user: User = Depends(require_roles(["user", "admin", "superadmin"]))):
    return show_schedules(session, page, size, current_user)
