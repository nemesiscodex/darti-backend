from datetime import datetime

from asyncpg import Record

import aep.data.db.postgres as db
from aep.domain.models import Area, Location, AreaType, Sensor, SensorType, Reading, WeatherInfo, Activation, \
    WeatherInfoType


def record_to_location(record: Record):
    return Location(
        latitude=record['latitude'],
        longitude=record['longitude']
    )


def record_to_area(record: Record):
    return Area(
        identifier=record['identifier'],
        name=record['name'],
        location=record_to_location(record),
        area_type=AreaType[record['area_type']],
        parent_area_identifier=record['parent_area_identifier'],
    )


def record_to_sensor(record: Record):
    return Sensor(
        identifier=record['identifier'],
        location=record_to_location(record),
        sensor_type=SensorType[record['sensor_type']],
        area_identifier=record['area_identifier']
    )


def record_to_reading(record: Record):
    return Reading(
        identifier=record['identifier'],
        weather_info=WeatherInfo(
            wind_direction=record['wind_direction'],
            wind_velocity=record['wind_velocity'],
            rainfall=record['rainfall'],
            interior_temperature=record['interior_temperature'],
            exterior_temperature=record['exterior_temperature'],
            humidity=record['humidity'],
            atmospheric_pressure=record['atmospheric_pressure']
        ),
        timestamp=record['timestamp'],
        location=record_to_location(record)
    )


def record_to_activation(record: Record):
    return Activation(
        identifier=record['identifier'],
        reading_identifier=record['reading_identifier'],
        activation_count=record['activation_count'],
        sensor_identifier=record['sensor_identifier'],
        timestamp=record.get('timestamp', None)
    )


class AreaDatasource:
    async def get(self, identifier):
        async with db.pool.acquire() as conn:
            areas = await conn.fetch("SELECT * FROM area WHERE identifier = $1", identifier)
            areas = list(map(record_to_area, areas))
            assert len(areas) <= 1
            if len(areas) == 1:
                return areas[0]
            return None

    async def create(self, area: Area):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                INSERT INTO area (id, identifier, latitude, longitude, name, area_type, parent_area_identifier)
                    values (default, default, $1, $2, $3, $4, $5)
                """, area.location.latitude, area.location.longitude, area.name, area.area_type.name,
                                   area.parent_area_identifier)

    async def all(self, page: int, elements: int):
        offset = page * elements
        print(page, elements, offset)
        async with db.pool.acquire() as conn:
            areas = await conn.fetch("SELECT * FROM area ORDER BY identifier DESC limit $1 offset $2", elements, offset)

            return list(map(record_to_area, areas))

    async def update(self, area: Area):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                UPDATE area set latitude = $2, longitude = $3, name = $4, area_type = $5, parent_area_identifier = $6
                    where identifier = $1
                """, area.identifier, area.location.latitude, area.location.longitude, area.name, area.area_type.name,
                                   area.parent_area_identifier)

    async def delete(self, identifier):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                DELETE FROM area WHERE identifier = $1
                """, identifier)


class SensorDatasource:
    async def get(self, identifier):
        async with db.pool.acquire() as conn:
            sensor = await conn.fetch("SELECT * FROM sensor WHERE identifier = $1", identifier)
            sensor = list(map(record_to_sensor, sensor))
            assert len(sensor) <= 1
            if len(sensor) == 1:
                return sensor[0]
            return None

    async def create(self, sensor: Sensor):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                INSERT INTO sensor (id, identifier, latitude, longitude, area_identifier, sensor_type)
                    values (default, $1, $2, $3, $4, $5)
                """, sensor.identifier, sensor.location.latitude, sensor.location.longitude, sensor.area_identifier,
                                   sensor.sensor_type.name)

    async def all(self, page: int, elements: int):
        offset = page * elements
        print(page, elements, offset)
        async with db.pool.acquire() as conn:
            sensors = await conn.fetch("SELECT * FROM sensor ORDER BY identifier DESC limit $1 offset $2", elements,
                                       offset)
            return list(map(record_to_sensor, sensors))

    async def update(self, sensor: Sensor):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                UPDATE sensor set latitude = $2, longitude = $3, area_identifier = $4, sensor_type = $5
                    where identifier = $1
                """, sensor.identifier, sensor.location.latitude, sensor.location.longitude, sensor.area_identifier,
                                   sensor.sensor_type.name)

    async def delete(self, identifier):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                DELETE FROM sensor WHERE identifier = $1
                """, identifier)


