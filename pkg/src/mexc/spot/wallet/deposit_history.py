from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Deposit record."""
  amount: NotRequired[str | None]
  """Deposit amount."""
  coin: NotRequired[str | None]
  """Asset deposited."""
  network: NotRequired[str | None]
  """Deposit network."""
  status: NotRequired[int | None]
  """Deposit status code."""
  address: NotRequired[str | None]
  """Deposit address."""
  addressTag: NotRequired[str | None]
  """Deposit address tag."""
  txId: NotRequired[str | None]
  """Blockchain transaction id."""
  insertTime: NotRequired[datetime | None]
  """Deposit insert time."""
  unlockConfirm: NotRequired[str | None]
  """Required confirmations to unlock."""
  confirmTimes: NotRequired[str | None]
  """Observed confirmations."""
  memo: NotRequired[str | None]
  """Deposit memo."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class DepositHistory(AuthSpotMixin):
  async def deposit_history(
    self,
    *,
    coin: str | None = None,
    status: str | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    limit: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Returns deposit records for the signed account, optionally filtered by coin, status, and time window.

    Args:
      coin: Asset filter.
      status: Deposit status filter.
      start_time: Start time in milliseconds; defaults to seven days ago.
      end_time: End time in milliseconds; defaults to current time.
      limit: Maximum records to return; max 1000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#deposit-history-supporting-network"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if coin is not None:
      params['coin'] = coin
    if status is not None:
      params['status'] = status
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if limit is not None:
      params['limit'] = limit
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/deposit/hisrec', params=params)
    return self.output(r.text, adapter, validate)
