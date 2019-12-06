from aiohttp import web

from aep.domain.serializers import json_to_area, json_to_sensor, json_to_reading, json_to_activation
from aep.di import Services
from aep.data.db.redis import redis_pool, delete_keys
import brotli
import json


class GenericCrud:
    def __init__(self, di, deserializer):
        self.deserializer = deserializer
        self.di = di

    async def create(self, request):
        service = self.di()
        json_object = await request.json()
        model = self.deserializer(json_object)
        await service.create(model)
        await delete_keys(str(request.url) + "*")
        return web.json_response({"success": True})

    async def get_many(self, request):
        service = self.di()
        page = request.query.getone('page', None)
        elements = request.query.getone('elements', None)

        url = str(request.url)

        cached = await redis_pool.get(url)

        if cached:
            decompressed_bytes = brotli.decompress(cached)
            response = web.Response(body=decompressed_bytes.decode('utf-8'), content_type='application/json')
            response.enable_compression()
            return response
        data = json.dumps({'data': await service.all(page, elements)})

        compressed_data = brotli.compress(data.encode('utf-8'))
        # await redis_pool.set(url, codecs.encode(data.encode('utf-8'), 'gzip'), expire=86400)
        await redis_pool.set(url, compressed_data, expire=86400)
        response = web.Response(body=data, content_type='application/json')
        response.enable_compression()
        return response

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


async def reading_range(request):
    service = Services.reading()
    # TODO: Format date
    from_date = request.query.getone('from_date', None)
    to_date = request.query.getone('to_date', None)

    model = await service.all_range(from_date, to_date)
    return web.json_response({"data": model})
