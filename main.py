from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI

from src.core.config import settings
from src.infrastructure.mongodb import init_mongo
from src.infrastructure.mongodb.database import close_db_connection, connect_and_init_db
from src.presentation.api.alerts.handlers.alert_api_route_handler import AlertApiRouteHandler
from src.presentation.api.devices.handlers.device_api_route_handler import DeviceApiRouteHandler
from src.presentation.api.sensor_events.handlers.sensor_event_api_route_handler import (
    SensorEventApiRouteHandler,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    await connect_and_init_db()
    await init_mongo()
    yield
    await close_db_connection()


app = FastAPI(
    title='DDD iot monitoring API',
    description='A RESTful API for iot monitoring using Domain-Driven Design principles.',
    version='1.0.0',
    lifespan=lifespan,
)

device_route_handler = DeviceApiRouteHandler()
device_route_handler.register_routes(app)

alert_route_handler = AlertApiRouteHandler()
alert_route_handler.register_routes(app)

sensor_event_route_handler = SensorEventApiRouteHandler()
sensor_event_route_handler.register_routes(app)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HTTP_HOST, port=settings.HTTP_PORT, reload=True)
