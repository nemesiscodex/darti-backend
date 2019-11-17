from aiohttp import web

from di import Services
from aep.domain.serializers import json_to_area, json_to_sensor, json_to_reading, json_to_activation


class GenericCrud:
    def __init__(self, di, deserializer):
        self.deserializer = deserializer
        self.di = di

    async def create(self, request):
        service = self.di()
        json_object = await request.json()
        model = self.deserializer(json_object)
        await service.create(model)
        return web.json_response({"success": True})

    async def get_many(self, request):
        service = self.di()
        page = request.query.getone('page', None)
        elements = request.query.getone('elements', None)
        return web.json_response({"data": await service.all(page, elements)})

    async def update(self, request):
        service = self.di()
        json_object = await request.json()
        assert int(request.match_info['identifier']) == int(json_object['identifier'])
        model = self.deserializer(json_object)
        await service.update(model)
        return web.json_response({"success": True})

    async def delete(self, request):
        service = self.di()
        identifier = int(request.match_info['identifier'])
        await service.delete(identifier)
        return web.json_response({"success": True})

    async def get(self, request):
        service = self.di()
        identifier = int(request.match_info['identifier'])
        model = await service.get(identifier)
        if model is None:
            return web.Response(status=404)
        return web.json_response(model)


area_crud = GenericCrud(Services.area, json_to_area)
sensor_crud = GenericCrud(Services.sensor, json_to_sensor)
reading_crud = GenericCrud(Services.reading, json_to_reading)
activation_crud = GenericCrud(Services.activation, json_to_activation)
