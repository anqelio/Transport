from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.schedule_changes_controller import *
from app.db.session import get_session
from app.models.schedule_changes import ScheduleChanges
from app.schemas.schemas_requests import ScheduleChangesCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/schedule_change/{schedule_change_id}', description='Поиск изменений расписания по ID')
def router_get_schedule_change_by_id(schedule_change_id: int, session: Session = Depends(get_session),
                                     current_user: User = Depends(require_roles(["user", "admin", "superadmin"]))):
    return get_schedule_changes_by_id(schedule_change_id, session, current_user)


@router.post('/schedule_change', status_code=status.HTTP_201_CREATED, description='Добавление изменений расписания')
def router_add_schedule_change(data: ScheduleChangesCreate, session: Session = Depends(get_session),
                               current_user: User = Depends(require_roles(["user", "operator", "superadmin"]))):
    return add_schedule_changes(data, session, current_user)


@router.delete('/schedule_change/{schedule_change_id}', status_code=status.HTTP_204_NO_CONTENT,
               description='Удаление изменений расписания')
def router_delete_schedule_change(schedule_change_id: int, session: Session = Depends(get_session),
                                  current_user: User = Depends(require_roles(["user", "operator", "superadmin"]))):
    return delete_schedule_changes_by_id(schedule_change_id, session, current_user)


@router.put('/schedule_change/{schedule_change_id}', status_code=status.HTTP_200_OK,
            description='Изменение изменений расписания')
def router_update_schedule_change(schedule_change_id: int, data: ScheduleChanges,
                                  session: Session = Depends(get_session),
                                  current_user: User = Depends(require_roles(["user", "operator", "superadmin"]))):
    return update_schedule_changes(schedule_change_id, data, session, current_user)


@router.get('/schedule_change', description='Вывод изменений расписания', response_model=Page[ScheduleChanges])
def router_show_schedule_change(session: Session = Depends(get_session), page: int = 1, size: int = 10,
                                current_user: User = Depends(require_roles(["user", "admin", "superadmin"]))):
    return show_schedule_changes(session, page, size, current_user)
