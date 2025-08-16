# Hedging Perps

Let's use the real-time streams for automated hedging.

## Reacting to Trades

We'll manually place limit short orders on the `EUR_USDT` perpetual. Once one fills, we'll automatically buy the spot, same amount.

```python
async def hedge_short():
  async with MEXC.env() as client:
    async for trade in client.futures.streams.my_trades():
      if trade['symbol'] == 'EUR_USDT':
        await client.spot.place_order('EURUSDT', {
          'quantity': f'{trade["vol"]:f}',
          'type': 'MARKET',
          'side': 'BUY',
        })
```

And that's the kind of thing you can only do with the API.🚀🚀
