from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class Body(TypedDict):
  """Place futures trigger order request body."""
  symbol: str
  """Contract symbol."""
  price: NotRequired[float]
  """Execution price; may be omitted for market-price execution."""
  vol: float
  """Order volume in contracts."""
  leverage: NotRequired[int]
  """Leverage, required for isolated margin according to docs."""
  side: int
  """Order direction: Item1 open long, 2 close short, 3 open short, 4 close long."""
  openType: int
  """Margin mode: Item1 isolated, 2 cross."""
  triggerPrice: float
  """Trigger price."""
  triggerType: int
  """Trigger condition: Item1 greater than or equal, 2 less than or equal."""
  executeCycle: int
  """Execution cycle: Item1 for 24 hours, 2 for 7 days."""
  orderType: int
  """Execution order type: Item1 limit, 2 post-only maker, 3 IOC, 4 FOK, 5 market."""
  trend: int
  """Trigger price source: Item1 latest price, 2 fair price, 3 index price."""

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

class PlacePlan(AuthFuturesMixin):
  async def place_plan(self, body: Body, *, validate: bool | None = None) -> Response200:
    """Places a futures trigger order with trigger price, trigger direction, execution cycle, and execution order type.

    Args:
      body: Request body.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#trigger-order-under-maintenance"""
    params = {}
    r = await self.signed_post('/api/v1/private/planorder/place', json=body)
    return self.envelope_output(r.text, adapter, validate)
