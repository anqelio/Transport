from fastapi import FastAPI
from app.models import *
from app.db.database import init_db
from app.api.v1.router_transport_type import router as router_transport_v1

main_app = FastAPI()
app_v1 = FastAPI(title='Transport API v1',
                 version='1.0.0',
                 openapi_url='/openapi.json',
                 docs_url='/docs',
                 redoc_url='/redoc')

main_app.mount('/api/v1/', app_v1)


@app_v1.on_event('startup')
def on_startup():
    '''
    Инициализация БД при запуске приложения
    :return: init_db()
    '''
    init_db()


app_v1.include_router(router_transport_v1, prefix="/transport", tags=['transport'])
