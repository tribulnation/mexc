# Examples

## Portfolio

```python
async with MEXC.new() as client:
    account = await client.spot.account()
    total = sum(
        float(b['free']) + float(b['locked'])
        for b in account['balances']
        if float(b['free']) > 0 or float(b['locked']) > 0
    )
    print(f"Spot Balance: {total}")
```

## Positions & Fills

```python
# Futures positions
positions = await client.futures.positions()

# Spot trades
from datetime import datetime, timedelta
end, start = datetime.now(), datetime.now() - timedelta(days=7)
trades = await client.spot.my_trades('BTCUSDT', start=start, end=end, limit=100)
```

## Candles

```python
# Spot candles
candles = await client.spot.candles('BTCUSDT', interval='1m', limit=500)

# Paginated
async for chunk in client.spot.candles_paged(
    'BTCUSDT', interval='1m', start=start, end=end
):
    for c in chunk:
        print(c.open, c.close)
```

## Trading

```python
# Place limit order
result = await client.spot.place_order(
    'BTCUSDT',
    {'side': 'BUY', 'type': 'LIMIT', 'price': '50000', 'quantity': '0.001'}
)

# Cancel order
await client.spot.cancel_order('BTCUSDT', orderId=result['orderId'])

# Open orders
orders = await client.spot.open_orders(symbol='BTCUSDT')
```

## Funding Rate

```python
rate = await client.futures.funding_rate(symbol='BTC_USDT')
print(f"Funding rate: {rate['fundingRate']}")
```

## WebSocket Streams

```python
async with MEXC.new() as client:
    # Spot candles stream
    async for candle in client.spot.streams.candles('BTCUSDT', interval='Min1'):
        print(candle)
    
    # Futures tickers
    async for tickers in client.futures.streams.tickers():
        print(tickers)
```

## Error Handling

```python
from mexc.core import ApiError, ValidationError, NetworkError

try:
    account = await client.spot.account()
except ApiError as e:
    print(e)
except ValidationError:
    account = await client.spot.account(validate=False)
except NetworkError:
    pass
```

[API Overview](api-overview.md) · [Quickstart](quickstart.md)
