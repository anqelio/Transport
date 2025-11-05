from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.models import *
from app.db.database import *
from app.api.v1.router_transport_type import router as router_transport_v1
from app.api.v1.router_stops import router as router_stops_v1
from app.api.v1.router_routes import router as router_route_v1
from app.api.v1.router_carriers import router as router_carrier_v1
from app.api.v1.router_schedule import router as router_schedule_v1
from app.api.v1.router_employee import router as router_employee_v1
from app.api.v1.router_route_stops import router as router_route_stop_v1
from app.api.v1.router_trip import router as router_trip_v1
from app.api.v1.router_schedule_changes import router as router_schedule_changes_v1

main_app = FastAPI()
@asynccontextmanager
async def on_startup(app: FastAPI):
    '''
    Инициализация БД при запуске приложения
    :params: app: FastAPI
    :return: init_db()
    '''
    init_db()
    yield
    close_db()

app_v1 = FastAPI(title='Transport API v1',
                 version='1.0.0',
                 openapi_url='/openapi.json',
                 docs_url='/docs',
                 redoc_url='/redoc',
                 lifespan=on_startup)

main_app.mount('/api/v1/', app_v1)


app_v1.include_router(router_transport_v1, tags=['transport'])
app_v1.include_router(router_stops_v1, tags=['stop'])
app_v1.include_router(router_route_v1, tags=['route'])
app_v1.include_router(router_carrier_v1, tags=['carrier'])
app_v1.include_router(router_schedule_v1, tags=['schedule'])
app_v1.include_router(router_employee_v1, tags=['employee'])
app_v1.include_router(router_route_stop_v1, tags=['route_stop'])
app_v1.include_router(router_trip_v1, tags=['trip'])
app_v1.include_router(router_schedule_changes_v1, tags=['schedule_changes'])
