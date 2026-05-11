from datetime import datetime
from typing_extensions import Any, NotRequired, TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

class Item(TypedDict):
  symbol: NotRequired[str]
  """Spot symbol."""
  status: NotRequired[Any]
  """Symbol status."""
  baseAsset: NotRequired[str]
  """Base asset."""
  quoteAsset: NotRequired[str]
  """Quote asset."""
  orderTypes: NotRequired[list[str]]
  """Supported order types."""
  isSpotTradingAllowed: NotRequired[bool]
  """Whether spot trading is allowed."""
  isMarginTradingAllowed: NotRequired[bool]
  """Whether margin trading is allowed."""

class Response200(TypedDict):
  timezone: NotRequired[str]
  """Exchange timezone."""
  serverTime: NotRequired[datetime]
  """Server timestamp in milliseconds."""
  rateLimits: NotRequired[list[Any]]
  """Rate limit entries."""
  exchangeFilters: NotRequired[list[Any]]
  """Exchange-level filters."""
  symbols: list[Item]
  """Symbol trading rules."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class ExchangeInfo(SpotMixin):
  async def exchange_info(
    self,
    *,
    symbol: str | None = None,
    symbols: str | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Return spot exchange metadata and symbol trading rules.

    Args:
      symbol: Single spot symbol to query.
      symbols: Comma-separated spot symbols to query.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#exchange-information"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if symbols is not None:
      params['symbols'] = symbols
    r = await self.request('GET', '/api/v3/exchangeInfo', params=params)
    return self.output(r.text, adapter, validate)
