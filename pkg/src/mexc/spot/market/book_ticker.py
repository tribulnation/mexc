from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

class BookTickerResponse(TypedDict):
  """Best bid and ask ticker."""
  symbol: str
  """Spot symbol."""
  bidPrice: str
  """Best bid price."""
  bidQty: str
  """Best bid quantity."""
  askPrice: str
  """Best ask price."""
  askQty: str
  """Best ask quantity."""

class BookTickerListItem(TypedDict):
  """Best bid and ask ticker."""
  symbol: NotRequired[str]
  """Spot symbol."""
  bidPrice: NotRequired[str]
  """Best bid price."""
  bidQty: NotRequired[str]
  """Best bid quantity."""
  askPrice: NotRequired[str]
  """Best ask price."""
  askQty: NotRequired[str]
  """Best ask quantity."""

Response: type[BookTickerResponse | list[BookTickerListItem] | ErrorResponse] = BookTickerResponse | list[BookTickerListItem] | ErrorResponse # type: ignore
adapter = validator(Response)

class BookTicker(SpotMixin):
  async def book_ticker(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> BookTickerResponse | list[BookTickerListItem]:
    """Return best bid and ask for one spot symbol or all symbols.

    Args:
      symbol: Spot symbol. If omitted, returns all symbols.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#symbol-order-book-ticker)
    """
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/api/v3/ticker/bookTicker', params=params)
    return self.output(r.text, adapter, validate)
