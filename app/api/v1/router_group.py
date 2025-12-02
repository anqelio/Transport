from fastapi import Depends, status, APIRouter
from fastapi_pagination import Page
from sqlmodel import Session
from app.controllers.groups_controller import *
from app.db.session import get_session
from app.models.groups import UserGroup
from app.schemas.schemas_requests import GroupCreate
from app.security.auth_deps import require_roles

router = APIRouter()


@router.get('/group/{group_id}', description='Поиск групп рабочих по ID')
def router_get_group_by_id(group_id: int, session: Session = Depends(get_session),
                           current_user: User = Depends(require_roles(["admin", "superadmin"]))):
    return get_group_by_id(group_id, session, current_user)


@router.post('/group', status_code=status.HTTP_201_CREATED, description='Добавление групп')
def router_add_group(data: GroupCreate, session: Session = Depends(get_session),
                     current_user: User = Depends(require_roles(["superadmin"]))):
    return add_group(data, session, current_user)


@router.delete('/group/{group_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление групп')
def router_delete_group(group_id: int, session: Session = Depends(get_session),
                        current_user: User = Depends(require_roles(["superadmin"]))):
    return delete_group_by_id(group_id, session, current_user)


@router.put('/group/{group_id}', status_code=status.HTTP_200_OK, description='Изменение групп')
def router_update_group(group_id: int, data: UserGroup, session: Session = Depends(get_session),
                        current_user: User = Depends(require_roles(["superadmin"]))):
    return update_group(group_id, data, session, current_user)


@router.get('/group', description='Вывод групп', response_model=Page[UserGroup])
def router_show_group(session: Session = Depends(get_session), page: int = 1, size: int = 10,
                      current_user: User = Depends(require_roles(["superadmin"]))):
    return show_group(session, page, size, current_user)
