import asyncio
import logging

from . import HANDLERS


CLOSE_SIGNAL = object()


class Handler(logging.Handler):
    def __init__(self,
                 queue_size=1000,
                 level=logging.NOTSET):
        super().__init__(level=level)
        self.queue = None
        self.queue_size = queue_size
        HANDLERS.append(self)

    def emit(self, record):
        if self.queue and not self.queue.full():
            entry = self.format(record)
            self.queue.put_nowait(entry)

    def start(self, loop):
        self.loop = loop
        self.queue = asyncio.Queue(maxsize=self.queue_size, loop=loop)
        self.task = asyncio.ensure_future(self.new_entry(), loop=loop)

    async def stop(self):
        await self.queue.put(CLOSE_SIGNAL)
        await asyncio.sleep(0.1)
        self.task.cancel()

    async def new_entry(self):
        while True:
            entry = await self.queue.get()
            self.queue.task_done()
            if entry is CLOSE_SIGNAL:
                break
            entries = [entry] + list(self.get_all_entries())
            await self.store(entries)

    def get_all_entries(self):
        for i in range(self.queue.qsize()):
            yield self.queue.get_nowait()
            self.queue.task_done()

    async def store(self, entries):
        raise NotImplementedError
