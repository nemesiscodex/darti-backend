from domain.models import AreaType

DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 500


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
    pass


class ActivationService(Service):
    pass
