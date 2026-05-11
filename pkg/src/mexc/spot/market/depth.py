from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

class Response200(TypedDict):
  lastUpdateId: int
  """Last update id."""
  bids: list[list[str]]
  """Bid price and quantity levels."""
  asks: list[list[str]]
  """Ask price and quantity levels."""
  timestamp: NotRequired[datetime]
  """Snapshot timestamp in milliseconds."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class Depth(SpotMixin):
  async def depth(
    self,
    *,
    symbol: str,
    limit: int | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Return a spot order book snapshot for a symbol.

    Args:
      symbol: Spot symbol.
      limit: Number of bids and asks to return.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#order-book"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v3/depth', params=params)
    return self.output(r.text, adapter, validate)
