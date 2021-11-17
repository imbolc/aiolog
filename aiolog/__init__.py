"""Asynchronous handlers for standard python logging library"""
import asyncio

__version__ = "0.1.1"
HANDLERS = []


def start():
    for handler in HANDLERS:
        handler.start()


async def stop(*agrs):
    await asyncio.gather(*[h.stop() for h in HANDLERS])


def setup_aiohttp(app, *, graceful_shutdown: bool = True):
    start()
    if graceful_shutdown:
        app.on_shutdown.append(stop)
