import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator
from sqlmodel import Field

MAX_STRING_LENGTH = 255
MAX_TEXT_LENGTH = 500
TIME_REGEX = re.compile(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$')


class UserCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=MAX_STRING_LENGTH)
    password: str = Field(..., min_length=6, max_length=MAX_STRING_LENGTH)


class UserUpdate(BaseModel):
    login: Optional[str] = Field(None, min_length=3, max_length=MAX_STRING_LENGTH)
    password: Optional[str] = Field(None, min_length=6, max_length=MAX_STRING_LENGTH)


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


class TripUpdate(BaseModel):
    schedule_id: Optional[int] = Field(None, gt=0)
    planned_departure_time: Optional[str] = None
    actual_departure_time: Optional[str] = None
    trip_date: Optional[date] = None
    vehicle_info: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)
    driver_id: Optional[int] = Field(None, gt=0)
    conductor_id: Optional[int] = Field(None, gt=0)

    @field_validator('planned_departure_time', 'actual_departure_time')
    def validate_time_format(cls, v):
        if v is not None and not TIME_REGEX.match(v):
            raise ValueError('Время должно быть указано в формате ЧЧ:ММ')
        return v


class TransportCreate(BaseModel):
    name_transport: str = Field(..., max_length=MAX_STRING_LENGTH)


class TransportUpdate(BaseModel):
    name_transport: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)


class StopCreate(BaseModel):
    name_stop: str = Field(..., max_length=MAX_STRING_LENGTH)
    latitude: str = Field(..., regex=r'^-?([0-8]?[0-9]|90)(\.[0-9]{1,6})?$')
    longitude: str = Field(..., regex=r'^-?((1[0-7][0-9]|[0-9]?[0-9])(\.[0-9]{1,6})?|180)$')
    has_pavilion: bool


class StopUpdate(BaseModel):
    name_stop: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)
    latitude: Optional[str] = Field(None, regex=r'^-?([0-8]?[0-9]|90)(\.[0-9]{1,6})?$')
    longitude: Optional[str] = Field(None, regex=r'^-?((1[0-7][0-9]|[0-9]?[0-9])(\.[0-9]{1,6})?|180)$')
    has_pavilion: Optional[bool] = None


class ScheduleCreate(BaseModel):
    route_id: int = Field(..., gt=0)
    departure_time: str
    is_weekend: bool

    @field_validator('departure_time')
    def validate_time_format(cls, v):
        if not TIME_REGEX.match(v):
            raise ValueError('Время должно быть указано в формате ЧЧ:ММ')
        return v


class ScheduleUpdate(BaseModel):
    route_id: Optional[int] = Field(None, gt=0)
    departure_time: Optional[str] = None
    is_weekend: Optional[bool] = None

    @field_validator('departure_time')
    def validate_time_format(cls, v):
        if v is not None and not TIME_REGEX.match(v):
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


class ScheduleChangesUpdate(BaseModel):
    trip_id: Optional[int] = Field(None, gt=0)
    reason: Optional[str] = Field(None, max_length=MAX_TEXT_LENGTH)
    date_trip: Optional[date] = None
    old_time_trip: Optional[str] = None
    time_new_trip: Optional[str] = None

    @field_validator('old_time_trip', 'time_new_trip')
    def validate_time_format(cls, v):
        if v is not None and not TIME_REGEX.match(v):
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


class RoutesUpdate(BaseModel):
    number_route: Optional[int] = Field(None, gt=0)
    start: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)
    stop: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)
    operating_days: Optional[str] = Field(None, max_length=100)
    total_time: Optional[int] = Field(None, gt=0)
    transport_type: Optional[int] = Field(None, gt=0)
    carrier_id: Optional[int] = Field(None, gt=0)


class RouteStopCreate(BaseModel):
    route_id: int = Field(..., gt=0)
    stop_id: int = Field(..., gt=0)
    minutes_to_next_stop: int = Field(..., ge=0)


class RouteStopUpdate(BaseModel):
    route_id: Optional[int] = Field(None, gt=0)
    stop_id: Optional[int] = Field(None, gt=0)
    minutes_to_next_stop: Optional[int] = Field(None, ge=0)


class EmployeeCreate(BaseModel):
    position: str = Field(..., max_length=MAX_STRING_LENGTH)
    carrier_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=MAX_STRING_LENGTH)
    surname: str = Field(..., max_length=MAX_STRING_LENGTH)


class EmployeeUpdate(BaseModel):
    position: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)
    carrier_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)
    surname: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)


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


class EmployeeSchedulesUpdate(BaseModel):
    employee_id: Optional[int] = Field(None, gt=0)
    trip_id: Optional[int] = Field(None, gt=0)
    work_date: Optional[date] = None
    planned_start_time: Optional[str] = None
    planned_end_time: Optional[str] = None

    @field_validator('planned_start_time', 'planned_end_time')
    def validate_time_format(cls, v):
        if v is not None and not TIME_REGEX.match(v):
            raise ValueError('Время должно быть указано в формате ЧЧ:ММ')
        return v


class CarrierCreate(BaseModel):
    name_company: str = Field(..., max_length=MAX_STRING_LENGTH)
    contact_info: str = Field(..., max_length=MAX_TEXT_LENGTH)


class CarrierUpdate(BaseModel):
    name_company: Optional[str] = Field(None, max_length=MAX_STRING_LENGTH)
    contact_info: Optional[str] = Field(None, max_length=MAX_TEXT_LENGTH)
