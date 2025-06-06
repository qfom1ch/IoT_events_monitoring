from enum import Enum


class SensorType(str, Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    PRESSURE = 'pressure'
