# Place & Manage Spot Orders

Spot trading methods live on `client.spot.trade`.

For safe live testing, `USDCUSDT` is a practical symbol because you can buy a very small amount.

## Place A Market Order

```python
from mexc import MEXC

async with MEXC.new() as client:
  order = await client.spot.trade.place_order(
    symbol='USDCUSDT',
    side='BUY',
    type_='MARKET',
    quantity='1',
  )
  print(order['orderId'])
```

## Query An Order

```python
from mexc import MEXC

order_id = 'your-order-id'

async with MEXC.new() as client:
  order = await client.spot.account.order(symbol='USDCUSDT', order_id=order_id)
  print(order['status'])
```

## Fetch Open Orders

```python
from mexc import MEXC

async with MEXC.new() as client:
  orders = await client.spot.account.open_orders(symbol='USDCUSDT')
  print(len(orders))
```

## Fetch Order History

```python
from mexc import MEXC

async with MEXC.new() as client:
  orders = await client.spot.account.orders(symbol='USDCUSDT', limit=20)
  print(orders[0]['orderId'])
```

## Place A Cancelable Limit Order

Use a far-off limit price with valid notional if you want an order that stays open long enough to cancel.

```python
from mexc import MEXC

async with MEXC.new() as client:
  order = await client.spot.trade.place_order(
    symbol='USDCUSDT',
    side='BUY',
    type_='LIMIT',
    price='0.8000',
    quantity='2',
  )
  print(order['orderId'])
```

## Cancel An Order

```python
from mexc import MEXC

order_id = 'your-order-id'

async with MEXC.new() as client:
  order = await client.spot.trade.cancel_order(symbol='USDCUSDT', order_id=order_id)
  print(order['status'])
```

## Cancel All Orders For A Symbol

```python
from mexc import MEXC

async with MEXC.new() as client:
  orders = await client.spot.trade.cancel_open_orders(symbol='USDCUSDT')
  print(len(orders))
```
