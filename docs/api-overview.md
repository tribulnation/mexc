# API Overview

Guide to available endpoints in Typed MEXC. Not all [MEXC API](https://mexcdevelop.github.io/apidocs/spot_v3_en/) endpoints are implemented yet.

## Module Structure

The client is organized hierarchically, mirroring MEXC's API structure:

```python
from mexc import MEXC

async with MEXC.new() as client:
    client.spot          # Spot trading + market data + wallet + streams
    client.futures       # Futures market data + user data + streams
```

Methods are mixed onto `client.spot` and `client.futures` directly (no nested sub-modules for REST).

## Spot Trading

### Spot Market Data (Public)

| Method | Description | Returns |
|--------|-------------|---------|
| `time()` | Get server time | `ServerTime` |
| `depth()` | Get order book depth | `OrderbookData` |
| `trades()` | Get recent trades | `list` |
| `agg_trades()` | Get aggregated trades | `list` |
| `avg_price()` | Get average price | — |
| `candles()` | Get candlestick data | `list[Candle]` |
| `candles_paged()` | Get candles (paginated) | `AsyncIterable` |
| `exchange_info()` | Get exchange info / symbols | — |

**Example:**

```python
# Get candles
candles = await client.spot.candles('BTCUSDT', interval='1m', limit=100)

# Paginated candles
async for chunk in client.spot.candles_paged(
    'BTCUSDT', interval='1m', start=start, end=end
):
    for c in chunk:
        print(c.open, c.close)
```

### Spot Account / User Data

| Method | Description | Returns |
|--------|-------------|---------|
| `account()` | Get account information | `AccountInfo` |
| `my_trades()` | Get trade history | `list[Trade]` |
| `my_trades_paged()` | Get trades (paginated) | `AsyncIterable` |
| `query_order()` | Get order by ID | — |
| `open_orders()` | Get open orders | `list` |
| `my_orders()` | Get order history | `list` |

**Example:**

```python
# Get account
account = await client.spot.account()

# Get recent trades
trades = await client.spot.my_trades('BTCUSDT', limit=50)
```

### Spot Trade

| Method | Description | Returns |
|--------|-------------|---------|
| `place_order()` | Place order | `NewOrder` |
| `cancel_order()` | Cancel order | — |
| `cancel_all_orders()` | Cancel all orders for symbol | — |

**Example:**

```python
# Place limit order
result = await client.spot.place_order(
    'BTCUSDT',
    {'side': 'BUY', 'type': 'LIMIT', 'price': '50000', 'quantity': '0.001'}
)

# Cancel
await client.spot.cancel_order('BTCUSDT', orderId=result['orderId'])
```

### Spot Wallet

| Method | Description | Returns |
|--------|-------------|---------|
| `currency_info()` | Get currency info | — |
| `deposit_addresses()` | Get deposit addresses | — |
| `deposit_history()` | Get deposit history | — |
| `withdrawal_history()` | Get withdrawal history | — |
| `withdraw()` | Withdraw | — |
| `cancel_withdraw()` | Cancel withdrawal | — |

### Spot WebSocket Streams

**Module**: `client.spot.streams`

| Method | Description |
|--------|-------------|
| `candles(symbol, interval)` | Subscribe to klines |
| `depth(symbol, level)` | Subscribe to order book |
| `my_trades()` | Subscribe to user deals (via `auth_ws`) |

## Futures

### Futures Market Data

| Method | Description | Returns |
|--------|-------------|---------|
| `candles()` | Get candlestick data | `list` |
| `candles_paged()` | Get candles (paginated) | `AsyncIterable` |
| `contract_info()` | Get contract info | `Info` |
| `depth()` | Get order book depth | — |
| `funding_rate()` | Get funding rate | `Data` |
| `funding_rate_history()` | Get funding rate history | — |
| `funding_rate_history_paged()` | Funding history (paginated) | `AsyncIterable` |

**Example:**

```python
# Contract info
info = await client.futures.contract_info('BTC_USDT')

# Funding rate
rate = await client.futures.funding_rate(symbol='BTC_USDT')
```

### Futures User Data

| Method | Description | Returns |
|--------|-------------|---------|
| `assets()` | Get futures account assets | `list[Asset]` |
| `positions()` | Get positions | `list[Position]` |
| `my_trades()` | Get trade history | — |
| `my_funding_history()` | Get funding history | — |

**Example:**

```python
# Get positions
positions = await client.futures.positions()

# Get positions for symbol
btc_pos = await client.futures.positions(symbol='BTC_USDT')
```

### Futures Trade

Not yet implemented. (Order placement, cancellation, etc.)

### Futures WebSocket Streams

**Module**: `client.futures.streams`

| Method | Description |
|--------|-------------|
| `tickers()` | Subscribe to all tickers |
| `my_trades()` | Subscribe to user deals |

## Common Parameters

- **symbol** (futures): Use underscore format, e.g. `'BTC_USDT'` (not `BTCUSDT`). Spot uses `'BTCUSDT'`.
- **interval** (candles): `'1m'`, `'5m'`, `'15m'`, `'30m'`, `'60m'`, `'4h'`, `'1d'`, `'1W'`, `'1M'` (spot REST); `'Min1'`, `'Min5'`, etc. (streams)
- **Time**: Pass `datetime` or ms; e.g. `start=datetime(2024,1,1)`, `end=datetime.now()`
- **validate**: Default `True`; use `validate=False` per call or `MEXC.new(validate=False)` to skip Pydantic validation

## Response Types

Responses use `TypedDict` / `NamedTuple` with precise types (strings for amounts, `Decimal` where used, `datetime` for timestamps). Use IDE autocomplete.

## Pagination

Manual: use `limit` and `start`/`end`. Auto: `async for chunk in client.spot.candles_paged(...)` or `client.spot.my_trades_paged(...)`.

## Errors

`mexc.core`: `Error`, `NetworkError`, `ValidationError`, `UserError`, `AuthError`, `ApiError`. Catch as needed.

## Advanced

Custom base URL: `Spot.new(..., base_url='...')` or `Futures.new(..., base_url='...')` when constructing directly. The top-level `MEXC.new()` uses defaults.

## Next Steps

[Examples](examples.md) · [Design Philosophy](design-philosophy.md) · [Quickstart](quickstart.md)

For parameter details, use `help(client.spot.account)` or your IDE docstrings.
