from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.core.config import settings
from src.infrastructure.di.container import create_container
from src.infrastructure.mongodb import init_mongo
from src.presentation.api.alerts.handlers.alert_api_route_handler import AlertApiRouteHandler
from src.presentation.api.devices.handlers.device_api_route_handler import DeviceApiRouteHandler
from src.presentation.api.sensor_events.handlers.sensor_event_api_route_handler import (
    SensorEventApiRouteHandler,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    client = await init_mongo()
    yield
    client.close()


app = FastAPI(
    title='DDD iot monitoring API',
    description='A RESTful API for iot monitoring using Domain-Driven Design principles.',
    version='1.0.0',
    lifespan=lifespan,
)

container = create_container()
setup_dishka(container=container, app=app)

# Routers
device_route_handler = DeviceApiRouteHandler()
device_route_handler.register_routes(app)

alert_route_handler = AlertApiRouteHandler()
alert_route_handler.register_routes(app)

sensor_event_route_handler = SensorEventApiRouteHandler()
sensor_event_route_handler.register_routes(app)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HTTP_HOST, port=settings.HTTP_PORT, reload=True)
