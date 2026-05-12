from datetime import datetime
from typing_extensions import AsyncIterator, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class RowsItem(TypedDict):
  """Transfer row."""
  tranId: str | None
  """Transfer id."""
  clientTranId: str | None
  """Client transfer id."""
  asset: str | None
  """Asset."""
  amount: str | None
  """Amount."""
  fromAccountType: str | None
  """Source account type."""
  toAccountType: str | None
  """Destination account type."""
  fromSymbol: str | None
  """Source symbol."""
  toSymbol: str | None
  """Destination symbol."""
  status: str | None
  """Transfer status."""
  timestamp: datetime | None
  """Transfer timestamp."""

class UniversalTransferHistoryItem(TypedDict):
  """Universal transfer history page."""
  rows: list[RowsItem]
  """Transfer rows."""
  total: int | None
  """Total records."""

Response: type[list[UniversalTransferHistoryItem] | ErrorResponse] = list[UniversalTransferHistoryItem] | ErrorResponse # type: ignore
adapter = validator(Response)

class UniversalTransferHistory(AuthSpotMixin):
  async def universal_transfer_history(
    self,
    *,
    from_account_type: str,
    to_account_type: str,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    page: int | None = None,
    size: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[UniversalTransferHistoryItem]:
    """Returns universal transfer records between account types for the signed account.

    Args:
      from_account_type: Source account type filter.
      to_account_type: Destination account type filter.
      start_time: Start time in milliseconds.
      end_time: End time in milliseconds.
      page: Page number; default 1.
      size: Page size; max 100.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-user-universal-transfer-history)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if from_account_type is not None:
      params['fromAccountType'] = from_account_type
    if to_account_type is not None:
      params['toAccountType'] = to_account_type
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if page is not None:
      params['page'] = page
    if size is not None:
      params['size'] = size
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/transfer', params=params)
    return self.output(r.text, adapter, validate)

  async def universal_transfer_history_paged(self, *, from_account_type: str, to_account_type: str, start_time: Timestamp | None = None, end_time: Timestamp | None = None, size: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[list[UniversalTransferHistoryItem]]:
    """Yield pages from `universal_transfer_history` until the response reports the final page."""
    page = 1
    while True:
      response = await self.universal_transfer_history(from_account_type=from_account_type, to_account_type=to_account_type, start_time=start_time, end_time=end_time, size=size, timestamp=timestamp, page=page, validate=validate)
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
