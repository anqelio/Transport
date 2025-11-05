from fastapi import Depends, status, APIRouter
from sqlmodel import Session
from app.controllers.employees_controller import *
from app.db.session import get_session
from app.models.employees import Employee

router = APIRouter()


@router.get('/employee/{employee_id}', description='Поиск сотрудника по ID')
def router_get_employee_by_id(employee_id: int, session: Session = Depends(get_session)):
    return get_employee_by_id(employee_id, session)


@router.post('/employee', status_code=status.HTTP_201_CREATED, description='Добавление сотрудника')
def router_add_employee(data: Employee, session: Session = Depends(get_session)):
    return add_employee(data, session)


@router.delete('/employee/{employee_id}', status_code=status.HTTP_200_OK, description='Удаление сотрудника')
def router_delete_employee(employee_id: int, session: Session = Depends(get_session)):
    return delete_employee_by_id(employee_id, session)


@router.put('/employee/{employee_id}', status_code=status.HTTP_200_OK, description='Изменение сотрудника')
def router_update_employee(employee_id: int, data: Employee, session: Session = Depends(get_session)):
    return update_employee(employee_id, data, session)


@router.get('/employee', description='Вывод информации о сотрудниках')
def router_show_employee(session: Session = Depends(get_session)):
    return show_employee(session)