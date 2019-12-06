# Serializers
import dataclasses
import json
from datetime import datetime
from decimal import Decimal, getcontext
from enum import Enum

from aep.domain.models import Area, Location, AreaType, Sensor, SensorType, Reading, WeatherInfo, Activation

import re

camel_pat = re.compile(r'([A-Z])')
under_pat = re.compile(r'_([a-z])')


def camel_to_underscore(name):
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)


def underscore_to_camel(name):
    return under_pat.sub(lambda x: x.group(1).upper(), name)

def convert_json(d: dict, convert):
    new_d = {}
    for k, v in d.items():
        new_d[convert(k)] = convert_json(v, convert) if isinstance(v, dict) else v
    return new_d


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return convert_json(dataclasses.asdict(o), underscore_to_camel)
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
        area_type=AreaType[json_object['areaType']],
        parent_area_identifier=json_object.get('parentAreaIdentifier', None)
    )


def json_to_sensor(json_object: dict):
    area_identifier = json_object.get('areaIdentifier', None)
    if not area_identifier:
        area_identifier = None
    return Sensor(
        identifier=int(json_object['identifier']),
        location=Location(
            latitude=json_object['location']['latitude'],
            longitude=json_object['location']['longitude']
        ),
        sensor_type=SensorType[json_object['sensorType']],
        area_identifier=area_identifier
    )


def json_to_reading(json_object: dict):
    return Reading(
        identifier=int(json_object.get('identifier', -1)),
        weather_info=WeatherInfo(
            wind_direction=Decimal(json_object['weatherInfo']['windDirection']),
            wind_velocity=Decimal(json_object['weatherInfo']['windVelocity']),
            rainfall=Decimal(json_object['weatherInfo']['rainfall']),
            interior_temperature=Decimal(json_object['weatherInfo']['interiorTemperature']),
            exterior_temperature=Decimal(json_object['weatherInfo']['exteriorTemperature']),
            humidity=Decimal(json_object['weatherInfo']['humidity']),
            atmospheric_pressure=Decimal(json_object['weatherInfo']['atmosphericPressure'])
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
        reading_identifier=int(json_object['readingIdentifier']),
        activation_count=int(json_object['activationCount']),
        sensor_identifier=int(json_object['sensorIdentifier'])
    )
