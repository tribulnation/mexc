from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """transfer record"""
  id: NotRequired[int | str]
  """Transfer record id."""
  txid: NotRequired[str]
  """Transfer flow number."""
  currency: NotRequired[str]
  """Currency code."""
  amount: NotRequired[float]
  """Transfer amount."""
  type: NotRequired[str]
  """Transfer direction: IN or OUT."""
  state: NotRequired[str]
  """Transfer state."""
  createTime: NotRequired[datetime | str]
  """Creation time."""
  updateTime: NotRequired[datetime | str]
  """Update time."""

class Data(TypedDict):
  """Transfer record page."""
  pageSize: NotRequired[int]
  """Number of records requested per page."""
  totalCount: NotRequired[int]
  """Total number of matching records."""
  totalPage: NotRequired[int]
  """Total number of available pages."""
  currentPage: NotRequired[int]
  """Current page number."""
  resultList: NotRequired[list[Item]]
  """Page of transfer record records."""

class Response200(TypedDict):
  """Get futures asset transfer records response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: Data

adapter = validator(Response200)

class TransferRecord(AuthFuturesMixin):
  async def transfer_record(
    self,
    *,
    currency: str | None = None,
    state: str | None = None,
    type_: str | None = None,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> Response200:
    """Returns paginated asset transfer records for the signed futures account.

    Args:
      currency: Filter by currency code.
      state: Filter by transfer state: WAIT, SUCCESS, or FAILED.
      type_: Filter by transfer direction: IN or OUT.
      page_num: Page number; default is 1.
      page_size: Page size; default 20, maximum 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-the-user-39-s-asset-transfer-records"""
    headers = {}
    params = {}
    if currency is not None:
      params['currency'] = currency
    if state is not None:
      params['state'] = state
    if type_ is not None:
      params['type'] = type_
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.signed_request('GET', '/api/v1/private/account/transfer_record', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)

  async def transfer_record_paged(self, *, currency: str | None = None, state: str | None = None, type_: str | None = None, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `transfer_record` until the response reports the final page."""
    page = 1
    while True:
      response = await self.transfer_record(currency=currency, state=state, type_=type_, page_size=page_size, page_num=page, validate=validate)
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
