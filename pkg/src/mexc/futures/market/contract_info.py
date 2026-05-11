from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Item0(TypedDict):
  """Contract metadata record."""
  symbol: str
  """Contract symbol."""
  displayName: NotRequired[str]
  """Display name."""
  displayNameEn: NotRequired[str]
  """English display name."""
  positionOpenType: NotRequired[int]
  """Supported position open type: isolated, cross, or both."""
  baseCoin: NotRequired[str]
  """Base currency."""
  quoteCoin: NotRequired[str]
  """Quote currency."""
  settleCoin: NotRequired[str]
  """Settlement currency."""
  contractSize: NotRequired[float]
  """Contract value."""
  minLeverage: NotRequired[int]
  """Minimum supported leverage."""
  maxLeverage: NotRequired[int]
  """Maximum supported leverage."""
  priceScale: NotRequired[int]
  """Price precision scale."""
  volScale: NotRequired[int]
  """Volume precision scale."""
  amountScale: NotRequired[int]
  """Amount precision scale."""
  priceUnit: NotRequired[float]
  """Minimum price increment."""
  volUnit: NotRequired[float]
  """Minimum volume increment."""
  minVol: NotRequired[float]
  """Minimum order volume."""
  maxVol: NotRequired[float]
  """Maximum order volume."""
  state: NotRequired[int]
  """Contract status code."""
  apiAllowed: NotRequired[bool]
  """Whether API trading is allowed for the contract."""

class Item(TypedDict):
  """Contract metadata record."""
  symbol: str
  """Contract symbol."""
  displayName: NotRequired[str]
  """Display name."""
  displayNameEn: NotRequired[str]
  """English display name."""
  positionOpenType: NotRequired[int]
  """Supported position open type: isolated, cross, or both."""
  baseCoin: NotRequired[str]
  """Base currency."""
  quoteCoin: NotRequired[str]
  """Quote currency."""
  settleCoin: NotRequired[str]
  """Settlement currency."""
  contractSize: NotRequired[float]
  """Contract value."""
  minLeverage: NotRequired[int]
  """Minimum supported leverage."""
  maxLeverage: NotRequired[int]
  """Maximum supported leverage."""
  priceScale: NotRequired[int]
  """Price precision scale."""
  volScale: NotRequired[int]
  """Volume precision scale."""
  amountScale: NotRequired[int]
  """Amount precision scale."""
  priceUnit: NotRequired[float]
  """Minimum price increment."""
  volUnit: NotRequired[float]
  """Minimum volume increment."""
  minVol: NotRequired[float]
  """Minimum order volume."""
  maxVol: NotRequired[float]
  """Maximum order volume."""
  state: NotRequired[int]
  """Contract status code."""
  apiAllowed: NotRequired[bool]
  """Whether API trading is allowed for the contract."""

class Response200(TypedDict):
  """Contract information envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: Item0 | list[Item]
  """Contract metadata object when symbol is supplied, otherwise a list."""

adapter = validator(Response200)

class ContractInfo(FuturesMixin):
  async def contract_info(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Return contract metadata, optionally filtered to one futures contract.

    Args:
      symbol: Optional contract symbol filter, for example BTC_USDT.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-the-contract-information"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/api/v1/contract/detail', params=params)
    return self.envelope_output(r.text, adapter, validate)
