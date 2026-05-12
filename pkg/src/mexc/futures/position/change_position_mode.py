from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class ChangePositionModeRequest(TypedDict):
  """Change futures position mode request body."""
  positionMode: int
  """Target position mode: 1 hedge, 2 one-way."""

class ChangePositionModeResponse(TypedDict):
  """Futures write endpoint response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""

adapter = validator(ChangePositionModeResponse)

class ChangePositionMode(AuthFuturesMixin):
  async def change_position_mode(
    self,
    body: ChangePositionModeRequest,
    *,
    validate: bool | None = None
  ) -> ChangePositionModeResponse:
    """Switches the account position mode between hedge and one-way mode when no active orders, plan orders, or unfinished positions block the change.

    Args:
      body: Request body.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/contract_v1_en/#change-position-mode)
    """
    params = {}
    r = await self.signed_post('/api/v1/private/position/change_position_mode', json=body)
    return self.envelope_output(r.text, adapter, validate)
