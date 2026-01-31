# Quickstart

## Installation

```bash
pip install typed-mexc
```

Requires Python 3.10+ and a [MEXC](https://www.mexc.com) account. Create an API key under Account → API Management and save Access Key and Secret Key.

## Credentials

Set env vars (or use a `.env` file and `load_dotenv()`):

```bash
export MEXC_ACCESS_KEY="your_access_key"
export MEXC_SECRET_KEY="your_secret_key"
```

## First Request

```python
import asyncio
from mexc import MEXC

async def main():
    async with MEXC.new() as client:
        account = await client.spot.account()
        for balance in account['balances']:
            if float(balance['free']) > 0:
                print(f"{balance['asset']}: {balance['free']}")

asyncio.run(main())
```

## Client Structure

`client.spot`, `client.futures` — each has methods from market data, trading, user data, and streams. Spot also has wallet. Use `async with MEXC.new() as client:` for proper cleanup. Pass `api_key`, `api_secret` to `MEXC.new()` if not using env vars. Use `validate=False` to skip response validation.

## Next Steps

[Authentication](authentication.md) · [API Overview](api-overview.md) · [Examples](examples.md)
