import re
from datetime import date
from typing import Optional, List

from pydantic import BaseModel, field_validator
from sqlmodel import Field

from app.models.users import User

MAX_STRING_LENGTH = 255
MAX_TEXT_LENGTH = 500
TIME_REGEX = re.compile(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$')


class UserCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=MAX_STRING_LENGTH)
    password: str = Field(..., min_length=6, max_length=MAX_STRING_LENGTH)
    role: Optional[str] = "user"
    carrier_id: Optional[int] = None
    group_id: Optional[int] = None


class UserLogin(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    username: Optional[str] = None


class TripCreate(BaseModel):
    schedule_id: int = Field(..., gt=0)
    planned_departure_time: str
    actual_departure_time: str
    trip_date: date
    vehicle_info: str = Field(..., max_length=MAX_STRING_LENGTH)
    driver_id: int = Field(..., gt=0)
    conductor_id: int = Field(..., gt=0)

    @field_validator('planned_departure_time', 'actual_departure_time')
    def validate_time_format(cls, v):
        if not TIME_REGEX.match(v):
            raise ValueError('Время должно быть указано в формате ЧЧ:ММ')
        return v


class TransportCreate(BaseModel):
    name_transport: str = Field(..., max_length=MAX_STRING_LENGTH)


class StopCreate(BaseModel):
    name_stop: str = Field(..., max_length=MAX_STRING_LENGTH)
    latitude: str = Field(..., regex=r'^-?([0-8]?[0-9]|90)(\.[0-9]{1,6})?$')
    longitude: str = Field(..., regex=r'^-?((1[0-7][0-9]|[0-9]?[0-9])(\.[0-9]{1,6})?|180)$')
    has_pavilion: bool


class ScheduleCreate(BaseModel):
    route_id: int = Field(..., gt=0)
    departure_time: str
    is_weekend: bool

    @field_validator('departure_time')
    def validate_time_format(cls, v):
        if not TIME_REGEX.match(v):
            raise ValueError('Время должно быть указано в формате ЧЧ:ММ')
        return v


class ScheduleChangesCreate(BaseModel):
    trip_id: int = Field(..., gt=0)
    reason: str = Field(..., max_length=MAX_TEXT_LENGTH)
    date_trip: date
    old_time_trip: str
    time_new_trip: str

    @field_validator('old_time_trip', 'time_new_trip')
    def validate_time_format(cls, v):
        if not TIME_REGEX.match(v):
            raise ValueError('Время должно быть указано в формате ЧЧ:ММ')
        return v


class RoutesCreate(BaseModel):
    number_route: int = Field(..., gt=0)
    start: str = Field(..., max_length=MAX_STRING_LENGTH)
    stop: str = Field(..., max_length=MAX_STRING_LENGTH)
    operating_days: str = Field(..., max_length=100)
    total_time: int = Field(..., gt=0)
    transport_type: int = Field(..., gt=0)
    carrier_id: int = Field(..., gt=0)


class RouteStopCreate(BaseModel):
    route_id: int = Field(..., gt=0)
    stop_id: int = Field(..., gt=0)
    minutes_to_next_stop: int = Field(..., ge=0)


class EmployeeCreate(BaseModel):
    position: str = Field(..., max_length=MAX_STRING_LENGTH)
    carrier_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=MAX_STRING_LENGTH)
    surname: str = Field(..., max_length=MAX_STRING_LENGTH)


class EmployeeSchedulesCreate(BaseModel):
    employee_id: int = Field(..., gt=0)
    trip_id: int = Field(..., gt=0)
    work_date: date
    planned_start_time: str
    planned_end_time: str

    @field_validator('planned_start_time', 'planned_end_time')
    def validate_time_format(cls, v):
        if not TIME_REGEX.match(v):
            raise ValueError('Время должно быть указано в формате ЧЧ:ММ')
        return v


class CarrierCreate(BaseModel):
    name_company: str = Field(..., max_length=MAX_STRING_LENGTH)
    contact_info: str = Field(..., max_length=MAX_TEXT_LENGTH)


class GroupCreate(BaseModel):
    name: str = Field(..., max_length=MAX_STRING_LENGTH)
    description: Optional[str] = Field(..., max_length=MAX_TEXT_LENGTH)
    users: List[User]
