from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Rebate record."""
  spot: NotRequired[str]
  """Spot rebate amount in USDT."""
  futures: NotRequired[str]
  """Futures rebate amount in USDT."""
  total: NotRequired[str]
  """Total rebate amount in USDT."""
  uid: NotRequired[str]
  """Invitee user id."""
  account: NotRequired[str]
  """Masked invitee account."""
  inviteTime: NotRequired[datetime]
  """Invite time in milliseconds."""

class Response200(TypedDict):
  """Paginated rebate response."""
  page: NotRequired[int]
  """Current result page."""
  totalRecords: NotRequired[int]
  """Total number of matching records."""
  totalPageNum: NotRequired[int]
  """Total number of result pages."""
  data: NotRequired[list[Item]]
  """Result records for the page."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class History(AuthSpotMixin):
  async def history(
    self,
    *,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    page: int | None = None,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns aggregated rebate history for users invited by the signed account.

    Args:
      start_time: Start time in milliseconds.
      end_time: End time in milliseconds.
      page: Result page; defaults to 1.
      recv_window: Optional receive window in milliseconds.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#get-rebate-history-records"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if page is not None:
      params['page'] = page
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/rebate/taxQuery', params=params)
    return self.output(r.text, adapter, validate)

  async def history_paged(self, *, start_time: Timestamp | None = None, end_time: Timestamp | None = None, recv_window: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `history` until the response reports the final page."""
    page = 1
    while True:
      response = await self.history(start_time=start_time, end_time=end_time, recv_window=recv_window, timestamp=timestamp, page=page, validate=validate)
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
