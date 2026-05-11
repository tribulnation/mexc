from datetime import datetime
from typing_extensions import Any, NotRequired, TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

class Item(TypedDict):
  id: NotRequired[Any]
  """Trade id; can be null on current live responses."""
  price: NotRequired[str]
  """Trade price."""
  qty: NotRequired[str]
  """Trade quantity."""
  quoteQty: NotRequired[str]
  """Quote quantity."""
  time: NotRequired[datetime]
  """Trade timestamp in milliseconds."""
  isBuyerMaker: NotRequired[bool]
  """Whether the buyer was maker."""
  isBestMatch: NotRequired[bool]
  """Whether this was the best match."""
  tradeType: NotRequired[str]
  """Trade side label."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class HistoricalTrades(SpotMixin):
  async def historical_trades(
    self,
    *,
    symbol: str,
    limit: int | None = None,
    from_id: str | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Return older public spot trades for a symbol.

    Args:
      symbol: Spot symbol.
      limit: Maximum number of trades to return.
      from_id: Trade id to fetch from.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#old-trade-lookup"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if limit is not None:
      params['limit'] = limit
    if from_id is not None:
      params['fromId'] = from_id
    r = await self.request('GET', '/api/v3/historicalTrades', params=params)
    return self.output(r.text, adapter, validate)
