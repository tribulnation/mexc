# API Overview

The MEXC client surface is split into `spot` and `futures`.

The top-level entry point is:

```python
from mexc import MEXC

async with MEXC.new() as client:
  ...
```

That gives you two main surfaces:

- `client.spot`
- `client.futures`

Each one also exposes `streams`.

## `spot`

`spot` mixes several REST groups directly onto one client:

- market data: `time`, `depth`, `trades`, `agg_trades`, `avg_price`, `candles`, `exchange_info`
- trading: `place_order`, `cancel_order`, `cancel_all_orders`
- user data: `account`, `my_trades`, `query_order`, `open_orders`, `my_orders`
- wallet: `currency_info`, `deposit_addresses`, `deposit_history`, `withdrawal_history`, `withdraw`, `cancel_withdraw`

It also exposes `client.spot.streams` for:

- public candles and order book streams
- authenticated spot trade streams

## `futures`

`futures` currently covers:

- market data: `candles`, `contract_info`, `depth`, `funding_rate`, `funding_rate_history`
- user data: `assets`, `positions`, `my_trades`, `my_funding_history`

It also exposes `client.futures.streams` for:

- public futures ticker streams
- authenticated futures trade streams

## Current Limitation

The `futures.trading` surface exists structurally, but futures trading REST methods are not available in the MEXC API.

## Public vs Authenticated Usage

For combined authenticated workflows, prefer `MEXC.new()`.

For focused public-only workflows, instantiate `Spot.public()` or `Futures.public()` directly.

## Symbol Format

Spot methods use symbols like `BTCUSDT`.

Futures market-data methods generally use `BTC_USDT`.

Several futures private/user-data methods currently use `BTCUSDT`.

That inconsistency comes from the upstream API surface as represented by the current client. Use each method docstring as the final source of truth.

## Generated Reference

The complete endpoint reference belongs under [Reference > API](reference/api/index.md).
