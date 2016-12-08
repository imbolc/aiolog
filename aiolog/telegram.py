from . import base
import aiohttp


class Handler(base.Handler):
    def __init__(self, token, chat_id, disable_notification=False, **kwargs):
        super().__init__(**kwargs)
        self.chat_id = chat_id
        self.disable_notification = disable_notification
        self.url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)

    async def store(self, entries):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            data = {
                'chat_id': self.chat_id,
                'text': '```\n{}\n```'.format('\n'.join(entries)),
                'parse_mode': 'markdown',
                'disable_notification': self.disable_notification,
                'disable_web_page_preview': True,
            }
            async with session.post(self.url, data=data):
                pass
