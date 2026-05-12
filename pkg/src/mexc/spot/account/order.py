from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class OrderStatus(TypedDict):
  """Order status response."""
  symbol: str
  """Spot symbol."""
  orderId: int | str
  """MEXC order id."""
  orderListId: int | str
  """Order-list id."""
  clientOrderId: str | None
  """Client order id."""
  price: str
  """Price."""
  origQty: str
  """Original quantity."""
  executedQty: str
  """Executed quantity."""
  cummulativeQuoteQty: str
  """Executed quote quantity."""
  status: str
  """Order status."""
  timeInForce: str | None
  """Time in force."""
  type: str
  """Order type."""
  side: str
  """Order side."""
  time: datetime
  """Creation time."""
  updateTime: datetime
  """Update time."""
  isWorking: bool
  """Whether active on the order book."""
  origQuoteOrderQty: str
  """Returned origQuoteOrderQty field."""
  stopPrice: str | None
  """Returned stopPrice field."""
  icebergQty: NotRequired[str | None]
  """Returned icebergQty field."""

Response: type[OrderStatus | ErrorResponse] = OrderStatus | ErrorResponse # type: ignore
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
  ) -> OrderStatus:
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
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-order)
    """
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
