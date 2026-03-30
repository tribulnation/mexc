# Typed MEXC

> Fully typed, validated async clients for the MEXC spot and futures APIs.

**Use autocomplete instead of documentation.**

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account()
  print(account['balances'][0]['asset'])
```

## Why Typed MEXC?

- **🎯 Precise Types**: Literal types where they help, so your IDE knows what is valid.
- **✅ Automatic Validation**: Catch upstream API changes earlier.
- **⚡ Async First**: Built for concurrent, network-heavy workflows.
- **🔒 Type Safety**: Full type hints throughout.
- **🎨 Better DX**: Clear separation between `spot`, `futures`, and their `streams`.
- **📦 Practical Extras**: Pagination helpers and stream wrappers where they add real value.

## Installation

```bash
pip install typed-mexc
```

## Quick Start

### Spot market data

```python
from mexc.spot import Spot

async with Spot.public() as spot:
  candles = await spot.candles('BTCUSDT', interval='1m', limit=5)
  print(candles[-1].close)
```

### Authenticated multi-surface usage

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account()
  positions = await client.futures.positions()
  print(len(account['balances']), len(positions))
```

## API Coverage

This package is split the way MEXC itself is split:

- `MEXC.spot` for spot market data, trading, user data, wallet methods, and spot streams
- `MEXC.futures` for futures market data, futures account data, and futures streams
- `spot.streams` and `futures.streams` for real-time subscriptions

Current limitation:

- futures trading REST methods are not available in the MEXC API

📋 See [API Overview](api-overview.md) for the current coverage and structure.

## Documentation

- [**Getting Started**](getting-started.md) - Install the package and make your first requests
- [**API Keys Setup**](api-keys.md) - Configure credentials for spot and futures authenticated usage
- [**API Overview**](api-overview.md) - Understand the spot / futures split and implemented surface
- [**How To**](how-to/index.md) - Task-focused guides for market data, orders, balances, and streams
- [**Reference**](reference/index.md) - Async usage, error handling, env vars, and API reference

## Design Philosophy

Typed MEXC follows the principles outlined in [this blog post](https://tribulnation.com/blog/clients).

*Details matter. Developer experience matters.*
