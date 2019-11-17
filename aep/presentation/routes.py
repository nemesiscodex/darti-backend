from aiohttp import web

from aep.presentation.handlers import area_crud, sensor_crud, reading_crud, activation_crud

routes = [
    web.post('/areas', area_crud.create),
    web.get('/areas', area_crud.get_many),
    web.get(r'/areas/{identifier:\d+}', area_crud.get),
    web.put(r'/areas/{identifier:\d+}', area_crud.update),
    web.delete(r'/areas/{identifier:\d+}', area_crud.delete),

    web.post('/sensors', sensor_crud.create),
    web.get('/sensors', sensor_crud.get_many),
    web.get(r'/sensors/{identifier:\d+}', sensor_crud.get),
    web.put(r'/sensors/{identifier:\d+}', sensor_crud.update),
    web.delete(r'/sensors/{identifier:\d+}', sensor_crud.delete),

    web.post('/readings', reading_crud.create),
    web.get('/readings', reading_crud.get_many),
    web.get(r'/readings/{identifier:\d+}', reading_crud.get),
    web.put(r'/readings/{identifier:\d+}', reading_crud.update),
    web.delete(r'/readings/{identifier:\d+}', reading_crud.delete),

    web.post('/activations', activation_crud.create),
    web.get('/activations', activation_crud.get_many),
    web.get(r'/activations/{identifier:\d+}', activation_crud.get),
    web.put(r'/activations/{identifier:\d+}', activation_crud.update),
    web.delete(r'/activations/{identifier:\d+}', activation_crud.delete)
]
