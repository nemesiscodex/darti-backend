from datetime import datetime

from aep.domain.models import AreaType, WeatherInfoType

DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 100000


class Service:
    def __init__(self, repository):
        self.repository = repository

    async def create(self, model):
        await self.repository.create(model)

    async def update(self, model):
        assert model.identifier is not None
        assert model.identifier >= 0
        await self.repository.update(model)

    async def get(self, identifier):
        return await self.repository.get(identifier)

    async def all(self, page, elements):
        if page is None:
            page = 0
        page = int(page)
        if int(page) < 0:
            page = 0
        if elements is None:
            elements = DEFAULT_PAGE_SIZE
        elements = int(elements)
        if elements < 0:
            elements = DEFAULT_PAGE_SIZE
        if elements > MAX_PAGE_SIZE:
            elements = MAX_PAGE_SIZE
        return await self.repository.all(page, elements)

    async def delete(self, identifier):
        return await self.repository.delete(identifier)


class AreaService(Service):

    @staticmethod
    def get_area_types():
        return list(area_type for area_type in AreaType)


class SensorService(Service):
    pass


class ReadingService(Service):
    async def all_type(self, type: WeatherInfoType, from_date: datetime = None, to_date: datetime = None):
        return await self.repository.all_type(type, from_date, to_date)

    async def all_range(self, from_date: datetime = None, to_date: datetime = None):
        return await self.repository.all_range(from_date, to_date)


class ActivationService(Service):
    pass
