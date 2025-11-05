from sqlmodel import SQLModel, Field


class Schedule(SQLModel, table=True):
    schedule_id: int = Field(primary_key=True)
    route_id: int = Field(foreign_key='routes.route_id')
    departure_time: str
    is_weekend: bool