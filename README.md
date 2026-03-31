# Typed MEXC

[![MEXC](https://raw.githubusercontent.com/tribulnation/mexc/refs/heads/main/media/mexc.svg)](https://www.mexc.com)

> A fully typed, validated async client for the MEXC spot and futures APIs

**Use autocomplete instead of documentation.**

```python
from mexc import MEXC

async with MEXC.new() as client:
  account = await client.spot.account()
  print(account['balances'][0]['asset'])
```

## Why Typed MEXC?

- **🎯 Precise Types**: Strong typing throughout, so your editor can help before runtime does.
- **✅ Automatic Validation**: Catch upstream API changes earlier, where they are easier to debug.
- **⚡ Async First**: Built for concurrent, network-heavy workflows.
- **🔒 Safer Usage**: Typed inputs and explicit errors reduce avoidable mistakes.
- **🎨 Better DX**: Clear `spot` / `futures` routing and stream surfaces.
- **📦 Practical Extras**: Pagination helpers and streams where they actually help.

## Package Shape

This package intentionally follows the way MEXC itself is split:

- `MEXC.spot` for spot market data, trading, user data, wallet methods, and spot streams
- `MEXC.futures` for futures market data, futures user data, and futures streams

Current limitation:

- futures trading REST methods are not available in the MEXC API

## Installation

```bash
pip install typed-mexc
```

## Documentation

> [**Read the docs**](https://mexc.tribulnation.com)
