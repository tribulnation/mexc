# Listen To Streams

MEXC exposes separate spot and futures stream surfaces.

The subscription methods are `async`, so first await the subscription, then iterate the returned stream.

## Listen To Spot Candles

```python
from mexc.spot import Spot

async with Spot.public() as spot:
  stream = await spot.streams.candles('BTCUSDT', interval='Min1')
  async for candle in stream:
    print(candle)
```

## Listen To Spot Order Book Updates

```python
from mexc.spot import Spot

async with Spot.public() as spot:
  stream = await spot.streams.depth('BTCUSDT', level=5)
  async for book in stream:
    print(book)
```

## Listen To Your Spot Trades

```python
from mexc import MEXC

async with MEXC.new() as client:
  stream = await client.spot.streams.my_trades()
  async for trade in stream:
    print(trade)
```

## Listen To Futures Tickers

```python
from mexc.futures import Futures

async with Futures.public() as futures:
  stream = await futures.streams.tickers()
  async for tickers in stream:
    print(tickers[0])
```

## Listen To Your Futures Trades

```python
from mexc import MEXC

async with MEXC.new() as client:
  stream = await client.futures.streams.my_trades()
  async for trade in stream:
    print(trade['symbol'], trade['price'])
```
