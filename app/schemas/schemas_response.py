from datetime import date
from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    login: str
    password: str
    role: str
    carrier_id: int
    group_id: int

class UserLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int

class Trip(BaseModel):
    trip_id: int
    schedule_id: int
    planned_departure_time: str
    actual_departure_time: str
    trip_date: date
    vehicle_info: str
    driver_id: int
    conductor_id: int

class Transport(BaseModel):
    transport_id: int
    name_transport: str

class Stop(BaseModel):
    stop_id: int
    name_stop: str
    latitude: str
    longitude: str
    has_pavilion: bool

class Schedule(BaseModel):
    schedule_id: int
    route_id: int
    departure_time: str
    is_weekend: bool

class ScheduleChanges(BaseModel):
    change_id: int
    trip_id: int
    reason: str
    date_trip: date
    old_time_trip: str
    time_new_trip: str

class Routes(BaseModel):
    route_id: int
    number_route: int
    start: str
    stop: str
    operating_days: str
    total_time: int
    transport_type: int
    carrier_id: int

class RouteStop(BaseModel):
    route_stop_id: int
    route_id: int
    stop_id: int
    minutes_to_next_stop: int

class Employee(BaseModel):
    employee_id: int
    position: str
    carrier_id: int
    name: str
    surname: str

class EmployeeSchedules(BaseModel):
    id_employee_schedule: int
    employee_id: int
    trip_id: int
    work_date: date
    planned_start_time: str
    planned_end_time: str

class Carrier(BaseModel):
    carrier_id: int
    name_company: str
    contact_info: str

class GroupCreate(BaseModel):
    name: str
    description: str
    users: str