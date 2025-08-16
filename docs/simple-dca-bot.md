# Simple Trading Bot

Let's build our first simple trading bot!🚀🚀

It'll be a simple DCA bot for our bitcoin maximalists :)

## First Version

```python
import asyncio
from mexc import MEXC

async def dca_bot(
  pair: str = 'BTCUSDT',
  qty: str = '0.001',
  interval: int = 3600*24,
):
  async with MEXC.env() as client:
    while True:
      await client.spot.place_order(pair, {
        'quantity': qty,
        'side': 'BUY',
        'type': 'MARKET',
      })
      await asyncio.sleep(interval)
```

## Second Version

> "This eats the spread and taker fees!", you'll point out.

> "Fair enough, let's make it smarter".

We'll keep track of the order book at instead place limit orders on the top bid.

```python
async def maker_dca_bot(
  pair: str = 'BTCUSDT',
  qty: str = '0.001',
  interval: int = 3600*24,
):
  async with MEXC.env() as client:
    while True:
      book = await client.spot.depth(pair, limit=1)
      price, _ = book['bids'][0]
      order = await client.spot.place_order(pair, {
        'price': price,
        'quantity': qty,
        'type': 'LIMIT',
        'side': 'BUY',
      })
      while True:
        status = await client.spot.query_order(pair, orderId=order['orderId'])
        if status['status'] == 'FILLED':
          break
        await asyncio.sleep(15)
    
      await asyncio.sleep(interval)
```

Much better!


## Next Steps

- [Hedging Perps](/hedging-perps) - Use real-time streams for automated hedging.