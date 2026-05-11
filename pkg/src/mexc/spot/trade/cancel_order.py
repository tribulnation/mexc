from datetime import datetime
from typing_extensions import Any, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Canceled order response."""
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

class CancelOrder(AuthSpotMixin):
  async def cancel_order(
    self,
    *,
    symbol: str,
    order_id: str | None = None,
    orig_client_order_id: str | None = None,
    new_client_order_id: str | None = None,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Cancels one active spot order by order id or original client order id.

    Args:
      symbol: Spot symbol.
      order_id: Order id.
      orig_client_order_id: Original client order id.
      new_client_order_id: Optional cancel client id.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#cancel-order"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if order_id is not None:
      params['orderId'] = order_id
    if orig_client_order_id is not None:
      params['origClientOrderId'] = orig_client_order_id
    if new_client_order_id is not None:
      params['newClientOrderId'] = new_client_order_id
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('DELETE', '/api/v3/order', params=params)
    return self.output(r.text, adapter, validate)
