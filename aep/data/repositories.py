from abc import ABC


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
    pass


class ActivationRepository(Repository):
    pass
