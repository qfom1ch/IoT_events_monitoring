from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import httpx
import pytest
import pytest_asyncio
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import test_settings
from src.infrastructure.di.container import create_container_test
from src.infrastructure.di.providers.mongo_providers import BeanieInitializer
from src.monitoring.middleware import PrometheusMiddleware
from src.presentation.api.alerts.handlers.alert_api_route_handler import AlertApiRouteHandler
from src.presentation.api.devices.handlers.device_api_route_handler import DeviceApiRouteHandler
from src.presentation.api.monitoring.handlers import router as monitoring_router
from src.presentation.api.sensor_events.handlers.sensor_event_api_route_handler import (
    SensorEventApiRouteHandler,
)


@pytest.fixture
def test_app():
    container = create_container_test()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
        await container.get(BeanieInitializer)
        yield

    app = FastAPI(title='DDD iot monitoring API - Test', lifespan=lifespan)

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

    return app


@pytest_asyncio.fixture
async def async_client(test_app) -> AsyncGenerator[httpx.AsyncClient, Any]:
    await test_app.state.dishka_container.get(BeanieInitializer)

    client = await test_app.state.dishka_container.get(AsyncIOMotorClient)
    db = client[test_settings.DATABASE_NAME]

    collection_names = await db.list_collection_names()
    for collection_name in collection_names:
        await db[collection_name].delete_many({})

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url='http://test'
    ) as client:
        yield client
