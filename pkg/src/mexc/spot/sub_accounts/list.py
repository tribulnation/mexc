from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Sub-account record."""
  subAccount: NotRequired[str | None]
  """Sub-account name."""
  isFreeze: NotRequired[bool | str | None]
  """Whether the sub-account is frozen."""
  createTime: NotRequired[datetime | None]
  """Sub-account creation time in milliseconds."""
  uid: NotRequired[str | int | None]
  """Sub-account user id."""

class Response200(TypedDict):
  """Sub-account list wrapper."""
  subAccounts: NotRequired[list[Item]]
  """Sub-account records."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class List(AuthSpotMixin):
  async def list(
    self,
    *,
    sub_account: str | None = None,
    is_freeze: str | None = None,
    page: int | None = None,
    limit: int | None = None,
    timestamp: Timestamp | None = None,
    recv_window: int | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns sub-account records visible to the signed master account.

    Args:
      sub_account: Optional sub-account name filter.
      is_freeze: Optional freeze-state filter, expressed as true or false.
      page: Result page number. Defaults to 1.
      limit: Maximum records to return. Defaults to 10 and may not exceed 200.
      timestamp: Signed request timestamp in milliseconds.
      recv_window: Optional signed-request validity window in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-sub-account-list-for-master-account"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if sub_account is not None:
      params['subAccount'] = sub_account
    if is_freeze is not None:
      params['isFreeze'] = is_freeze
    if page is not None:
      params['page'] = page
    if limit is not None:
      params['limit'] = limit
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    if recv_window is not None:
      params['recvWindow'] = recv_window
    r = await self.signed_request('GET', '/api/v3/sub-account/list', params=params)
    return self.output(r.text, adapter, validate)

  async def list_paged(self, *, sub_account: str | None = None, is_freeze: str | None = None, limit: int | None = None, timestamp: Timestamp | None = None, recv_window: int | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `list` until the response reports the final page."""
    page = 1
    while True:
      response = await self.list(sub_account=sub_account, is_freeze=is_freeze, limit=limit, timestamp=timestamp, recv_window=recv_window, page=page, validate=validate)
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
