# Fetch Market Data

MEXC market data is split between `spot` and `futures`.

## Fetch Spot Market Data

```python
from mexc.spot import Spot

async with Spot.public() as spot:
  server_time = await spot.time()
  depth = await spot.depth('BTCUSDT', limit=5)
  trades = await spot.trades('BTCUSDT', limit=10)
  print(server_time['serverTime'], depth['bids'][0], trades[0]['price'])
```

## Fetch Spot Candles

```python
from mexc.spot import Spot
from datetime import datetime, timedelta

async with Spot.public() as spot:
  end = datetime.now()
  start = end - timedelta(hours=1)
  candles = await spot.candles('BTCUSDT', interval='1m', start=start, end=end, limit=60)
  print(candles[-1].close)
```

## Fetch Spot Exchange Metadata

```python
from mexc.spot import Spot

async with Spot.public() as spot:
  info = await spot.exchange_info('BTCUSDT')
  print(info['BTCUSDT']['symbol'])
```

## Fetch Futures Market Data

```python
from mexc.futures import Futures

async with Futures.public() as futures:
  contract = await futures.contract_info('BTC_USDT')
  depth = await futures.depth('BTC_USDT', limit=20)
  rate = await futures.funding_rate('BTC_USDT')
  print(contract['symbol'], depth['bids'][0], rate['fundingRate'])
```

## Fetch Futures Funding History

```python
from mexc.futures import Futures

async with Futures.public() as futures:
  history = await futures.funding_rate_history('BTC_USDT', page_size=20)
  print(history['resultList'][0]['fundingRate'])
```
