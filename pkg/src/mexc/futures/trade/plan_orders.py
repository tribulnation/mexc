from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Trigger order record."""
  id: NotRequired[int | str]
  """Trigger order id."""
  symbol: NotRequired[str]
  """Contract symbol."""
  leverage: NotRequired[int]
  """Order leverage."""
  side: NotRequired[int]
  """Order side."""
  triggerPrice: NotRequired[float]
  """Trigger price."""
  price: NotRequired[float]
  """Execution price."""
  vol: NotRequired[float]
  """Order volume."""
  openType: NotRequired[int]
  """Margin mode."""
  triggerType: NotRequired[int]
  """Trigger type."""
  state: NotRequired[int]
  """Trigger order state."""
  executeCycle: NotRequired[int]
  """Execution cycle."""
  trend: NotRequired[int]
  """Trigger trend."""
  orderType: NotRequired[int]
  """Order type."""
  orderId: NotRequired[int | str]
  """Generated order id."""
  errorCode: NotRequired[int]
  """Error code."""
  createTime: NotRequired[datetime | str]
  """Creation time."""
  updateTime: NotRequired[datetime | str]
  """Update time."""

class Response200(TypedDict):
  """List futures trigger orders response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Trigger order records."""

adapter = validator(Response200)

class PlanOrders(AuthFuturesMixin):
  async def plan_orders(
    self,
    *,
    symbol: str | None = None,
    states: str | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> Response200:
    """Returns paginated trigger/plan orders for the signed futures account.

    Args:
      symbol: Optional contract symbol filter.
      states: Comma-separated trigger order states.
      start_time: Start time in milliseconds; maximum span is 90 days.
      end_time: End time in milliseconds; maximum span is 90 days.
      page_num: Page number; default is 1.
      page_size: Page size; default 20, maximum 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#gets-the-trigger-order-list"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if states is not None:
      params['states'] = states
    if start_time is not None:
      params['start_time'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['end_time'] = ts.dump_ms(end_time)
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.signed_request('GET', '/api/v1/private/planorder/list/orders', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)

  async def plan_orders_paged(self, *, symbol: str | None = None, states: str | None = None, start_time: Timestamp | None = None, end_time: Timestamp | None = None, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `plan_orders` until the response reports the final page."""
    page = 1
    while True:
      response = await self.plan_orders(symbol=symbol, states=states, start_time=start_time, end_time=end_time, page_size=page_size, page_num=page, validate=validate)
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
