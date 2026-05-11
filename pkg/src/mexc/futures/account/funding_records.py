from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """funding record"""
  id: NotRequired[int | str]
  """Funding record id."""
  symbol: NotRequired[str]
  """Contract symbol."""
  positionId: NotRequired[int | str]
  """Position id when present."""
  positionType: NotRequired[int]
  """Position side: Item1 long, 2 short."""
  positionValue: NotRequired[float]
  """Position value used for funding."""
  funding: NotRequired[float]
  """Funding amount."""
  rate: NotRequired[float]
  """Funding rate."""
  settleTime: NotRequired[datetime | str]
  """Funding settlement time."""

class Data(TypedDict):
  """Funding record page."""
  pageSize: NotRequired[int]
  """Number of records requested per page."""
  totalCount: NotRequired[int]
  """Total number of matching records."""
  totalPage: NotRequired[int]
  """Total number of available pages."""
  currentPage: NotRequired[int]
  """Current page number."""
  resultList: NotRequired[list[Item]]
  """Page of funding record records."""

class Response200(TypedDict):
  """Get user funding records response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: Data

adapter = validator(Response200)

class FundingRecords(AuthFuturesMixin):
  async def funding_records(
    self,
    *,
    symbol: str | None = None,
    position_id: int | None = None,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> Response200:
    """Returns paginated funding-fee records for the signed futures account.

    Args:
      symbol: Optional contract symbol filter.
      position_id: Optional position id filter.
      page_num: Page number; default is 1.
      page_size: Page size; default 20, maximum 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-details-of-user-s-funding-rate"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if position_id is not None:
      params['position_id'] = position_id
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.signed_request('GET', '/api/v1/private/position/funding_records', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)

  async def funding_records_paged(self, *, symbol: str | None = None, position_id: int | None = None, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `funding_records` until the response reports the final page."""
    page = 1
    while True:
      response = await self.funding_records(symbol=symbol, position_id=position_id, page_size=page_size, page_num=page, validate=validate)
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
