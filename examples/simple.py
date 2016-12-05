from utils import get_logger
import asyncio
import aiolog


log = get_logger(__name__)


async def hello():
    log.debug('Hey')
    try:
        assert 0
    except Exception:
        log.exception('Error occurred')


loop = asyncio.get_event_loop()
aiolog.start()
loop.run_until_complete(hello())
loop.run_until_complete(aiolog.stop())
