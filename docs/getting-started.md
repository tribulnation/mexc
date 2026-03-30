# Getting Started

This guide gets you from installation to your first public and authenticated MEXC requests.

## Install The Package

```bash
pip install typed-mexc
```

## Make A Public Spot Request

For focused public-only reads, instantiate the surface you need directly:

```python
from mexc.spot import Spot

async with Spot.public() as spot:
  depth = await spot.depth('BTCUSDT', limit=5)
  print(depth['bids'][0])
```

## Make A Public Futures Request

```python
from mexc.futures import Futures

async with Futures.public() as futures:
  rate = await futures.funding_rate('BTC_USDT')
  print(rate['fundingRate'])
```

## Make An Authenticated Request

Once your credentials are configured, use the top-level client for combined spot and futures workflows:

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account()
  positions = await client.futures.positions()
  print(account['accountType'], len(positions))
```

## Context Manager Pattern

Use `async with` so HTTP sessions and stream clients open and close cleanly:

```python
async with MEXC.new() as client:
  ...
```

You can also construct `Spot.new(...)` or `Futures.new(...)` directly when you need explicit credential control for one side of the API.

## Symbol Format Note

Spot endpoints use symbols like `BTCUSDT`.

Futures market-data endpoints in this client generally use symbols like `BTC_USDT`, while several futures private endpoints currently use `BTCUSDT`.

Follow the method docstring and autocomplete for the exact endpoint you are calling.

## Next Steps

- Go to [API Keys Setup](api-keys.md) if you have not configured credentials yet
- Read [API Overview](api-overview.md) to understand the spot / futures split
- Browse [How To](how-to/index.md) for common workflows
