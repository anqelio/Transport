from sqlmodel import SQLModel, Field


class Transport(SQLModel, table=True):
    transport_id: int = Field(default=None, primary_key=True)
    name_transport: str