class ReadingDatasource:
    async def get(self, identifier):
        async with db.pool.acquire() as conn:
            reading = await conn.fetch("SELECT * FROM reading WHERE identifier = $1", identifier)
            reading = list(map(record_to_reading, reading))
            assert len(reading) <= 1
            if len(reading) == 1:
                return reading[0]
            return None

    async def create(self, reading: Reading):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                INSERT INTO reading (id, identifier, timestamp, latitude, longitude, wind_direction, wind_velocity, 
                    rainfall, interior_temperature, exterior_temperature, humidity, atmospheric_pressure)
                    values (default, default, $1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """, reading.timestamp, reading.location.latitude, reading.location.longitude,
                                   reading.weather_info.wind_direction,
                                   reading.weather_info.wind_velocity,
                                   reading.weather_info.rainfall,
                                   reading.weather_info.interior_temperature,
                                   reading.weather_info.exterior_temperature,
                                   reading.weather_info.humidity,
                                   reading.weather_info.atmospheric_pressure)

    async def all(self, page: int, elements: int):
        offset = page * elements
        print(page, elements, offset)
        async with db.pool.acquire() as conn:
            readings = await conn.fetch("SELECT * FROM reading ORDER BY timestamp DESC limit $1 offset $2", elements,
                                        offset)
            return list(map(record_to_reading, readings))

    async def update(self, reading: Reading):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                UPDATE reading set timestamp = $2,  latitude = $3,  longitude = $4,  wind_direction = $5,  
                    wind_velocity = $6, rainfall = $7,  interior_temperature = $8,  exterior_temperature = $9,  
                    humidity = $10,  atmospheric_pressure = $11
                    where identifier = $1
                """, reading.identifier, reading.timestamp, reading.location.latitude, reading.location.longitude,
                                   reading.weather_info.wind_direction,
                                   reading.weather_info.wind_velocity,
                                   reading.weather_info.rainfall,
                                   reading.weather_info.interior_temperature,
                                   reading.weather_info.exterior_temperature,
                                   reading.weather_info.humidity,
                                   reading.weather_info.atmospheric_pressure)

    async def delete(self, identifier):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                DELETE FROM reading WHERE identifier = $1
                """, identifier)

    async def all_type(self, type: WeatherInfoType, from_date: datetime, to_date: datetime):
        pass

    async def all_range(self, from_date: datetime = None, to_date: datetime = None):

        if to_date is None:
            to_date = datetime.now()

        to_date_where = "timestamp <= \'{0}\'".format(to_date.isoformat())
        if from_date is None:
            from_date_where = ""
        else:
            from_date_where = " and timestamp >= \'{0}\'".format(from_date.isoformat())

        query = """
                SELECT * FROM reading
                WHERE {0}{1} ORDER BY timestamp DESC""".format(
                    to_date_where, from_date_where)

        print(query)

        async with db.pool.acquire() as conn:
            readings = await conn.fetch(query)
            return list(map(record_to_reading, readings))


class ActivationDatasource:
    async def get(self, identifier):
        async with db.pool.acquire() as conn:
            activation = await conn.fetch("SELECT * FROM activation WHERE identifier = $1", identifier)
            activation = list(map(record_to_activation, activation))
            assert len(activation) <= 1
            if len(activation) == 1:
                return activation[0]
            return None

    async def create(self, activation: Activation):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                INSERT INTO activation (id, identifier, reading_identifier, activation_count, sensor_identifier)
                    values (default, default, $1, $2, $3)
                """, activation.reading_identifier, activation.activation_count, activation.sensor_identifier)

    async def all(self, page: int, elements: int):
        offset = page * elements
        print(page, elements, offset)
        async with db.pool.acquire() as conn:
            activations = await conn.fetch("SELECT a.*, r.timestamp FROM activation a "
                                           " JOIN reading r ON a.reading_identifier = r.identifier "
                                           " ORDER BY a.identifier DESC limit $1 offset $2",
                                           elements, offset)
            return list(map(record_to_activation, activations))

    async def update(self, activation: Activation):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                UPDATE activation set reading_identifier = $2, activation_count = $3, sensor_identifier = $4
                    where identifier = $1
                """, activation.identifier, activation.reading_identifier, activation.activation_count,
                                   activation.sensor_identifier)

    async def delete(self, identifier):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                DELETE FROM activation WHERE identifier = $1
                """, identifier)
