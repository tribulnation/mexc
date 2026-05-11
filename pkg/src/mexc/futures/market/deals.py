from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Item(TypedDict):
  """Recent contract deal."""
  p: float
  """Transaction price."""
  v: float
  """Transaction quantity."""
  T: int
  """Deal type: Item1 purchase, 2 sell."""
  O: int
  """Open-position flag/type from upstream."""
  M: int
  """Self-trade flag: Item1 yes, 2 no."""
  t: datetime
  """Transaction timestamp in milliseconds."""
  i: NotRequired[str]
  """Live API deal id."""

class Response200(TypedDict):
  """Contract deals envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Recent contract deals."""

adapter = validator(Response200)

class Deals(FuturesMixin):
  async def deals(
    self,
    symbol: str,
    *,
    limit: int | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Return recent transaction/deal data for a contract.

    Args:
      symbol: Contract symbol, for example BTC_USDT.
      limit: Number of recent deals to return; maximum is 100 and default is 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-contract-transaction-data"""
    params = {}
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v1/contract/deals/{symbol}'.replace('{symbol}', str(symbol)), params=params)
    return self.envelope_output(r.text, adapter, validate)
