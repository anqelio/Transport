from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.employees_controller import *
from app.db.session import get_session
from app.models.employees import Employee
from app.schemas.schemas_requests import EmployeeCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/employee/{position}', description='Поиск сотрудника по позиции')
def router_get_employee_by_position(position: str, session: Session = Depends(get_session),
                              current_user: User = Depends(require_roles(["operator", "admin", "superadmin"]))):
    return get_employee_by_position(position, session, current_user)


@router.post('/employee', status_code=status.HTTP_201_CREATED, description='Добавление сотрудника')
def router_add_employee(data: EmployeeCreate, session: Session = Depends(get_session),
                        current_user: User = Depends(require_roles(["operator", "superadmin"]))):
    return add_employee(data, session, current_user)


@router.delete('/employee/{employee_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление сотрудника')
def router_delete_employee(employee_id: int, session: Session = Depends(get_session),
                           current_user: User = Depends(require_roles(["operator", "superadmin"]))):
    return delete_employee_by_id(employee_id, session, current_user)


@router.put('/employee/{employee_id}', status_code=status.HTTP_200_OK, description='Изменение сотрудника')
def router_update_employee(employee_id: int, data: Employee, session: Session = Depends(get_session),
                           current_user: User = Depends(require_roles(["operator", "superadmin"]))):
    return update_employee(employee_id, data, session, current_user)


@router.get('/employee', description='Вывод информации о сотрудниках', response_model=Page[Employee])
def router_show_employee(session: Session = Depends(get_session), page: int = 1, size: int = 10,
                         current_user: User = Depends(require_roles(["operator", "superadmin"]))):
    return show_employee(session, page, size, current_user)
