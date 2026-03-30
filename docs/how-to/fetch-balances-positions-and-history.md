# Fetch Balances, Positions & History

Use `MEXC.new()` when you need authenticated spot and futures account data together.

## Fetch Spot Balances

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account()
  print(account['balances'][0]['asset'], account['balances'][0]['free'])
```

## Fetch Spot Trade History

```python
from mexc import MEXC
from datetime import datetime, timedelta

async with MEXC.new() as client:
  end = datetime.now()
  start = end - timedelta(days=7)
  trades = await client.spot.my_trades('BTCUSDT', start=start, end=end, limit=100)
  print(trades[0]['id'], trades[0]['price'])
```

## Fetch Futures Assets

```python
from mexc import MEXC

async with MEXC.new() as client:
  assets = await client.futures.assets()
  print(assets[0]['currency'], assets[0]['availableBalance'])
```

## Fetch Futures Positions

```python
from mexc import MEXC

async with MEXC.new() as client:
  positions = await client.futures.positions()
  print(positions[0]['symbol'], positions[0]['holdVol'])
```

## Fetch Futures Trades

```python
from mexc import MEXC
from datetime import datetime, timedelta

async with MEXC.new() as client:
  end = datetime.now()
  start = end - timedelta(days=7)
  trades = await client.futures.my_trades(symbol='BTCUSDT', start=start, end=end, page_size=100)
  print(trades[0]['symbol'], trades[0]['price'])
```

## Fetch Futures Funding History

```python
from mexc import MEXC

async with MEXC.new() as client:
  history = await client.futures.my_funding_history(symbol='BTCUSDT', page_size=100)
  print(history['resultList'][0]['funding'])
```
