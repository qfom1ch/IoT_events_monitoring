import os

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = os.environ.get('PROJECT_NAME', 'UNNAMED PROJECT')
    API_V1_STR: str = '/api/v1'
    HTTP_HOST: str = '0.0.0.0'
    HTTP_PORT: int = 8000
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    DEBUG: bool = os.environ.get('DEBUG', 'False')

    @field_validator('BACKEND_CORS_ORIGINS')
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_NAME: str = os.environ.get('DATABASE_NAME')
    MONGO_URI: str = os.environ.get('MONGO_URI')

    ELASTICSEARCH_HOSTS: str | None = os.environ.get('ELASTICSEARCH_HOSTS')

    KAFKA_BOOTSTRAP_SERVERS: str = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC_SENSOR_EVENTS: str = os.environ.get(
        'KAFKA_TOPIC_SENSOR_EVENTS', 'sensor_events'
    )
    KAFKA_GROUP_ID: str = os.environ.get('KAFKA_GROUP_ID', 'sensor-event-group')

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, extra='ignore')


settings = Settings()
