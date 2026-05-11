from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Data(TypedDict):
  """Current funding-rate state for a contract."""
  symbol: str
  """Contract symbol."""
  fundingRate: float
  """Current funding rate."""
  maxFundingRate: NotRequired[float]
  """Maximum funding rate."""
  minFundingRate: NotRequired[float]
  """Minimum funding rate."""
  collectCycle: NotRequired[int]
  """Funding collection cycle in hours."""
  nextSettleTime: NotRequired[datetime]
  """Next funding settlement time in milliseconds."""
  timestamp: NotRequired[datetime]
  """System timestamp in milliseconds."""

class Response200(TypedDict):
  """Funding rate envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: Data

adapter = validator(Response200)

class FundingRate(FuturesMixin):
  async def funding_rate(self, symbol: str, *, validate: bool | None = None) -> Response200:
    """Return the current funding-rate state for a contract.

    Args:
      symbol: Contract symbol, for example BTC_USDT.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-contract-funding-rate"""
    params = {}
    r = await self.request('GET', '/api/v1/contract/funding_rate/{symbol}'.replace('{symbol}', str(symbol)))
    return self.envelope_output(r.text, adapter, validate)
