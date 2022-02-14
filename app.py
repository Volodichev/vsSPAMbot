import asyncio
import logging

from bots.bots import init_webhook_bots
from aiohttp import web
import sys

# v. 0.1.10 11.02.2022
from server import init_server

polling = True

try:
    import uvloop

    asyncio.set_event_loop(uvloop.EventLoopPollicy())
except ImportError:
    print('Uvloop is not available')


async def on_startup(app: web.Application):
    print('on_startup')
    # await setup_routes(app) #restapi
    await init_webhook_bots(app)


async def on_cleanup(app):
    logging.warning('on_cleanup..')

    # await shutdown()


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    # insert code here to run it before shutdown

    # await bot.delete_webhook()

    logging.warning('Bye!')


def init_app() -> web.Application:
    app = web.Application()

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_cleanup)
    app.on_cleanup.append(on_cleanup)

    return app


if __name__ == '__main__':
    try:
        app = init_app()
        server = init_server()
        web.run_app(app=app, sock=server)

    except Exception as e:
        logging.warning(e)

