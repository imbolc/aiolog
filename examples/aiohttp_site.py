from aiohttp import web

import aiolog
from utils import get_logger

log = get_logger(__name__)


async def hello(request):
    log.debug("Hey")
    try:
        assert 0
    except Exception:
        log.exception("Error occurred")
    return web.Response(text="Hello, world!")


app = web.Application()
app.router.add_get("/", hello)
aiolog.setup_aiohttp(app)
web.run_app(app)
