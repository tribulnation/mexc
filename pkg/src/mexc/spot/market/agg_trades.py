from datetime import datetime
from typing_extensions import Any, NotRequired, TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  a: NotRequired[Any]
  """Aggregate trade id; can be null."""
  f: NotRequired[Any]
  """First trade id; can be null."""
  l: NotRequired[Any]
  """Last trade id; can be null."""
  p: NotRequired[str]
  """Price."""
  q: NotRequired[str]
  """Quantity."""
  T: NotRequired[datetime]
  """Trade timestamp in milliseconds."""
  m: NotRequired[bool]
  """Whether buyer was maker."""
  M: NotRequired[bool]
  """Whether this was the best match."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class AggTrades(SpotMixin):
  async def agg_trades(
    self,
    *,
    symbol: str,
    limit: int | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Return aggregate public trades for a spot symbol.

    Args:
      symbol: Spot symbol.
      limit: Maximum number of aggregate trades.
      start_time: Start timestamp in milliseconds.
      end_time: End timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#compressed-aggregate-trades-list"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if limit is not None:
      params['limit'] = limit
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    r = await self.request('GET', '/api/v3/aggTrades', params=params)
    return self.output(r.text, adapter, validate)
