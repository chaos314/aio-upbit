import asyncio
import aiohttp
import uuid
import json

PROTOCOL = 'ws'
HOST = 'api-beta.upbit.com/websocket'
VERSION = 'v1'
USER_AGENT = 'aio-upbit'


class UpbitWs(object):
    """
    WebSocket client for the Upbit API
    """

    def __init__(self, read_timeout=30, conn_timeout=30, queue=None):
        self._read_timeout = read_timeout
        self._conn_timeout = conn_timeout
        self._session = self._setup()
        self.host_url = self.get_host_url()
        self.queue = queue

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close()

    def _setup(self):
        session = aiohttp.ClientSession(
            headers={'User-Agent': USER_AGENT},
            read_timeout=self._read_timeout,
            conn_timeout=self._conn_timeout,
        )
        return session

    async def _close(self):
        await self._session.close()

    def get_host_url(self):
        url = '{0:s}://{1:s}/{2:s}'.format(PROTOCOL, HOST, VERSION)
        return url

    async def _dispatch_once(self, message):
        async with self._session.ws_connect(self.host_url) as ws:
            await ws.send_str(message)
            response = await ws.receive()
            return json.loads(response.data)

    async def _dispatch(self, message):
        async with self._session.ws_connect(self.host_url) as ws:
            await ws.send_str(message)
            while True:
                response = await ws.receive()
                await self.queue.put(json.loads(response.data))

    def _make_message(self, api_type, markets, is_snapshot=True, is_simple=False):
        ticket = {'ticket': str(uuid.uuid4())}
        type = {
            'type': api_type,
            'codes': markets
        }
        if is_snapshot:
            type['isOnlySnapshot'] = True
        else:
            type['isOnlyRealtime'] = True
        if is_simple:
            format = {'format': 'SIMPLE'}
        else:
            format = {'format': 'DEFAULT'}
        message = [ticket, type, format]
        return json.dumps(message)

    async def get_ticker(self, markets):
        message = self._make_message('ticker', markets)
        return await self._dispatch_once(message)

    async def get_ticker_streaming(self, markets):
        message = self._make_message('ticker', markets, False)
        return await self._dispatch(message)

    async def get_trading_history(self, markets):
        message = self._make_message('trade', markets)
        return await self._dispatch_once(message)

    async def get_trading_history_streaming(self, markets):
        message = self._make_message('trade', markets, False)
        return await self._dispatch(message)

    async def get_orderbook(self, markets):
        message = self._make_message('orderbook', markets)
        return await self._dispatch_once(message)

    async def get_orderbook_streaming(self, markets):
        message = self._make_message('orderbook', markets, False)
        return await self._dispatch(message)

