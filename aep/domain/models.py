from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Type


@dataclass
class Location:
    latitude: str
    longitude: str


class AreaType(Enum):
    HOUSE = 1
    LOCATION = 2
    VILLAGE = 3
    TOWN = 4
    CITY = 5
    STATE = 6
    REGION = 7
    COUNTRY = 8

    def default(self):
        return self.name


@dataclass
class Area:
    identifier: int
    name: str
    location: Location
    area_type: AreaType
    parent_area_identifier: int = None
    parent_area: Type["Area"] = None


class SensorType(Enum):
    KISSING_BUG = 1

    def default(self):
        return self.name


@dataclass
class Sensor:
    identifier: int
    location: Location
    sensor_type: SensorType
    area_identifier: int = None
    area: Area = None


@dataclass
class WeatherInfo:
    wind_direction: Decimal
    wind_velocity: Decimal
    rainfall: Decimal
    interior_temperature: Decimal
    exterior_temperature: Decimal
    humidity: Decimal
    atmospheric_pressure: Decimal


@dataclass
class Reading:
    identifier: int
    weather_info: WeatherInfo
    timestamp: datetime
    location: Location


@dataclass()
class Activation:
    identifier: int
    reading_identifier: int
    activation_count: int
    sensor_identifier: int
    sensor: Sensor = None
    reading: Reading = None
