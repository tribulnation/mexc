# MEXC

The top-level `MEXC` client composes:

- `spot`
- `futures`

Use it when you want a single authenticated client spanning both surfaces.

## Constructor

```python
from mexc import MEXC

client = MEXC.new(
  api_key='your_access_key',
  api_secret='your_secret_key',
  validate=True,
)
```

## Notes

- `MEXC.new()` reads `MEXC_ACCESS_KEY` and `MEXC_SECRET_KEY` if credentials are not passed explicitly
- `async with MEXC.new()` manages both `spot` and `futures` lifecycles together
- `MEXC.public()` is the public-only top-level constructor
- `Spot.public()` and `Futures.public()` are the focused public-only constructors
