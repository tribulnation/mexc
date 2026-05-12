from datetime import datetime
from typing_extensions import AsyncIterator, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class TransferHistoryResponse(TypedDict):
  """Sub-account transfer history record."""
  tranId: str | int | None
  """Transfer id."""
  fromAccount: str | None
  """Source account name."""
  toAccount: str | None
  """Destination account name."""
  clientTranId: str | None
  """Client transfer id."""
  asset: str | None
  """Transferred asset."""
  amount: str | None
  """Transferred amount."""
  fromAccountType: str | None
  """Source account type."""
  toAccountType: str | None
  """Destination account type."""
  fromSymbol: str | None
  """Source symbol or account label."""
  toSymbol: str | None
  """Destination symbol or account label."""
  status: str | None
  """Transfer status."""
  timestamp: datetime | None
  """Transfer time in milliseconds."""

Response: type[TransferHistoryResponse | ErrorResponse] = TransferHistoryResponse | ErrorResponse # type: ignore
adapter = validator(Response)

class TransferHistory(AuthSpotMixin):
  async def transfer_history(
    self,
    *,
    from_account: str | None = None,
    to_account: str | None = None,
    from_account_type: str,
    to_account_type: str,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    page: int | None = None,
    limit: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> TransferHistoryResponse:
    """Returns transfer records between the master account and sub-accounts.

    Args:
      from_account: Source account filter. Defaults to the master account when omitted.
      to_account: Destination account filter. Defaults to the master account when omitted.
      from_account_type: Source account type filter, documented as SPOT or FUTURES.
      to_account_type: Destination account type filter, documented as SPOT or FUTURES.
      start_time: Start time filter in milliseconds.
      end_time: End time filter in milliseconds.
      page: Result page number. Defaults to 1.
      limit: Maximum records to return. Defaults to 500 and may not exceed 500.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-universal-transfer-history-for-master-account)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if from_account is not None:
      params['fromAccount'] = from_account
    if to_account is not None:
      params['toAccount'] = to_account
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
    if limit is not None:
      params['limit'] = limit
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/sub-account/universalTransfer', params=params)
    return self.output(r.text, adapter, validate)

  async def transfer_history_paged(self, *, from_account: str | None = None, to_account: str | None = None, from_account_type: str, to_account_type: str, start_time: Timestamp | None = None, end_time: Timestamp | None = None, limit: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[TransferHistoryResponse]:
    """Yield pages from `transfer_history` until the response reports the final page."""
    page = 1
    while True:
      response = await self.transfer_history(from_account=from_account, to_account=to_account, from_account_type=from_account_type, to_account_type=to_account_type, start_time=start_time, end_time=end_time, limit=limit, timestamp=timestamp, page=page, validate=validate)
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
