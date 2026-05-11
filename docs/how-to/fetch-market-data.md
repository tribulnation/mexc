# Fetch Market Data

MEXC market data is split between `spot` and `futures`.

For time windows, pass `datetime` objects directly. See [Timestamps](../reference/timestamps.md).

## Fetch Spot Market Data

```python
from mexc import MEXC

async with MEXC.public() as client:
  server_time = await client.spot.market.time()
  depth = await client.spot.market.depth(symbol='BTCUSDT', limit=5)
  trades = await client.spot.market.trades(symbol='BTCUSDT', limit=10)
  print(server_time['serverTime'], depth['bids'][0], trades[0]['price'])
```

## Fetch Spot Candles

```python
from datetime import datetime, timedelta
from mexc import MEXC

async with MEXC.public() as client:
  end_time = datetime.now()
  start_time = end_time - timedelta(hours=1)
  candles = await client.spot.market.candles(
    symbol='BTCUSDT',
    interval='1m',
    start_time=start_time,
    end_time=end_time,
    limit=60,
  )
  print(candles[-1][4])
```

## Fetch Futures Candles

```python
from datetime import datetime, timedelta
from mexc import MEXC

async with MEXC.public() as client:
  end = datetime.now()
  start = end - timedelta(hours=1)
  candles = await client.futures.market.candles(
    'BTC_USDT',
    interval='Min1',
    start=start,
    end=end,
  )
  print(candles['data']['close'][-1])
```

## Fetch Spot Exchange Metadata

```python
from mexc import MEXC

async with MEXC.public() as client:
  info = await client.spot.market.exchange_info(symbol='BTCUSDT')
  print(info['symbols'][0]['symbol'])
```

## Fetch Futures Market Data

```python
from mexc import MEXC

async with MEXC.public() as client:
  contract = await client.futures.market.contract_info(symbol='BTC_USDT')
  depth = await client.futures.market.depth('BTC_USDT', limit=20)
  rate = await client.futures.market.funding_rate('BTC_USDT')
  print(contract['data']['symbol'], depth['data']['bids'][0], rate['data']['fundingRate'])
```

## Fetch Futures Funding History

```python
from mexc import MEXC

async with MEXC.public() as client:
  history = await client.futures.market.funding_rate_history(
    symbol='BTC_USDT',
    page_num=1,
    page_size=20,
  )
  print(history['data']['resultList'][0]['fundingRate'])
```
