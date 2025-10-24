from sqlmodel import SQLModel, Field


class RouteStop(SQLModel, table=True):
    route_stop_id: int = Field(primary_key=True)
    route_id: int = Field(foreign_key='routes.route_id')
    stop_id: int = Field(foreign_key='stop.stop_id')
    minutes_to_next_stop: int