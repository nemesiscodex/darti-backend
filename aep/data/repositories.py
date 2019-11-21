import datetime
from abc import ABC

from aep.domain.models import WeatherInfoType


class Repository(ABC):
    def __init__(self, datasource):
        self.datasource = datasource

    async def create(self, model):
        await self.datasource.create(model)

    async def update(self, model):
        await self.datasource.update(model)

    async def get(self, identifier):
        return await self.datasource.get(identifier)

    async def all(self, page, elements):
        return await self.datasource.all(page, elements)

    async def delete(self, identifier):
        return await self.datasource.delete(identifier)


class AreaRepository(Repository):
    pass


class SensorRepository(Repository):
    pass


class ReadingRepository(Repository):
    async def all_type(self, type: WeatherInfoType, from_date: datetime = None, to_date: datetime = None):
        return await self.datasource.all_type(type, from_date, to_date)

    async def all_range(self, from_date: datetime = None, to_date: datetime = None):
        return await self.datasource.all_range(from_date, to_date)


class ActivationRepository(Repository):
    pass
