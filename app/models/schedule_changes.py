from datetime import date
from sqlmodel import SQLModel, Field


class ScheduleChanges(SQLModel, table=True):
    change_id: int = Field(primary_key=True)
    trip_id: int = Field(foreign_key='trip.trip_id')
    reason: str
    date_trip: date
    old_time_trip: str
    time_new_trip: str