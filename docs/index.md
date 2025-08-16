# MEXC Trading SDK

> The unofficial, fully-typed async Python SDK for MEXC, by Tribulnation.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Quick Start

```bash
pip install mexc-trading-sdk
```

```python
from mexc import MEXC

async with MEXC.new(API_KEY, API_SECRET) as client:
  candles = await client.spot.place_order('BTCUSDT', {
    'price': '50000',
    'quantity': '0.001',
    'type': 'LIMIT',
    'side': 'BUY',
  })
```

## Why MEXC SDK?

- **🚀 Fully Async** - Built with `httpx` for high-performance async operations
- **🔒 Type Safe** - Complete type annotations with `TypedDict` and `pydantic` validation
- **⚡ Easy to Use** - Simple context-managed API with `async with`
- **📊 Comprehensive** - Spot trading, market data, wallet, and WebSocket streams
- **🎯 No Setup Required** - Start exploring markets immediately

## What's Included

- **Market Data** - Real-time prices, order books, and historical data
- **Spot Trading** - Place, cancel, and query orders
- **User Data** - Account balances, trade history, and order status
- **Wallet Operations** - Deposits, withdrawals, and address management
- **WebSocket Streams** - Live market data and user notifications

## Next Steps

- [Getting Started](/getting-started) - Explore markets with real-time data
- [API Keys Setup](/api-keys) - Set up your MEXC API credentials for trading
- [Simple DCA Bot](/simple-dca-bot) - Start trading in MEXC with a simple DCA bot.
- [Hedging Perps](/hedging-perps) - Use real-time streams for automated hedging.
