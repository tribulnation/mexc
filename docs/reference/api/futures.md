# Futures

`Futures` combines futures market data, futures user data, and `futures.streams`.

## Main REST Areas

- market data: `candles`, `candles_paged`, `contract_info`, `depth`, `funding_rate`, `funding_rate_history`, `funding_rate_history_paged`
- user data: `assets`, `positions`, `my_trades`, `my_funding_history`

## Streams

`futures.streams` currently includes:

- `tickers`
- `my_trades`

## Current Limitation

`futures.trading` is present structurally, but futures trading REST methods are not available in the MEXC API.

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
