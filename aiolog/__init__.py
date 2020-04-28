'''Asynchronous handlers for standard python logging library'''
import asyncio


__version__ = '0.1.0'
HANDLERS = []


def start():
    for handler in HANDLERS:
        handler.start()


async def stop(*agrs):
    await asyncio.gather(*[h.stop() for h in HANDLERS])


def setup_aiohttp(app):
    start()
    app.on_shutdown.append(stop)
