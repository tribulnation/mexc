# Documentation

- **[Quickstart](quickstart.md)** — Install, credentials, first request
- **[Authentication](authentication.md)** — API keys and env vars
- **[API Overview](api-overview.md)** — Endpoints and modules
- **[Examples](examples.md)** — Portfolio, fills, trading, streams
- **[Design Philosophy](design-philosophy.md)** — Why we built it this way

## Quick start

```bash
pip install typed-mexc
export MEXC_ACCESS_KEY="..." MEXC_SECRET_KEY="..."
```

```python
from mexc import MEXC
async with MEXC.new() as client:
    account = await client.spot.account()
```

[MEXC API](https://mexcdevelop.github.io/apidocs/spot_v3_en/) · [Blog post](https://tribulnation.com/blog/clients)
