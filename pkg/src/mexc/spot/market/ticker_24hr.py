from typing_extensions import Any
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

Response: type[dict[str, Any] | list[dict[str, Any]] | ErrorResponse] = dict[str, Any] | list[dict[str, Any]] | ErrorResponse # type: ignore
adapter = validator(Response)

class Ticker24hr(SpotMixin):
  async def ticker_24hr(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> dict[str, Any] | list[dict[str, Any]]:
    """Return 24-hour ticker statistics for one spot symbol or all symbols.

    Args:
      symbol: Spot symbol. If omitted, returns all symbols.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#24hr-ticker-price-change-statistics"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/api/v3/ticker/24hr', params=params)
    return self.output(r.text, adapter, validate)
