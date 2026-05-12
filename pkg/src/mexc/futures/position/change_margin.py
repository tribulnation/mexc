from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class ChangeMarginRequest(TypedDict):
  """Change futures position margin request body."""
  positionId: int
  """Position identifier whose margin will be changed."""
  amount: float
  """Margin amount to add or subtract."""
  type: str
  """Margin change direction: ADD increases margin, SUB decreases margin."""

class ChangeMarginResponse(TypedDict):
  """Futures write endpoint response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""

adapter = validator(ChangeMarginResponse)

class ChangeMargin(AuthFuturesMixin):
  async def change_margin(
    self,
    body: ChangeMarginRequest,
    *,
    validate: bool | None = None
  ) -> ChangeMarginResponse:
    """Increases or decreases margin on an existing futures position.

    Args:
      body: Request body.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/contract_v1_en/#increase-or-decrease-margin)
    """
    params = {}
    r = await self.signed_post('/api/v1/private/position/change_margin', json=body)
    return self.envelope_output(r.text, adapter, validate)
