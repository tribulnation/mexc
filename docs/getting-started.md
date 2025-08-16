# Getting Started

Let's start exploring the MEXC SDK. We don't need API keys for market data:

## Market Data

```python
from mexc.spot import MarketData

async with MarketData() as client:
  book = await client.depth('BTCUSDT', limit=2)
  print(book)
```

```python
{
  'bids': [
    BookEntry(price='117658.65', qty='3.27462000'),
    BookEntry(price='117658.64', qty='0.18392561')
  ],
 'asks': [
    BookEntry(price='117658.66', qty='6.52537624'),
    BookEntry(price='117658.68', qty='0.18654832')
  ]
}
```

## Real-time Feed

We can also subscribe to real-time data:

```python
from mexc.spot import MarketStreams

async with MarketStreams() as client:
  async for book in client.depth('BTCUSDT'):
    print(book)
```

```python
# keeps printing book updates
```

## Next Steps

- [API Keys Setup](/api-keys) - Set up your MEXC API credentials for trading.
- [Simple DCA Bot](/simple-dca-bot) - Start trading in MEXC with a simple DCA bot.