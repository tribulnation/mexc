from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Futures deal record."""
  id: NotRequired[int | str]
  """Trade/deal identifier."""
  symbol: NotRequired[str]
  """Contract symbol."""
  side: NotRequired[int]
  """Order side."""
  vol: NotRequired[float]
  """Executed volume."""
  price: NotRequired[float]
  """Execution price."""
  feeCurrency: NotRequired[str]
  """Fee currency."""
  fee: NotRequired[float]
  """Charged fee."""
  timestamp: NotRequired[datetime | str]
  """Execution timestamp."""
  profit: NotRequired[float]
  """Realized profit."""
  isTaker: NotRequired[bool]
  """Whether the fill was taker-side."""
  taker: NotRequired[bool]
  """Whether the fill was taker-side; name used by some examples."""
  category: NotRequired[int]
  """Order category."""
  orderId: NotRequired[int | str]
  """Related order identifier."""

class Response200(TypedDict):
  """List futures order deals response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Order deal history records."""

adapter = validator(Response200)

class OrderDeals(AuthFuturesMixin):
  async def order_deals(
    self,
    *,
    symbol: str,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> Response200:
    """Returns paginated futures order deal history for the signed account.

    Args:
      symbol: Contract symbol.
      start_time: Start time in milliseconds; default is the last 7 days and maximum span is 90 days.
      end_time: End time in milliseconds; maximum span is 90 days.
      page_num: Page number; default is 1.
      page_size: Page size; default 20, maximum 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-all-transaction-details-of-the-user-s-order"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if start_time is not None:
      params['start_time'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['end_time'] = ts.dump_ms(end_time)
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.signed_request('GET', '/api/v1/private/order/list/order_deals', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)

  async def order_deals_paged(self, *, symbol: str, start_time: Timestamp | None = None, end_time: Timestamp | None = None, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `order_deals` until the response reports the final page."""
    page = 1
    while True:
      response = await self.order_deals(symbol=symbol, start_time=start_time, end_time=end_time, page_size=page_size, page_num=page, validate=validate)
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
