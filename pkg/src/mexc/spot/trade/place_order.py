from datetime import datetime
from typing_extensions import Any, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Created order response."""
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

class PlaceOrder(AuthSpotMixin):
  async def place_order(
    self,
    *,
    symbol: str,
    side: str,
    type_: str,
    quantity: str | None = None,
    quote_order_qty: str | None = None,
    price: str | None = None,
    new_client_order_id: str | None = None,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Creates a live spot order on the signed account.

    Args:
      symbol: Spot symbol.
      side: Order side.
      type_: Order type.
      quantity: Base-asset quantity.
      quote_order_qty: Quote-asset amount.
      price: Limit price.
      new_client_order_id: Client order id.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#new-order"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if side is not None:
      params['side'] = side
    if type_ is not None:
      params['type'] = type_
    if quantity is not None:
      params['quantity'] = quantity
    if quote_order_qty is not None:
      params['quoteOrderQty'] = quote_order_qty
    if price is not None:
      params['price'] = price
    if new_client_order_id is not None:
      params['newClientOrderId'] = new_client_order_id
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/order', params=params)
    return self.output(r.text, adapter, validate)
