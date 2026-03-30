# Async Usage

MEXC supports both a top-level combined client and focused subsystem clients.

## Combined Client

Use `MEXC.new()` when you want spot and futures access in the same flow.

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account()
  positions = await client.futures.positions()
```

This is the recommended default style for authenticated workflows.

## Spot-Only Or Futures-Only Usage

Use `Spot.public()`, `Futures.public()`, or their `new(...)` constructors when you only need one side of the API.

```python
from mexc.spot import Spot

async with Spot.public() as spot:
  depth = await spot.depth('BTCUSDT', limit=5)
```

```python
from mexc.futures import Futures

async with Futures.public() as futures:
  rate = await futures.funding_rate('BTC_USDT')
```

## Streams

Both `spot` and `futures` expose `streams`, and the parent clients manage their stream lifecycles under `async with`.

```python
async with MEXC.new() as client:
  stream = await client.spot.streams.my_trades()
  async for trade in stream:
    print(trade)
```
