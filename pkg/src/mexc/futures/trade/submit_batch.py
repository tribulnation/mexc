from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class BodyItem(TypedDict):
  """Single batch order request."""
  symbol: str
  """Contract symbol, for example BTC_USDT."""
  price: float
  """Order price. Market-price orders may ignore or use venue-specific handling."""
  vol: float
  """Order volume in contracts."""
  leverage: NotRequired[int]
  """Leverage to use; required for isolated margin according to the docs."""
  side: int
  """Order direction: Item1 open long, 2 close short, 3 open short, 4 close long."""
  type: int
  """Order type: Item1 limit, 2 post-only maker, 3 IOC, 4 FOK, 5 market, 6 market-to-current-price."""
  openType: int
  """Margin mode: Item1 isolated, 2 cross."""
  positionId: NotRequired[int]
  """Position identifier, recommended when closing a position."""
  externalOid: NotRequired[str]
  """Client-supplied external order identifier."""
  stopLossPrice: NotRequired[float]
  """Stop-loss price attached to the order."""
  takeProfitPrice: NotRequired[float]
  """Take-profit price attached to the order."""

class DataItem(TypedDict):
  """Per-order batch placement result."""
  externalOid: NotRequired[str]
  """Client-supplied external order identifier."""
  orderId: NotRequired[int | str | None]
  """Created order identifier when placement succeeds."""
  errorMsg: NotRequired[str | None]
  """Error message when placement fails."""
  errorCode: NotRequired[int]
  """Placement result code; zero indicates success."""

class Response200(TypedDict):
  """Futures batch order response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: NotRequired[list[DataItem]]
  """Per-order placement results."""

adapter = validator(Response200)

class SubmitBatch(AuthFuturesMixin):
  async def submit_batch(
    self,
    list_body_item: list[BodyItem],
    *,
    validate: bool | None = None
  ) -> Response200:
    """Places up to 50 futures orders in one request when the endpoint and account permission are available.

    Args:
      list_body_item: Request parameter.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#bulk-order-under-maintenance"""
    params = {}
    r = await self.signed_post('/api/v1/private/order/submit_batch', json=list_body_item)
    return self.envelope_output(r.text, adapter, validate)
