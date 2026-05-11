from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class Body(TypedDict):
  """Change futures leverage request body."""
  positionId: NotRequired[int]
  """Existing position identifier when changing leverage for a held position."""
  leverage: int
  """Target leverage."""
  openType: NotRequired[int]
  """Required when there is no position; 1 isolated, 2 cross."""
  symbol: NotRequired[str]
  """Required when there is no position; contract symbol."""
  positionType: NotRequired[int]
  """Required when there is no position; 1 long, 2 short."""

class Response200(TypedDict):
  """Futures write endpoint response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""

adapter = validator(Response200)

class ChangeLeverage(AuthFuturesMixin):
  async def change_leverage(self, body: Body, *, validate: bool | None = None) -> Response200:
    """Changes leverage either for an existing position or for a symbol/open-type/side when no position exists.

    Args:
      body: Request body.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#switch-leverage"""
    params = {}
    r = await self.signed_post('/api/v1/private/position/change_leverage', json=body)
    return self.envelope_output(r.text, adapter, validate)
