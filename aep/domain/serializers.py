# Serializers
import dataclasses
import json
from datetime import datetime
from decimal import Decimal, getcontext
from enum import Enum

from aep.domain.models import Area, Location, AreaType, Sensor, SensorType, Reading, WeatherInfo, Activation


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, Enum):
            return o.name
        elif isinstance(o, Decimal):
            return format(o, '.4f')
        elif isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class EnhancedJSONDecoder(json.JSONDecoder):
    pass


# Monkey patching json
json._default_encoder = EnhancedJSONEncoder()


# deserializers
def json_to_area(json_object: dict):
    return Area(
        identifier=int(json_object.get('identifier', -1)),
        location=Location(
            latitude=json_object['location']['latitude'],
            longitude=json_object['location']['longitude']
        ),
        name=json_object['name'],
        area_type=AreaType[json_object['area_type']],
        parent_area_identifier=json_object.get('parent_area_identifier', None)
    )


def json_to_sensor(json_object: dict):
    return Sensor(
        identifier=int(json_object['identifier']),
        location=Location(
            latitude=json_object['location']['latitude'],
            longitude=json_object['location']['longitude']
        ),
        sensor_type=SensorType[json_object['sensor_type']],
        area_identifier=json_object.get('area_identifier', None)
    )


def json_to_reading(json_object: dict):
    return Reading(
        identifier=int(json_object.get('identifier', -1)),
        weather_info=WeatherInfo(
            wind_direction=Decimal(json_object['weather_info']['wind_direction']),
            wind_velocity=Decimal(json_object['weather_info']['wind_velocity']),
            rainfall=Decimal(json_object['weather_info']['rainfall']),
            interior_temperature=Decimal(json_object['weather_info']['interior_temperature']),
            exterior_temperature=Decimal(json_object['weather_info']['exterior_temperature']),
            humidity=Decimal(json_object['weather_info']['humidity']),
            atmospheric_pressure=Decimal(json_object['weather_info']['atmospheric_pressure'])
        ),
        timestamp=datetime.fromisoformat(json_object['timestamp']).replace(tzinfo=None),
        location=Location(
            latitude=json_object['location']['latitude'],
            longitude=json_object['location']['longitude']
        )
    )


def json_to_activation(json_object: dict):
    return Activation(
        identifier=int(json_object.get('identifier', -1)),
        reading_identifier=int(json_object['reading_identifier']),
        activation_count=int(json_object['activation_count']),
        sensor_identifier=int(json_object['sensor_identifier'])
    )
