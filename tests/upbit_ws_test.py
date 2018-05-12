import unittest
import asyncio
from aioupbit import UpbitWs

MARKET = 'KRW-BTC'
MARKETS = [MARKET]


def async_loop(*tasks):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))


class TestUpbitWsClient(unittest.TestCase):
    """
    Integration tests for the Upbit WebSocket
    """

    def setUp(self):
        pass

    def test_get_ticker(self):
        async def test():
            async with UpbitWs() as u:
                actual = await u.get_ticker(MARKETS)
                self.assertGreater(len(actual), 0, 'get_ticker is 0-length.')
                self.assertEqual(actual['code'], MARKET, 'get_ticker has wrong data.')
        async_loop(test())

    def test_get_trading_history(self):
        async def test():
            async with UpbitWs() as u:
                actual = await u.get_trading_history(MARKETS)
                self.assertGreater(len(actual), 0, 'get_trading_history is 0-length.')
                self.assertEqual(actual['code'], MARKET, 'get_trading_history has wrong data.')
        async_loop(test())

    def test_get_orderbook(self):
        async def test():
            async with UpbitWs() as u:
                actual = await u.get_orderbook(MARKETS)
                self.assertGreater(len(actual), 0, 'get_orderbook is 0-length.')
                self.assertEqual(actual['code'], MARKET, 'get_orderbook has wrong data.')
        async_loop(test())

    def test_get_ticker_streaming(self):
        async def test1(q):
            async with UpbitWs(queue=q) as u:
                await u.get_ticker_streaming(MARKETS)
        async def test2(q):
            count = 3
            while count:
                actual = await q.get()
                self.assertGreater(len(actual), 0, 'get_ticker_streaming is 0-length.')
                self.assertEqual(actual['code'], MARKET, 'get_ticker_streaming has wrong data.')
                count -= 1
        q = asyncio.Queue()
        tasks = [
            test1(q),
            test2(q)
        ]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
                asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

    def test_get_trading_history_streaming(self):
        async def test1(q):
            async with UpbitWs(queue=q) as u:
                await u.get_trading_history_streaming(MARKETS)
        async def test2(q):
            count = 3
            while count:
                actual = await q.get()
                self.assertGreater(len(actual), 0, 'get_trading_history_streaming is 0-length.')
                self.assertEqual(actual['code'], MARKET, 'get_trading_history_streaming has wrong data.')
                count -= 1
        q = asyncio.Queue()
        tasks = [
            test1(q),
            test2(q)
        ]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
                asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

    def test_get_orderbook_streaming(self):
        async def test1(q):
            async with UpbitWs(queue=q) as u:
                await u.get_orderbook_streaming(MARKETS)
        async def test2(q):
            count = 3
            while count:
                actual = await q.get()
                self.assertGreater(len(actual), 0, 'get_orderbook_streaming is 0-length.')
                self.assertEqual(actual['code'], MARKET, 'get_orderbook_streaming has wrong data.')
                count -= 1
        q = asyncio.Queue()
        tasks = [
            test1(q),
            test2(q)
        ]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
                asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

