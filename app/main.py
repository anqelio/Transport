from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.openapi.utils import get_openapi
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
from app.api.v1.router_employee_schedules import router as router_employee_schedule_v1
from app.api.v1.router_users_controller import router as router_user_v1
from app.api.v1.router_group import router as router_group_v1
from app.api.v1.router_auth import router as router_auth_v1

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

def custom_openapi():
    if app_v1.openapi_schema:
        return app_v1.openapi_schema

    openapi_schema = get_openapi(
        title="Transport API v1",
        version="1.0.0",
        description="API для системы управления городским транспортом",
        routes=app_v1.routes,
    )

    # Добавляем Bearer аутентификацию для Swagger
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Введите токен в формате: Bearer <ваш_токен>"
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            # Пропускаем эндпоинты аутентификации
            if "auth" not in path:
                if "security" not in openapi_schema["paths"][path][method]:
                    openapi_schema["paths"][path][method]["security"] = []
                openapi_schema["paths"][path][method]["security"].append({"BearerAuth": []})

    app_v1.openapi_schema = openapi_schema
    return app_v1.openapi_schema

app_v1 = FastAPI(
    title='Transport API v1',
    version='1.0.0',
    openapi_url='/openapi.json',
    docs_url='/docs',
    redoc_url='/redoc',
    lifespan=on_startup,
    swagger_ui_parameters={
        "persistAuthorization": True,  # Сохраняет авторизацию при перезагрузке
        "displayRequestDuration": True
    }
)

# Кастомная OpenAPI схема
app_v1.openapi = custom_openapi

main_app.mount('/api/v1/', app_v1)

# Подключаем все роутеры
app_v1.include_router(router_transport_v1, tags=['Transport'])
app_v1.include_router(router_stops_v1, tags=['Stop'])
app_v1.include_router(router_route_v1, tags=['Routes'])
app_v1.include_router(router_carrier_v1, tags=['Carrier'])
app_v1.include_router(router_schedule_v1, tags=['Schedule'])
app_v1.include_router(router_employee_v1, tags=['Employee'])
app_v1.include_router(router_route_stop_v1, tags=['RouteStop'])
app_v1.include_router(router_trip_v1, tags=['Trip'])
app_v1.include_router(router_schedule_changes_v1, tags=['ScheduleChanges'])
app_v1.include_router(router_employee_schedule_v1, tags=['EmployeeSchedules'])
app_v1.include_router(router_user_v1, tags=['User'])
app_v1.include_router(router_group_v1, tags=['Group'])
app_v1.include_router(router_auth_v1, prefix="/auth", tags=['Auth'])

add_pagination(app_v1)