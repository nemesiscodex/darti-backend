if __name__ == '__main__':
    from aiohttp import web
    from aep.presentation.routes import routes

    app = web.Application()
    app.add_routes(routes)

    web.run_app(app, port=9000)
