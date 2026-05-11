from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class Body(TypedDict):
  """Submit futures order request body."""
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
  positionMode: NotRequired[int]
  """Position mode override: Item1 hedge, 2 one-way; defaults to account configuration."""
  reduceOnly: NotRequired[bool]
  """For one-way positions, restricts the order to reduce-only behavior when true."""

class Response200(TypedDict):
  """Futures write endpoint response envelope with created order id."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: NotRequired[int | str | None]
  """Order identifier returned when creation succeeds; null or absent when creation fails."""

adapter = validator(Response200)

class SubmitOrder(AuthFuturesMixin):
  async def submit_order(self, body: Body, *, validate: bool | None = None) -> Response200:
    """Places a futures limit, market, or post-only order when the endpoint is available and the account has sufficient margin.

    Args:
      body: Request body.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#order-under-maintenance"""
    params = {}
    r = await self.signed_post('/api/v1/private/order/submit', json=body)
    return self.envelope_output(r.text, adapter, validate)
