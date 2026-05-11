from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Data(TypedDict):
  """Commission data."""
  makerCommission: NotRequired[float]
  """Maker commission rate."""
  takerCommission: NotRequired[float]
  """Taker commission rate."""

class Response200(TypedDict):
  """Trade fee wrapper response."""
  data: NotRequired[Data]
  code: NotRequired[int]
  """Response code."""
  msg: NotRequired[str]
  """Response message."""
  timestamp: NotRequired[datetime]
  """Response timestamp."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class TradeFee(AuthSpotMixin):
  async def trade_fee(
    self,
    *,
    symbol: str,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns maker and taker commission rates for a symbol.

    Args:
      symbol: Spot symbol whose commission rates should be returned.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-symbol-commission"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/tradeFee', params=params)
    return self.output(r.text, adapter, validate)
