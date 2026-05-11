# Fetch Balances, Positions & History

Use `MEXC.new()` when you need authenticated spot and futures account data together.

## Fetch Spot Balances

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account.info()
  print(account['balances'][0]['asset'], account['balances'][0]['free'])
```

## Fetch Spot Trade History

```python
from mexc import MEXC

async with MEXC.new() as client:
  trades = await client.spot.account.trades(symbol='BTCUSDT', limit=100)
  print(trades[0]['id'], trades[0]['price'])
```

## Fetch Futures Assets

```python
from mexc import MEXC

async with MEXC.new() as client:
  assets = await client.futures.account.assets()
  print(assets[0]['currency'], assets[0]['availableBalance'])
```

## Fetch Futures Positions

```python
from mexc import MEXC

async with MEXC.new() as client:
  positions = await client.futures.position.open()
  print(positions[0]['symbol'], positions[0]['holdVol'])
```

## Fetch Futures Trades

```python
from mexc import MEXC

async with MEXC.new() as client:
  trades = await client.futures.trade.order_deals(
    symbol='BTC_USDT',
    page_num=1,
    page_size=100,
  )
  print(trades['data'][0]['symbol'], trades['data'][0]['price'])
```

## Fetch Futures Funding History

```python
from mexc import MEXC

async with MEXC.new() as client:
  history = await client.futures.account.funding_records(
    symbol='BTC_USDT',
    page_num=1,
    page_size=100,
  )
  print(history['data']['resultList'][0]['funding'])
```
