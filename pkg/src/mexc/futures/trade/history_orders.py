from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class HistoryOrdersItem(TypedDict):
  """Futures order record."""
  orderId: int | str
  """Order identifier."""
  symbol: str
  """Contract symbol."""
  positionId: int | str
  """Related position identifier."""
  price: float
  """Order or trigger price."""
  vol: float
  """Order volume."""
  leverage: int
  """Leverage used by the order."""
  side: int
  """Order side: 1 open long, 2 close short, 3 open short, 4 close long."""
  category: int
  """Order category."""
  orderType: int
  """Order type."""
  dealAvgPrice: float
  """Average filled price."""
  dealVol: float
  """Filled volume."""
  orderMargin: float
  """Margin reserved for the order."""
  takerFee: float
  """Taker fee."""
  makerFee: float
  """Maker fee."""
  profit: float
  """Realized close profit."""
  feeCurrency: str
  """Fee currency."""
  openType: int
  """Margin mode: 1 isolated, 2 cross."""
  state: int
  """Order state."""
  externalOid: str
  """Client-provided external order id."""
  errorCode: int
  """Order error code."""
  usedMargin: float
  """Used margin."""
  createTime: datetime | str
  """Creation time."""
  updateTime: datetime | str
  """Last update time."""
  stopLossPrice: NotRequired[float]
  """Attached stop-loss price when present."""
  takeProfitPrice: NotRequired[float]
  """Attached take-profit price when present."""

class HistoryOrdersResponse(TypedDict):
  """Get historical futures orders response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: NotRequired[list[HistoryOrdersItem]]
  """Historical futures orders."""

adapter = validator(HistoryOrdersResponse)

class HistoryOrders(AuthFuturesMixin):
  async def history_orders(
    self,
    *,
    symbol: str | None = None,
    states: str | None = None,
    category: int | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    side: int | None = None,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> HistoryOrdersResponse:
    """Returns paginated historical futures orders for the signed account.

    Args:
      symbol: Optional contract symbol filter.
      states: Comma-separated order states.
      category: Order category filter.
      start_time: Start time in milliseconds; maximum 90-day span with end_time.
      end_time: End time in milliseconds; maximum 90-day span with start_time.
      side: Order side filter.
      page_num: Page number; default is 1.
      page_size: Page size; default 20, maximum 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-all-of-the-user-39-s-historical-orders)
    """
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if states is not None:
      params['states'] = states
    if category is not None:
      params['category'] = category
    if start_time is not None:
      params['start_time'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['end_time'] = ts.dump_ms(end_time)
    if side is not None:
      params['side'] = side
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.signed_request('GET', '/api/v1/private/order/list/history_orders', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)

  async def history_orders_paged(self, *, symbol: str | None = None, states: str | None = None, category: int | None = None, start_time: Timestamp | None = None, end_time: Timestamp | None = None, side: int | None = None, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[HistoryOrdersResponse]:
    """Yield pages from `history_orders` until the response reports the final page."""
    page = 1
    while True:
      response = await self.history_orders(symbol=symbol, states=states, category=category, start_time=start_time, end_time=end_time, side=side, page_size=page_size, page_num=page, validate=validate)
      yield response
      if max_pages is not None and page >= max_pages:
        break
      data = response.get('data') if isinstance(response, dict) else None
      total = None
      if isinstance(data, dict):
        total = data.get('totalPage') or data.get('totalPageNum')
      if total is None and isinstance(response, dict):
        total = response.get('totalPage') or response.get('totalPageNum')
      if total is None:
        if data == [] or response == []:
          break
        if max_pages is None:
          break
        page += 1
        continue
      if total is None or page >= total:
        break
      page += 1
