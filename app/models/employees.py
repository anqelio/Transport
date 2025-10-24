from sqlmodel import SQLModel, Field


class Employee(SQLModel, table=True):
    employee_id: int = Field(primary_key=True)
    position: str
    carrier_id: int = Field(foreign_key='carrier.carrier_id')
    name: str
    surname: str