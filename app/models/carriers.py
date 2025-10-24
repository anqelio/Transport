from sqlmodel import SQLModel, Field


class Carrier(SQLModel, table=True):
    carrier_id: int = Field(primary_key=True)
    name_company: str
    contact_info: str
