# Error Handling

MEXC distinguishes transport failures, authentication failures, validation failures, and API-level failures.

## Common Error Categories

- `Error`: base package exception
- `NetworkError`: connection failures, timeouts, transport errors
- `AuthError`: missing credentials, invalid signatures, rejected authentication
- `ApiError`: the remote API returned an error payload or unsuccessful response
- `ValidationError`: the response shape did not match the expected schema
- `UserError`: incorrect local usage of the client

## Recommended Pattern

```python
from mexc import MEXC
from mexc.core import ApiError, AuthError, NetworkError, ValidationError

async with MEXC.new() as client:
  try:
    positions = await client.futures.positions()
  except ValidationError:
    ...
  except AuthError:
    ...
  except ApiError:
    ...
  except NetworkError:
    ...
```

## Operational Guidance

- retry transient network failures carefully
- do not blindly retry authentication failures
- log validation failures because they often signal upstream API changes
- inspect the original request context when debugging inconsistent symbol or timestamp errors
