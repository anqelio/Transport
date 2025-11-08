from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.schedule_controller import *
from app.db.session import get_session
from app.models.schedules import Schedule

router = APIRouter()


@router.get('/schedule/{schedule_id}', description='Поиск расписания по ID')
def router_get_schedule_by_id(schedule_id: int, session: Session = Depends(get_session)):
    return get_schedule_by_id(schedule_id, session)


@router.post('/schedule', status_code=status.HTTP_201_CREATED, description='Добавление расписания')
def router_add_schedule(data: Schedule, session: Session = Depends(get_session)):
    return add_schedule(data, session)


@router.delete('/schedule/{schedule_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление расписания')
def router_delete_schedule(schedule_id: int, session: Session = Depends(get_session)):
    return delete_schedule_by_id(schedule_id, session)


@router.put('/schedule/{schedule_id}', status_code=status.HTTP_200_OK, description='Изменение расписания')
def router_update_schedule(schedule_id: int, data: Schedule, session: Session = Depends(get_session)):
    update_schedule(schedule_id, data, session)


@router.get('/schedule', description='Вывод расписания', response_model=Page[Schedule])
def router_show_schedule(session: Session = Depends(get_session), page: int = 1, size: int = 10):
    return show_schedules(session, page, size)
