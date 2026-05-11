from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Leverage record."""
  positionType: NotRequired[int]
  """Position side: Item1 long, 2 short."""
  level: NotRequired[int]
  """Risk level."""
  imr: NotRequired[float]
  """Initial margin rate for the leverage risk level."""
  mmr: NotRequired[float]
  """Maintenance margin rate for the leverage risk level."""
  leverage: NotRequired[int]
  """Configured leverage."""

class Response200(TypedDict):
  """Get futures position leverage response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Leverage records for long and short sides."""

adapter = validator(Response200)

class Leverage(AuthFuturesMixin):
  async def leverage(self, *, symbol: str, validate: bool | None = None) -> Response200:
    """Returns leverage and risk-rate details for the signed account on a contract.

    Args:
      symbol: Contract symbol.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-leverage"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.signed_request('GET', '/api/v1/private/position/leverage', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
