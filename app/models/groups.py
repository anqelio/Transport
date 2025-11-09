from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.users import User


class UserGroup(SQLModel, table=True):
    group_id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None
    users: List[User] = Relationship(back_populates="group")