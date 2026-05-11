# Spot

`Spot` combines market, account, trade, wallet, sub-account, rebate, and stream methods.

## Main REST Areas

- market: `time`, `depth`, `trades`, `agg_trades`, `avg_price`, `candles`, `exchange_info`, tickers, and ETF/default symbol endpoints
- trade: order placement, test orders, batch orders, and cancel endpoints
- account: account info, orders, trades, KYC, MX deduct, and symbol permissions
- wallet: deposit, withdrawal, transfer, dust, and currency information endpoints
- sub-accounts and rebate: master-account sub-account management and affiliate/rebate endpoints

## Streams

`spot.streams.market` includes:

- `book_ticker`
- `book_ticker_batch`
- `candles`
- `depth`
- `depth_updates`
- `trades`

`spot.streams.user` includes:

- `account`
- `orders`
- `trades`

`spot.streams.listen_keys` includes listen-key `create`, `keepalive`, and `close` helpers for direct listen-key management.

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
