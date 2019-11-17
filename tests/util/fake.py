from datetime import datetime
from random import Random

from domain.models import Location, Area, AreaType, Sensor, SensorType, Reading, WeatherInfo, Activation


def fake_location():
    r = Random()
    return Location(
        longitude=str(r.randint(0, 20)),
        latitude=str(r.randint(0, 20))
    )


def fake_area(identifier):
    r = Random()
    return Area(
        identifier=identifier,
        name="Area %s" % identifier,
        location=fake_location(),
        area_type=AreaType(r.randint(1, 8))
    )


def fake_sensor(identifier):
    r = Random()
    return Sensor(
        identifier=identifier,
        location=fake_location(),
        sensor_type=SensorType.KISSING_BUG,
        area_identifier=r.randint(0, 10)
    )

def fake_reading(identifier):
    r = Random()
    return Reading(
        identifier=identifier,
        weather_info=WeatherInfo(
            wind_direction=r.random(),
            wind_velocity=r.random(),
            rainfall=r.random(),
            interior_temperature=r.random(),
            exterior_temperature=r.random(),
            humidity=r.random(),
            atmospheric_pressure=r.random()
        ),
        timestamp=datetime.now(),
        location=fake_location()
    )

def fake_activation(identifier):
    r = Random()
    return Activation(
        identifier=identifier,
        reading_identifier=r.randint(0, 20),
        activation_count=r.randint(0, 100),
        sensor_identifier=r.randint(0, 30)
    )