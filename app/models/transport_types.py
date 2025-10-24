from sqlmodel import SQLModel, Field


class Transport(SQLModel, table=True):
    transport_id: int = Field(primary_key=True)
    name_transport: str