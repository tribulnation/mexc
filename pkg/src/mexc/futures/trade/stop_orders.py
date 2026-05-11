from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Stop-limit order record."""
  id: NotRequired[int | str]
  """Stop-limit order id."""
  orderId: NotRequired[int | str]
  """Limit order id, or zero if based on a position."""
  symbol: NotRequired[str]
  """Contract symbol."""
  positionId: NotRequired[int | str]
  """Position id."""
  stopLossPrice: NotRequired[float]
  """Stop-loss price."""
  takeProfitPrice: NotRequired[float]
  """Take-profit price."""
  state: NotRequired[int]
  """Stop-limit order state."""
  triggerSide: NotRequired[int]
  """Trigger side."""
  positionType: NotRequired[int]
  """Position side."""
  vol: NotRequired[float]
  """Configured volume."""
  realityVol: NotRequired[float]
  """Actual executed volume."""
  placeOrderId: NotRequired[int | str]
  """Placed order id."""
  errorCode: NotRequired[int]
  """Error code."""
  version: NotRequired[int]
  """Record version."""
  isFinished: NotRequired[int]
  """Final-state indicator."""
  createTime: NotRequired[datetime | str]
  """Creation time."""
  updateTime: NotRequired[datetime | str]
  """Update time."""

class Response200(TypedDict):
  """List futures stop-limit orders response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Stop-limit order records."""

adapter = validator(Response200)

class StopOrders(AuthFuturesMixin):
  async def stop_orders(
    self,
    *,
    symbol: str | None = None,
    is_finished: int | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> Response200:
    """Returns paginated stop-limit trigger orders for the signed futures account.

    Args:
      symbol: Optional contract symbol filter.
      is_finished: Final-state filter: 0 unfinished, 1 finished.
      start_time: Start time in milliseconds; maximum span is 90 days.
      end_time: End time in milliseconds; maximum span is 90 days.
      page_num: Page number; default is 1.
      page_size: Page size; default 20, maximum 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-the-stop-limit-order-list"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if is_finished is not None:
      params['is_finished'] = is_finished
    if start_time is not None:
      params['start_time'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['end_time'] = ts.dump_ms(end_time)
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.signed_request('GET', '/api/v1/private/stoporder/list/orders', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)

  async def stop_orders_paged(self, *, symbol: str | None = None, is_finished: int | None = None, start_time: Timestamp | None = None, end_time: Timestamp | None = None, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `stop_orders` until the response reports the final page."""
    page = 1
    while True:
      response = await self.stop_orders(symbol=symbol, is_finished=is_finished, start_time=start_time, end_time=end_time, page_size=page_size, page_num=page, validate=validate)
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
