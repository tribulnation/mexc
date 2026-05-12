# `Core`

Shared exceptions, transport helpers, validation helpers, and common type aliases.

User code should import supported package exceptions from `mexc` directly:

```python
from mexc import ApiError, AuthError, NetworkError, RateLimited, ValidationError
```

## Root Exceptions

These exceptions are part of the package-root public surface:

1. `Error`: base package exception.
2. `NetworkError`: connection failures, timeouts, and transport errors.
3. `AuthError`: missing credentials, invalid signatures, or rejected authentication.
4. `BadRequest`: invalid request parameters or malformed payloads rejected locally or remotely.
5. `RateLimited`: provider-side rate limiting.
6. `ApiError`: the remote API returned an error payload or unsuccessful response.
7. `ValidationError`: the response shape did not match the expected schema.
8. `LogicError`: incorrect local usage of the client.

## Core Types

These aliases live under `mexc.core` and are used by generated method signatures:

1. `Timestamp`: accepted timestamp input type for request parameters that may be `datetime`, numeric timestamps, or numeric timestamp strings.
2. `OrderSide`: shared spot order side literal.
3. `OrderType`: shared spot order type literal.
4. `OrderStatus`: shared spot order status literal.
5. `TimeInForce`: shared spot time-in-force literal.

## Validation And Transport

These helpers are mostly used by generated modules and advanced integrations:

1. `mexc.core.ValidationMixin`: response validation and output parsing mixin.
2. `mexc.core.HttpClient`: async HTTP transport client.
3. `mexc.core.HttpMixin`: request helper mixin used by REST endpoint groups.
4. `mexc.core.validator`: pydantic adapter factory used by generated response models.
5. `mexc.core.timestamp`: timestamp conversion helper used by generated request encoders.
