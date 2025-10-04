from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.core.config import settings
from src.infrastructure.di.container import create_container
from src.infrastructure.di.providers.mongo_providers import BeanieInitializer
from src.monitoring.middleware import PrometheusMiddleware
from src.presentation.api.alerts.handlers.alert_api_route_handler import AlertApiRouteHandler
from src.presentation.api.devices.handlers.device_api_route_handler import DeviceApiRouteHandler
from src.presentation.api.monitoring.handlers import router as monitoring_router
from src.presentation.api.sensor_events.handlers.sensor_event_api_route_handler import (
    SensorEventApiRouteHandler,
)

container = create_container()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    await container.get(BeanieInitializer)
    yield


app = FastAPI(
    title='Iot monitoring API',
    description='API for iot monitoring',
    version='1.0.0',
    lifespan=lifespan,
)

app.add_middleware(PrometheusMiddleware)

setup_dishka(container=container, app=app)

# Routers
device_route_handler = DeviceApiRouteHandler()
device_route_handler.register_routes(app)

alert_route_handler = AlertApiRouteHandler()
alert_route_handler.register_routes(app)

sensor_event_route_handler = SensorEventApiRouteHandler()
sensor_event_route_handler.register_routes(app)

app.include_router(monitoring_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HTTP_HOST, port=settings.HTTP_PORT, reload=True)
