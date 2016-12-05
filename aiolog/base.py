import asyncio
import logging
from contextlib import suppress

from async_timeout import timeout as timeout_manager

from . import HANDLERS


STOP_SIGNAL = object()


class Handler(logging.Handler):
    def __init__(self,
                 queue_size=1000,
                 timeout=60,
                 level=logging.NOTSET):
        super().__init__(level=level)
        self.queue = None
        self.queue_size = queue_size
        self.timeout = timeout
        self.started = False
        HANDLERS.append(self)

    def emit(self, record):
        if self.queue and not self.queue.full():
            entry = self.format(record)
            self.queue.put_nowait(entry)

    def start(self, loop):
        self.loop = loop
        self.queue = asyncio.Queue(maxsize=self.queue_size, loop=loop)
        self.task = asyncio.ensure_future(self.new_entry(), loop=loop)
        self.started = True

    async def stop(self, timeout=60):
        with suppress(asyncio.TimeoutError):
            with timeout_manager(timeout, loop=self.loop):
                await self.queue.put(STOP_SIGNAL)
                await self.queue.join()
                while self.started:
                    await asyncio.sleep(0.1, loop=self.loop)
        self.task.cancel()

    async def new_entry(self):
        time_to_stop = False
        while not time_to_stop:
            entry = await self.queue.get()
            self.queue.task_done()
            entries = [entry] + list(self.get_all_entries())
            if STOP_SIGNAL in entries:
                entries.remove(STOP_SIGNAL)
                time_to_stop = True
            if entries:
                with suppress(asyncio.TimeoutError):
                    with timeout_manager(self.timeout, loop=self.loop):
                        await self.store(entries)
        self.started = False

    def get_all_entries(self):
        for i in range(self.queue.qsize()):
            yield self.queue.get_nowait()
            self.queue.task_done()

    async def store(self, entries):
        raise NotImplementedError
