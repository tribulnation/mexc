<p align="center">
  <a href="https://mexc.tribulnation.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tribulnation/mexc/refs/heads/main/media/mexc-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tribulnation/mexc/refs/heads/main/media/mexc-light.svg">
      <img alt="Typed MEXC" src="https://raw.githubusercontent.com/tribulnation/mexc/refs/heads/main/media/mexc-light.svg" width="520">
    </picture>
  </a>
</p>

<p align="center">
  <em>A fully typed, validated async client for the MEXC spot and futures APIs.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/typed-mexc/">
    <img src="https://img.shields.io/pypi/v/typed-mexc.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/typed-mexc/">
    <img src="https://img.shields.io/pypi/pyversions/typed-mexc.svg" alt="Python versions">
  </a>
  <a href="https://mexc.tribulnation.com/">
    <img src="https://img.shields.io/badge/docs-live-black" alt="Docs">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/pypi/l/typed-mexc.svg" alt="License">
  </a>
</p>

---

- **Documentation**: [https://mexc.tribulnation.com](https://mexc.tribulnation.com)
- **Source Code**: [https://github.com/tribulnation/mexc](https://github.com/tribulnation/mexc)

---

```python
from mexc import MEXC

async with MEXC.public() as client:
  candles = await client.spot.market.candles(symbol='BTCUSDT', interval='1m', limit=5)
  stream = await client.futures.streams.market.ticker('BTC_USDT')
  print(candles[-1][4])

  async for ticker in stream:
    print(ticker['lastPrice'])
    break
```

## Why Typed MEXC?

- **🎯 Precise Types**: Typed endpoint inputs and responses.
- **✅ Runtime Validation**: Validated responses by default.
- **⚡ Async First**: HTTP and WebSocket subscriptions.
- **📚 Full API Surface**: `client.spot`, `client.futures`, and
  stream groups for both spot and futures.

## Installation

```bash
pip install typed-mexc
```

## How To

- [API Keys Setup](https://mexc.tribulnation.com/api-keys/)
- [Fetch Market Data](https://mexc.tribulnation.com/how-to/fetch-market-data/)
- [Fetch Balances, Positions & History](https://mexc.tribulnation.com/how-to/fetch-balances-positions-and-history/)
- [Place & Manage Spot Orders](https://mexc.tribulnation.com/how-to/place-and-manage-spot-orders/)
- [Listen To Streams](https://mexc.tribulnation.com/how-to/listen-to-streams/)

## Reference

- [Async Usage](https://mexc.tribulnation.com/reference/async-usage/)
- [Error Handling](https://mexc.tribulnation.com/reference/error-handling/)
- [Environment Variables](https://mexc.tribulnation.com/reference/env-vars/)
- [Generated API Reference](https://mexc.tribulnation.com/reference/api/)
