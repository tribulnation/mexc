from datetime import datetime
from typing_extensions import Any, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Order status response."""
  symbol: NotRequired[str]
  """Spot symbol."""
  orderId: NotRequired[Any]
  """MEXC order id."""
  orderListId: NotRequired[Any]
  """Order-list id."""
  clientOrderId: NotRequired[str | None]
  """Client order id."""
  price: NotRequired[str]
  """Price."""
  origQty: NotRequired[str]
  """Original quantity."""
  executedQty: NotRequired[str]
  """Executed quantity."""
  cummulativeQuoteQty: NotRequired[str]
  """Executed quote quantity."""
  status: NotRequired[str]
  """Order status."""
  timeInForce: NotRequired[str]
  """Time in force."""
  type: NotRequired[str]
  """Order type."""
  side: NotRequired[str]
  """Order side."""
  time: NotRequired[datetime]
  """Creation time."""
  updateTime: NotRequired[datetime]
  """Update time."""
  isWorking: NotRequired[bool]
  """Whether active on the order book."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class Order(AuthSpotMixin):
  async def order(
    self,
    *,
    symbol: str | None = None,
    orig_client_order_id: str | None = None,
    order_id: str | None = None,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns status and fill information for one order.

    Args:
      symbol: Spot symbol.
      orig_client_order_id: Original client order id.
      order_id: Order id.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-order"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if orig_client_order_id is not None:
      params['origClientOrderId'] = orig_client_order_id
    if order_id is not None:
      params['orderId'] = order_id
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/order', params=params)
    return self.output(r.text, adapter, validate)
