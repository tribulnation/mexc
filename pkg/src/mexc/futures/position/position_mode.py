from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Get futures position mode response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: int
  """Position mode: Item1 hedge, 2 one-way."""

adapter = validator(Response200)

class PositionMode(AuthFuturesMixin):
  async def position_mode(self, *, validate: bool | None = None) -> Response200:
    """Returns the signed account position mode: 1 hedge mode, 2 one-way mode.

    Args:
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-position-mode"""
    headers = {}
    params = {}
    r = await self.signed_request('GET', '/api/v1/private/position/position_mode', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
