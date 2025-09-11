import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.monitoring.metrics import REQUEST_COUNT, REQUEST_DURATION


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        REQUEST_COUNT.labels(
            method=request.method, endpoint=request.url.path, status=response.status_code
        ).inc()

        REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(
            time.time() - start_time
        )

        return response
