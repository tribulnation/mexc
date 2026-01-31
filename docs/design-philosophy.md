# Design Philosophy

Typed MEXC follows four principles from [this blog post](https://tribulnation.com/blog/clients) on building better API clients.

## 1. Inputs shouldn't require custom imports

Use string literals, not enums. Your IDE autocompletes from `Literal` types:

```python
candles = await client.spot.candles('BTCUSDT', interval='1m')
```

## 2. Annotate types precisely

`TypedDict` with strings for prices (decimal precision), `datetime` for timestamps where applicable, `Literal` for enums. IDE and type checkers know exactly what you get.

## 3. Avoid unnecessary complication

Sensible defaults: `MEXC.new()` uses env vars and MEXC API URLs. Override only when needed (`base_url=`, `validate=False`).

## 4. Provide extra behavior optionally

Validation is on by default; use `validate=False` to skip. Pagination helpers exist (`candles_paged`, `my_trades_paged`) but simple `candles()` / `my_trades()` are there too. No forced retries or caching.

---

**Details matter. Developer experience matters.** Read the full post: [tribulnation.com/blog/clients](https://tribulnation.com/blog/clients)

[API Overview](api-overview.md) · [Examples](examples.md)
