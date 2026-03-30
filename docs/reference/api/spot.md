# Spot

`Spot` combines market data, trading, user data, wallet methods, and `spot.streams`.

## Main REST Areas

- market data: `time`, `depth`, `trades`, `agg_trades`, `avg_price`, `candles`, `candles_paged`, `exchange_info`
- trading: `place_order`, `cancel_order`, `cancel_all_orders`
- user data: `account`, `my_trades`, `my_trades_paged`, `query_order`, `open_orders`, `my_orders`
- wallet: `currency_info`, `deposit_addresses`, `deposit_history`, `withdrawal_history`, `withdraw`, `cancel_withdraw`

## Streams

`spot.streams` currently includes:

- `candles`
- `depth`
- `my_trades`

## Constructor

```python
from mexc.spot import Spot

spot = Spot.new(
  api_key='your_access_key',
  api_secret='your_secret_key',
)
```

For public-only reads:

```python
spot = Spot.public()
```
