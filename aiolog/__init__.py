import asyncio


HANDLERS = []


def start(loop=None):
    loop = loop or asyncio.get_event_loop()
    for handler in HANDLERS:
        handler.start(loop)


async def stop(*agrs):
    asyncio.gather(*[h.stop() for h in HANDLERS])


def setup_aiohttp(app):
    start(app.loop)
    app.on_shutdown.append(stop)
