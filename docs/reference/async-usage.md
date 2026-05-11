# Async Usage

MEXC exposes a top-level client with spot and futures groups.

## Combined Client

Use `MEXC.new()` when you want spot and futures access in the same flow.

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account.info()
  positions = await client.futures.position.open()
```

This is the recommended default style for authenticated workflows.

## Public Usage

Use `MEXC.public()` when you only need public market data and public streams.

```python
from mexc import MEXC

async with MEXC.public() as client:
  depth = await client.spot.market.depth(symbol='BTCUSDT', limit=5)
  rate = await client.futures.market.funding_rate('BTC_USDT')
  print(depth['bids'][0], rate['data']['fundingRate'])
```

## Streams

Both `spot` and `futures` expose `streams`, and the parent clients manage their stream lifecycles under `async with`.

```python
async with MEXC.new() as client:
  stream = await client.spot.streams.user.trades()
  async for trade in stream:
    print(trade)
```
