from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Item0(TypedDict):
  """Contract ticker/trend data."""
  symbol: str
  """Contract symbol."""
  lastPrice: float
  """Latest traded price."""
  bid1: NotRequired[float]
  """Best bid price."""
  ask1: NotRequired[float]
  """Best ask price."""
  volume24: NotRequired[float]
  """24-hour contract volume."""
  amount24: NotRequired[float]
  """24-hour quote amount."""
  holdVol: NotRequired[float]
  """Open interest volume."""
  lower24Price: NotRequired[float]
  """24-hour low price."""
  high24Price: NotRequired[float]
  """24-hour high price."""
  riseFallRate: NotRequired[float]
  """Rise/fall rate."""
  riseFallValue: NotRequired[float]
  """Rise/fall value."""
  indexPrice: NotRequired[float]
  """Index price."""
  fairPrice: NotRequired[float]
  """Fair price."""
  fundingRate: NotRequired[float]
  """Funding rate."""
  timestamp: datetime
  """Ticker timestamp in milliseconds."""

class Item(TypedDict):
  """Contract ticker/trend data."""
  symbol: str
  """Contract symbol."""
  lastPrice: float
  """Latest traded price."""
  bid1: NotRequired[float]
  """Best bid price."""
  ask1: NotRequired[float]
  """Best ask price."""
  volume24: NotRequired[float]
  """24-hour contract volume."""
  amount24: NotRequired[float]
  """24-hour quote amount."""
  holdVol: NotRequired[float]
  """Open interest volume."""
  lower24Price: NotRequired[float]
  """24-hour low price."""
  high24Price: NotRequired[float]
  """24-hour high price."""
  riseFallRate: NotRequired[float]
  """Rise/fall rate."""
  riseFallValue: NotRequired[float]
  """Rise/fall value."""
  indexPrice: NotRequired[float]
  """Index price."""
  fairPrice: NotRequired[float]
  """Fair price."""
  fundingRate: NotRequired[float]
  """Funding rate."""
  timestamp: datetime
  """Ticker timestamp in milliseconds."""

class Response200(TypedDict):
  """Ticker envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: Item0 | list[Item]
  """Ticker object when symbol is supplied, otherwise a list."""

adapter = validator(Response200)

class Ticker(FuturesMixin):
  async def ticker(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Return ticker/trend data, optionally filtered to one futures contract.

    Args:
      symbol: Optional contract symbol filter, for example BTC_USDT.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-contract-trend-data"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/api/v1/contract/ticker', params=params)
    return self.envelope_output(r.text, adapter, validate)
