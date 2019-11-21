from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Type

from aep.utils import snake_case


@dataclass
class Location:
    latitude: str
    longitude: str


class AreaType(Enum):
    House, Location, Village, Town, City, State, Region, Country = range(8)


@dataclass
class Area:
    identifier: int
    name: str
    location: Location
    area_type: AreaType
    parent_area_identifier: int = None
    parent_area: Type["Area"] = None


class SensorType(Enum):
    KissingBug, = range(1)


@dataclass
class Sensor:
    identifier: int
    location: Location
    sensor_type: SensorType
    area_identifier: int = None
    area: Area = None


class WeatherInfoType(Enum):
    WindDirection, WindVelocity, Rainfall, InteriorTemperature, \
        ExteriorTemperature, Humidity, AtmosphericPressure = range(7)

    def column(self):
        return snake_case(self.name)


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
