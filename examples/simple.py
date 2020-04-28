import asyncio

import aiolog
from utils import get_logger

log = get_logger(__name__)


async def hello():
    log.debug("Hey")
    try:
        assert 0
    except Exception:
        log.exception("Error occurred")


aiolog.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.run_until_complete(aiolog.stop())
