from typing_extensions import Literal, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class BatchOrderRequest(TypedDict):
  """Order to create."""
  symbol: NotRequired[str]
  """Spot symbol."""
  side: NotRequired[Literal['BUY', 'SELL']]
  """Order side."""
  type: NotRequired[str]
  """Order type."""
  quantity: NotRequired[str]
  """Base-asset quantity."""
  quoteOrderQty: NotRequired[str]
  """Quote-asset quantity."""
  price: NotRequired[str]
  """Limit price."""
  newClientOrderId: NotRequired[str]
  """Client order id."""

class BatchOrdersItem(TypedDict):
  """Batch order result."""
  symbol: NotRequired[str]
  """Spot symbol for a successfully created order."""
  orderId: NotRequired[int | str]
  """Created MEXC order id."""
  orderListId: NotRequired[int | str]
  """Order-list id."""
  newClientOrderId: NotRequired[str]
  """Client order id for a rejected order."""
  code: NotRequired[int]
  """Error code for a rejected order."""
  msg: NotRequired[str]
  """Error message for a rejected order."""

Response: type[list[BatchOrdersItem] | ErrorResponse] = list[BatchOrdersItem] | ErrorResponse # type: ignore
adapter = validator(Response)

class BatchOrders(AuthSpotMixin):
  async def batch_orders(
    self,
    *,
    batch_orders: list[BatchOrderRequest],
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[BatchOrdersItem]:
    """Creates up to 20 orders for the same symbol in one signed request.

    Args:
      batch_orders: List of order objects; maximum 20 orders with the same symbol.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#batch-orders)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if batch_orders is not None:
      params['batchOrders'] = batch_orders
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/batchOrders', params=params)
    return self.output(r.text, adapter, validate)
