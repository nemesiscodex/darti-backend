import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from random import Random

from aep.di import Datasources
from aep.domain.models import Reading, Activation, Location, WeatherInfo


async def generate_reading(date: datetime, location: Location, old_reading: Reading = None,
                           old_activations: [Activation] = None):
    reading_datasource = Datasources.reading()
    activation_datasource = Datasources.activation()
    r = Random()
    old_identifier = 0
    if old_reading:
        old_identifier = old_reading.identifier
    reading_identifier = old_identifier + 1
    activations = []
    reading = Reading(
        identifier=reading_identifier,
        weather_info=WeatherInfo(
            wind_direction=Decimal(r.randint(0, 360)),
            wind_velocity=Decimal(r.randint(20, 80)),
            rainfall=Decimal(r.randrange(1, 1000, 1)/ 100),
            interior_temperature=Decimal(r.randrange(1700, 4300, 1)/100),
            exterior_temperature=Decimal(r.randrange(1700, 4300, 1)/100),
            humidity=Decimal(r.randrange(0, 100, 1)),
            atmospheric_pressure=Decimal(r.randrange(99000, 102000, 1)/100)
        ),
        location=location,
        timestamp=date
    )

    await reading_datasource.create(reading)

    for i in range(32):
        current_count = 0
        if old_activations and len(old_activations) >= i + 1:
            current_count = old_activations[i].activation_count

        current_count = (current_count + r.randint(0, 255)) % 255
        activation = Activation(
            identifier=-1,
            reading_identifier=reading_identifier,
            activation_count=current_count,
            sensor_identifier=i
        )
        await activation_datasource.create(activation),
        activations.append(activation)
    return reading, activations


def generate_readings(amount: int, start_date: datetime):
    _loop = asyncio.get_event_loop()

    location = Location(
        latitude="-22.6074584",
        longitude="-59.8500665"
    )
    reading = None
    activations = None
    current_date = start_date
    for i in range(amount):
        if i % 100 == 0:
            print("Generated: " + str(i))
        reading, activations = _loop.run_until_complete(
            generate_reading(date=current_date, location=location, old_reading=reading, old_activations=activations))
        current_date = current_date + timedelta(days=1)
