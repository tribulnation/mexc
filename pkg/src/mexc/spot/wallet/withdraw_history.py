from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Withdrawal record."""
  id: NotRequired[str | None]
  """Withdrawal id."""
  txId: NotRequired[str | None]
  """Blockchain transaction id."""
  coin: NotRequired[str | None]
  """Asset withdrawn."""
  network: NotRequired[str | None]
  """Withdrawal network."""
  address: NotRequired[str | None]
  """Withdrawal address."""
  amount: NotRequired[str | None]
  """Withdrawal amount."""
  transferType: NotRequired[int | None]
  """Transfer type; outside or inside transfer."""
  status: NotRequired[int | None]
  """Withdrawal status code."""
  transactionFee: NotRequired[str | None]
  """Withdrawal fee."""
  applyTime: NotRequired[datetime | None]
  """Apply time."""
  remark: NotRequired[str | None]
  """Remark."""
  memo: NotRequired[str | None]
  """Memo."""
  transHash: NotRequired[str | None]
  """Transaction hash."""
  updateTime: NotRequired[datetime | None]
  """Update time."""
  coinId: NotRequired[str | None]
  """Asset id."""
  vcoinId: NotRequired[str | None]
  """Currency id."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class WithdrawHistory(AuthSpotMixin):
  async def withdraw_history(
    self,
    *,
    coin: str | None = None,
    status: str | None = None,
    limit: int | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Returns withdrawal records for the signed account, optionally filtered by coin, status, and time window.

    Args:
      coin: Asset filter.
      status: Withdrawal status filter.
      limit: Maximum records to return; max 1000.
      start_time: Start time in milliseconds; defaults to seven days ago.
      end_time: End time in milliseconds; defaults to current time.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#withdraw-history-supporting-network"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if coin is not None:
      params['coin'] = coin
    if status is not None:
      params['status'] = status
    if limit is not None:
      params['limit'] = limit
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/withdraw/history', params=params)
    return self.output(r.text, adapter, validate)
