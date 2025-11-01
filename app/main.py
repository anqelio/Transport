from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.models import *
from app.db.database import *
from app.api.v1.router_transport_type import router as router_transport_v1
from app.api.v1.router_stops import router as router_stops_v1
from app.api.v1.router_routes import router as router_route_v1

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


app_v1.include_router(router_transport_v1, prefix="/transports", tags=['transports'])
app_v1.include_router(router_stops_v1, prefix="/stops", tags=['stops'])
app_v1.include_router(router_route_v1, prefix="/routes", tags=['routes'])