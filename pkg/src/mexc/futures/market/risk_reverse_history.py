from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Item(TypedDict):
  """Risk fund balance snapshot."""
  symbol: str
  """Contract symbol."""
  currency: str
  """Settlement currency."""
  available: datetime
  """Risk fund balance at snapshot time."""
  snapshotTime: datetime
  """Snapshot time in milliseconds."""

class Data(TypedDict):
  """Risk fund balance history page."""
  pageSize: int
  """Page size."""
  totalCount: int
  """Total record count."""
  totalPage: int
  """Total page count."""
  currentPage: int
  """Current page number."""
  resultList: list[Item]
  """Page result records."""

class Response200(TypedDict):
  """Risk fund history envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: Data

adapter = validator(Response200)

class RiskReverseHistory(FuturesMixin):
  async def risk_reverse_history(
    self,
    *,
    symbol: str,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> Response200:
    """Return paginated risk fund balance history for a contract.

    Args:
      symbol: Contract symbol, for example BTC_USDT.
      page_num: Current page number; default is 1.
      page_size: Page size; default is 20 and maximum is 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-contract-risk-fund-balance-history"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.request('GET', '/api/v1/contract/risk_reverse/history', params=params)
    return self.envelope_output(r.text, adapter, validate)

  async def risk_reverse_history_paged(self, *, symbol: str, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `risk_reverse_history` until the response reports the final page."""
    page = 1
    while True:
      response = await self.risk_reverse_history(symbol=symbol, page_size=page_size, page_num=page, validate=validate)
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
