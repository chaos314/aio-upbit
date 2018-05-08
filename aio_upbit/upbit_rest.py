import asyncio
import aiohttp
import jwt
import time
from urllib.parse import urlencode

PROTOCOL = 'https'
HOST = 'api-beta.upbit.com'
VERSION = 'v1'
USER_AGENT = 'aio-upbit'


class UpbitRest(object):
    """
    """

    def __init__(self, access_key, secret_key, read_timeout=5, conn_timeout=5):
        self._access_key = access_key
        self._secret_key = secret_key
        self._read_timeout = read_timeout
        self._conn_timeout = conn_timeout
        self._session = self._setup()
        self.host_url = self.get_host_url()

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

    async def _fetch(self, method, path, query_params=None, authorization=False):
        url = '{0:s}/{1:s}'.format(self.host_url, path)
        headers = {'User-Agent': USER_AGENT}
        if authorization:
            payload = {
                'access_key': self._access_key,
                'nonce': str(int(time.time() * 1000))
            }
            if query_params:
                payload['query'] = query_params
                url = '{0:s}?{1:s}'.format(url, query_params)
            token = jwt.encode(payload, self._secret_key, algorithm='HS256')
            headers['Authorization'] = 'Bearer {0:s}'.format(token.decode('utf-8'))
        async with self._session.request(method, url, headers=headers, params=(query_params if query_params else None)) as resp:
            if resp.reason == 'OK':
                #result = await resp.text()
                result = await resp.json()
            else:
                result = None
        return result
        
    def get_host_url(self):
        url = '{0:s}://{1:s}/{2:s}'.format(PROTOCOL, HOST, VERSION)
        return url

    async def get_markets(self):
        return await self._fetch('GET', 'market/all')

    async def get_candles_per_minutes(self, minute, market, to='', count=1, cursor=0):
        if minute not in {1, 3, 5, 15, 10, 30, 60, 240}:
            raise Exception('{0:d}-minute interval is not available.'.format(minute))
        query_params = {'market': market,
                        'to': to,
                        'count': count,
                        'cursor': cursor}
        return await self._fetch('GET', 'candles/minutes/{0:d}'.format(minute), query_params=query_params)

    async def get_candles_daily(self, market, to='', count=1):
        query_params = {'market': market,
                        'to': to,
                        'count': count}
        return await self._fetch('GET', 'candles/days', query_params=query_params)

    async def get_candles_weekly(self, market, to='', count=1):
        query_params = {'market': market,
                        'to': to,
                        'count': count}
        return await self._fetch('GET', 'candles/weeks', query_params=query_params)

    async def get_candles_monthly(self, market, to='', count=1):
        query_params = {'market': market,
                        'to': to,
                        'count': count}
        return await self._fetch('GET', 'candles/months', query_params=query_params)

    async def get_trading_history(self, market, to='', count=1, cursor=''):
        query_params = {'market': market,
                        'to': to,
                        'count': count,
                        'cursor': cursor}
        return await self._fetch('GET', 'trades/ticks', query_params=query_params)

    async def get_ticker(self, markets):
        query_params = {'markets': markets}
        return await self._fetch('GET', 'ticker', query_params=query_params)

    async def get_assets(self):
        return await self._fetch('GET', 'assets', authorization=True)

    async def get_order_chance(self, market):
        query_params = urlencode({'market': market})
        return await self._fetch('GET', 'orders/chance', query_params=query_params, authorization=True)

    async def get_order_list(self, market, state='wait', page=1, order_by='asc'):
        query_params = urlencode({'market': market,
                                  'state': state,
                                  'page': page,
                                  'order_by': order_by})
        return await self._fetch('GET', 'orders', method='get', query_params=query_params, authorization=True)

    async def get_order(self, uuid):
        query_params = urlencode({'uuid': uuid})
        return await self._fetch('GET', 'order', method='get', query_params=query_params, authorization=True)

    async def place_order(self, market, side, volume, price, ord_type='limit'):
        query_params = urlencode({'market': market,
                                  'side': side,
                                  'volume': volume,
                                  'price': price,
                                  'ord_type': ord_type})
        return await self._fetch('POST', 'orders', query_params=query_params, authorization=True)

    async def cancel_order(self, uuid):
        query_params = urlencode({'uuid': uuid})
        return await self._fetch('DELETE', 'order', query_params=query_params, authorization=True)

    async def get_withdraw_list(self, currency, state, limit=100):
        query_params = urlencode({'currency': currency,
                                  'state': state,
                                  'limit': limit})
        return await self._fetch('GET', 'withdraws', query_params=query_params, authorization=True)

    async def get_withdraw(self, uuid):
        query_params = urlencode({'uuid': uuid})
        return await self._fetch('GET', 'withdraw', query_params=query_params, authorization=True)

    async def get_withdraw_chance(self, currency):
        query_params = urlencode({'currency': currency})
        return await self._fetch('GET', 'withdraws/chance', query_params=query_params, authorization=True)

    async def withdraw_crypto(self, currency, amount, address):
        query_params = urlencode({'currency': currency,
                                  'amount': amount,
                                  'address': address})
        return await self._fetch('POST', 'withdraws/coin', query_params=query_params, authorization=True)

    async def withdraw_krw(self, amount):
        query_params = urlencode({'amount': amount})
        return await self._fetch('POST', 'withdraws/krw', query_params=query_params, authorization=True)

