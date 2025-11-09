from typing import Optional
from sqlalchemy.orm import Relationship
from sqlmodel import SQLModel, Field
from app.models.groups import *
from app.models.roles import RoleEnum


class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    login: str
    password: str
    hashed_password: str
    role: RoleEnum = Field(default=RoleEnum.USER)
    carrier_id: Optional[int] = Field(default=None, foreign_key='carrier.carrier_id')
    group_id: Optional[int] = Field(default=None, foreign_key="usergroup.group_id")
    group: Optional['UserGroup'] = Relationship(back_populates="users")