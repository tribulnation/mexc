# API Keys Setup

This page explains how to configure credentials for authenticated spot and futures requests.

## Create API Credentials

Create API credentials from the MEXC API management page:

<https://www.mexc.com/user/openapi>

Before using them in production:

- enable only the permissions you actually need
- restrict IPs when the provider supports it
- keep trading and withdrawal permissions separate when possible

## Environment Variables

The recommended setup is environment variables:

```bash
export MEXC_ACCESS_KEY="your_access_key"
export MEXC_SECRET_KEY="your_secret_key"
```

Those are the only credential variables used by `MEXC.new()`, `Spot.new()`, and `Futures.new()`.

MEXC uses access key + secret key only. There is no passphrase in the current client model.

## Direct Usage

You can also pass credentials directly:

```python
from mexc import MEXC

async with MEXC.new(
  api_key="your_access_key",
  api_secret="your_secret_key",
) as client:
  account = await client.spot.account()
  print(account['accountType'])
```

## Security Notes

- never commit credentials to git
- prefer read-only keys for development
- use separate keys for production automation
- rotate credentials after any suspected leak
- keys without an IP whitelist expire after 90 days on MEXC

## Troubleshooting

If authenticated requests fail:

- confirm the key has the required permissions
- confirm your environment variables are loaded
- confirm your IP whitelist configuration on the MEXC side
- check [Error Handling](reference/error-handling.md) for the client error model
