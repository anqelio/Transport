from datetime import date
from sqlmodel import SQLModel, Field


class Trip(SQLModel, table=True):
    trip_id: int = Field(primary_key=True)
    schedule_id: int = Field(foreign_key='schedule.schedule_id')
    planned_departure_time: str
    actual_departure_time: str
    trip_date: date
    vehicle_info: str
    driver_id: int = Field(foreign_key='employee.employee_id')
    conductor_id: int = Field(foreign_key='employee.employee_id')
