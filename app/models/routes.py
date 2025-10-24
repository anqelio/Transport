from sqlmodel import SQLModel, Field


class Routes(SQLModel, table=True):
    route_id: int = Field(primary_key=True)
    number_route: int
    start: str
    stop: str
    operating_days: str
    total_time: int
    transport_type: int = Field(foreign_key='transport.transport_id')
    carrier_id: int = Field(foreign_key='carrier.carrier_id')