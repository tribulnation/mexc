# Futures

`Futures` combines futures market data, futures user data, and `futures.streams`.

## Main REST Areas

- market data: `contract_info`, `depth`, `ticker`, `funding_rate`, `funding_rate_history`, `funding_rate_history_paged`, and related public history endpoints
- account: `assets`, `asset`, `transfer_record`, `funding_records`, `tiered_fee_rate`
- position: `open`, `history`, `leverage`, `risk_limit`, and position mutation endpoints
- trade: order reads, order placement/cancel endpoints, trigger orders, stop orders, and deal history

## Streams

`futures.streams.market` includes:

- `all_tickers` / `tickers`
- `ticker`
- `deal`
- `depth`
- `depth_full`
- `candles`
- `fair_price`
- `funding_rate`
- `index_price`

`futures.streams.user` includes:

- `login`
- `adl_level`
- `asset`
- `order`
- `position`
- `position_mode`
- `risk_limit`
- `trades`

## Safety

Some futures write endpoints are effectful or documented upstream as under maintenance. They are available for typed usage and mock-tested from recorded examples, but use live trading credentials carefully.

## Constructor

```python
from mexc.futures import Futures

futures = Futures.new(
  api_key='your_access_key',
  api_secret='your_secret_key',
)
```

For public-only reads:

```python
futures = Futures.public()
```
