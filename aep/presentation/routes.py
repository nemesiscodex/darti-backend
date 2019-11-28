from aiohttp import web
from aep.presentation.handlers import area_crud, sensor_crud, reading_crud, activation_crud, reading_range


def cors(function):
    async def f(request):
        result = await function(request)
        result.headers.add('Access-Control-Allow-Origin', '*')
        return result

    return f


routes = [
    web.post('/areas', cors(area_crud.create)),
    web.get('/areas', cors(area_crud.get_many)),
    web.get(r'/areas/{identifier:\d+}', cors(area_crud.get)),
    web.put(r'/areas/{identifier:\d+}', cors(area_crud.update)),
    web.delete(r'/areas/{identifier:\d+}', cors(area_crud.delete)),

    web.post('/sensors', cors(sensor_crud.create)),
    web.get('/sensors', cors(sensor_crud.get_many)),
    web.get(r'/sensors/{identifier:\d+}', cors(sensor_crud.get)),
    web.put(r'/sensors/{identifier:\d+}', cors(sensor_crud.update)),
    web.delete(r'/sensors/{identifier:\d+}', cors(sensor_crud.delete)),

    web.post('/readings', cors(reading_crud.create)),
    web.get('/readings', cors(reading_crud.get_many)),
    web.get('/readings/range', cors(reading_range)),
    web.get(r'/readings/{identifier:\d+}', cors(reading_crud.get)),
    web.put(r'/readings/{identifier:\d+}', cors(reading_crud.update)),
    web.delete(r'/readings/{identifier:\d+}', cors(reading_crud.delete)),

    web.post('/activations', cors(activation_crud.create)),
    web.get('/activations', cors(activation_crud.get_many)),
    web.get(r'/activations/{identifier:\d+}', cors(activation_crud.get)),
    web.put(r'/activations/{identifier:\d+}', cors(activation_crud.update)),
    web.delete(r'/activations/{identifier:\d+}', cors(activation_crud.delete))
]

async def api(request):
    return web.json_response({"endpoints": list(map(lambda x: {"endpoint": x.path, "method": x.method}, routes))})

routes.append(web.get('/', api))