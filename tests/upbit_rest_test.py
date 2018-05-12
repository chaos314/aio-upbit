import unittest
import asyncio
import json
from aioupbit import UpbitRest

MARKET = 'KRW-BTC'
CURRENCY = 'BTC'


def async_loop(*tasks):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))


def test_basic_api_response(ut, actual, api_name):
    ut.assertIsNotNone(actual, '{0:s} returns an error.'.format(api_name))


class TestUpbitRestQuotationApi(unittest.TestCase):
    """
    Integration tests for the Upbit quotation API
    """

    def setUp(self):
        pass

    def test_has_neither_access_key_nor_secret_key(self):
        async def test(access_key, secret_key):
            async with UpbitRest(access_key, secret_key) as u:
                actual = await u.get_markets()
                self.assertIsNotNone(actual)
        tasks = [
            asyncio.ensure_future(test('abc', None)),
            asyncio.ensure_future(test(None, '123')),
            asyncio.ensure_future(test(None, None))
        ]
        async_loop(*tasks)

    def test_get_markets(self):
        async def test():
            async with UpbitRest(None, None) as u:
                actual = await u.get_markets()
                test_basic_api_response(self, actual, 'get_markets')
                self.assertGreater(len(actual), 0, 'get_markets\'s list is 0-length.')
        async_loop(test())

    def test_get_candles_per_minutes_with_exception(self):
        minute = 2
        async def test():
            async with UpbitRest(None, None) as u:
                with self.assertRaises(Exception) as cm:
                    actual = await u.get_candles_per_minutes(minute, MARKET)
                self.assertIn('{0:d}-minute'.format(minute), str(cm.exception).split())
        async_loop(test())

    def test_get_candles_per_minutes(self):
        minutes = [1, 3, 5, 10, 15, 30, 60, 240]
        count = 3
        async def test(min):
            async with UpbitRest(None, None) as u:
                actual = await u.get_candles_per_minutes(min, MARKET, '', count)
                test_basic_api_response(self, actual, 'get_candles_per_minutes')
                self.assertEqual(len(actual), count, 'the candle count is wrong.')
        tasks = [asyncio.ensure_future(test(i)) for i in minutes]
        async_loop(*tasks)

    def test_get_candles_daily(self):
        count = 5
        async def test():
            async with UpbitRest(None, None) as u:
                actual = await u.get_candles_daily(MARKET, '', count)
                test_basic_api_response(self, actual, 'get_candles_daily')
                self.assertEqual(len(actual), count, 'the candle count is wrong.')
        async_loop(test())

    def test_get_candles_weekly(self):
        count = 5
        async def test():
            async with UpbitRest(None, None) as u:
                actual = await u.get_candles_weekly(MARKET, '', count)
                test_basic_api_response(self, actual, 'get_candles_weekly')
                self.assertEqual(len(actual), count, 'the candle count is wrong.')
        async_loop(test())
        
    def test_get_candles_monthly(self):
        count = 5
        async def test():
            async with UpbitRest(None, None) as u:
                actual = await u.get_candles_monthly(MARKET, '', count)
                test_basic_api_response(self, actual, 'get_candles_monthly')
                self.assertEqual(len(actual), count, 'the candle count is wrong.')
        async_loop(test())

    def test_get_trading_history(self):
        async def test():
            async with UpbitRest(None, None) as u:
                actual = await u.get_trading_history(MARKET)
                test_basic_api_response(self, actual, 'get_trading_history')
                self.assertGreater(len(actual), 0, 'get_trading_history is 0-length.')
        async_loop(test())

    def test_get_ticker(self):
        markets = '{0:s}, BTC-ETH, KRW-STORM'.format(MARKET)
        async def test():
            async with UpbitRest(None, None) as u:
                actual = await u.get_ticker(markets)
                test_basic_api_response(self, actual, 'get_ticker')
                self.assertEqual(len(actual), 3, 'A list length is wrong.')
        async_loop(test())


class TestUpbitRestAccountApi(unittest.TestCase):
    """
    Integration tests for the Upbit exchange API

    A JSON file required for this test. It should have an access key and a secret key issued by Upbit.

    ie. key.json:
    {
        "access": "f4AT0XjalGRvnMPXaxaEK6u3lTTa5szKv7NZSW0q",
        "secret": "aSGFdg23948afj3487faheWGAEalsidhAGFDFaFa"
    }
    """

    def setUp(self):
        with open('key.json') as key_file:
            self.key = json.load(key_file)

    """
    def test_should_have_access_and_secret(self):
        async def test(access_key, secret_key):
            async with UpbitRest(access_key, secret_key) as u:
                actual = await u.get_assets()
                print(actual)
                self.assertIsNone(actual, 'Authorization failed.')
        tasks = [
            asyncio.ensure_future(test(None, None)),
            asyncio.ensure_future(test(None, self.key['secret'])),
            asyncio.ensure_future(test(self.key['access'], None))
        ]
        async_loop(*tasks)
    """

    def test_get_assets(self):
        async def test():
            async with UpbitRest(self.key['access'], self.key['secret']) as u:
                actual = await u.get_assets()
                test_basic_api_response(self, actual, 'get_assets')
        async_loop(test())

    def test_get_order_chance(self):
        async def test():
            async with UpbitRest(self.key['access'], self.key['secret']) as u:
                actual = await u.get_order_chance(MARKET)
                test_basic_api_response(self, actual, 'get_order_chance')
        async_loop(test())

    def test_get_withdraw_chance(self):
        async def test():
            async with UpbitRest(self.key['access'], self.key['secret']) as u:
                actual = await u.get_withdraw_chance(CURRENCY)
                test_basic_api_response(self, actual, 'get_withdraw_chance')
        async_loop(test())


