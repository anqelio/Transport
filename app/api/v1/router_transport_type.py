from fastapi import Depends, status, APIRouter
from sqlmodel import Session
from app.controllers.transport_type_controller import add_transport_type
from app.db.session import get_session
from app.models.transport_types import Transport

router = APIRouter()

@router.post('/add', status_code=status.HTTP_201_CREATED, description='Добавление вида транспорта')
def router_add_transport_type(data: Transport, session: Session = Depends(get_session)):
    '''
    Ручка для создания вида транпорта
    :param data:
    :param session:
    :return: add_transport_type(data, session)
    '''
    return add_transport_type(data, session)
