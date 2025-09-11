from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    'app_http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'app_http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge('app_active_connections', 'Number of active connections')

SENSOR_EVENTS_PROCESSED = Counter(
    'app_sensor_events_processed_total', 'Total sensor events processed'
)

ALERTS_GENERATED = Counter('app_alerts_generated_total', 'Total alerts generated')
