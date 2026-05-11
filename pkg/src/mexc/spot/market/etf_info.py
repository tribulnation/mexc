from typing_extensions import Any
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

Response: type[dict[str, Any] | list[dict[str, Any]] | ErrorResponse] = dict[str, Any] | list[dict[str, Any]] | ErrorResponse # type: ignore
adapter = validator(Response)

class EtfInfo(SpotMixin):
  async def etf_info(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> dict[str, Any] | list[dict[str, Any]]:
    """Return spot ETF information such as net value, leverage, and fund fee.

    Args:
      symbol: ETF symbol.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#etf-endpoints"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/api/v3/etf/info', params=params)
    return self.output(r.text, adapter, validate)
