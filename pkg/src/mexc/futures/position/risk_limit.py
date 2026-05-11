from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Risk limit record."""
  symbol: NotRequired[str]
  """Contract symbol."""
  positionType: NotRequired[int]
  """Position side: Item1 long, 2 short."""
  level: NotRequired[int]
  """Current risk level."""
  maxVol: NotRequired[float]
  """Maximum position volume."""
  maxLeverage: NotRequired[int]
  """Maximum leverage rate."""
  mmr: NotRequired[float]
  """Maintenance margin rate."""
  imr: NotRequired[float]
  """Initial margin rate."""

class Response200(TypedDict):
  """Get futures account risk limits response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: dict[str, list[Item]]
  """Risk limits keyed by contract symbol."""

adapter = validator(Response200)

class RiskLimit(AuthFuturesMixin):
  async def risk_limit(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns current risk-limit levels for the signed futures account, optionally filtered by symbol.

    Args:
      symbol: Optional contract symbol; omitted returns all symbols.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-risk-limits"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.signed_request('GET', '/api/v1/private/account/risk_limit', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
