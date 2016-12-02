from email.mime.text import MIMEText

import aiosmtplib

from . import base


class Handler(base.Handler):
    def __init__(self, hostname, port, sender, recipient,
                 username=None,
                 password=None,
                 use_tls=False,
                 subject='aioLog',
                 **kwargs):
        super().__init__(**kwargs)
        self.hostname = hostname
        self.port = port
        self.sender = sender
        self.recipient = recipient
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.subject = subject

    async def store(self, entries):
        async with aiosmtplib.SMTP(
            loop=self.loop,
            hostname=self.hostname,
            port=self.port,
            use_tls=self.use_tls,
        ) as smtp:
            if self.username:
                await smtp.login(self.username, self.password)
            msg = MIMEText('\n'.join(entries))
            msg['Subject'] = self.subject
            msg['From'] = self.sender
            msg['To'] = self.recipient
            await smtp.send_message(msg)
