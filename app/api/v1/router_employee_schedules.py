from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.employee_schedules_controller import *
from app.db.session import get_session
from app.models.employee_schedules import EmployeeSchedules
from app.schemas.schemas_requests import EmployeeSchedulesCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/employee_schedule/{employee_schedule_id}', description='Поиск графика рабочих по ID')
def router_get_employee_by_id(employee_schedule_id: int, session: Session = Depends(get_session),
                              current_user: User = Depends(require_roles(["operator", "admin", "superadmin"]))):
    return get_employee_schedule_by_id(employee_schedule_id, session, current_user)


@router.post('/employee_schedule', status_code=status.HTTP_201_CREATED, description='Добавление графика рабочих')
def router_add_employee(data: EmployeeSchedulesCreate, session: Session = Depends(get_session),
                        current_user: User = Depends(require_roles(["operator", "superadmin"]))):
    return add_employee_schedule(data, session, current_user)


@router.delete('/employee_schedule/{employee_schedule_id}', status_code=status.HTTP_204_NO_CONTENT,
               description='Удаление графика рабочих')
def router_delete_employee(employee_schedule_id: int, session: Session = Depends(get_session),
                           current_user: User = Depends(require_roles(["operator", "superadmin"]))):
    return delete_employee_schedule_by_id(employee_schedule_id, session, current_user)


@router.put('/employee_schedule/{employee_schedule_id}', status_code=status.HTTP_200_OK,
            description='Изменение графика рабочих')
def router_update_employee(employee_schedule_id: int, data: EmployeeSchedules, session: Session = Depends(get_session),
                           current_user: User = Depends(require_roles(["operator", "superadmin"]))):
    return update_employee_schedule(employee_schedule_id, data, session, current_user)


@router.get('/employee_schedule', description='Вывод графика рабочих', response_model=Page[EmployeeSchedules])
def router_show_employee(session: Session = Depends(get_session), page: int = 1, size: int = 10,
                         current_user: User = Depends(require_roles(["operator", "admin", "superadmin"]))):
    return show_employee_schedule(session, page, size, current_user)
