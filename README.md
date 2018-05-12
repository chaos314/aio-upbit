aio-upbit
=========

This is an unofficial Python wrapper for the Upbit API and the asynchronous version of [`python-upbit`](https://github.com/chaos314/python-upbit). I am not affiliated with Upbit. Please use at your own risk.

Donation
--------

BTC: 3Lpz6PJVtvBFhBjegvT9jyhuzkJ5LAkxGY  
ETH: 0x84D433120B0Aa19B5d9124d03ecD42665c0Fd958  
BCC: 3N5BhKh5mvKWt4oYe7FEYk24iZ7Ra64f5k  
LTC: 38QsK8687QKSTthbnSZuhqeMAYWe2mgaU8  
NEO: AY6jKuD6zwePxP4S6286ykRXj7JC7eAR2W  

Installation
------------

```
pip install aioupbit
```

Usage
-----

```python
import asyncio
from aioupbit import UpbitRest

async def task():
    async with UpbitRest(None, None) as u:
        response = await u.get_markets()
        print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(task())
```

```python
import asyncio
from aioupbit import UpbitWS

async def task():
    async with UpbitWs() as u:
        response = await u.get_ticker(MARKETS)
        print(response)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(task())
```

References
----------

https://docs.upbit.com/v1.0/reference  
https://docs.python.org/3/library/asyncio.html

Licence
-------

The MIT License (MIT)  
Copyright (c) 2018 Seokhwan Cheon  
