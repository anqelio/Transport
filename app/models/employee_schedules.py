from datetime import date

from sqlmodel import SQLModel, Field


class EmployeeSchedules(SQLModel, table=True):
    id_employee_schedule: int = Field(primary_key=True)
    employee_id: int = Field(foreign_key='employee.employee_id')
    trip_id: int = Field(foreign_key='trip.trip_id')
    work_date: date
    planned_start_time: str
    planned_end_time: str