from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class ConvertDetailsItem(TypedDict):
  """Conversion detail."""
  id: NotRequired[str | None]
  """Conversion id."""
  convert: NotRequired[str | None]
  """Converted MX amount."""
  fee: NotRequired[str | None]
  """Fee amount."""
  amount: NotRequired[str | None]
  """Source asset amount."""
  time: NotRequired[datetime | None]
  """Conversion time."""
  asset: NotRequired[str | None]
  """Source asset."""

class DataItem(TypedDict):
  """Dust conversion group."""
  totalConvert: NotRequired[str | None]
  """Total converted MX amount."""
  totalFee: NotRequired[str | None]
  """Total fee amount."""
  convertTime: NotRequired[datetime | None]
  """Conversion time."""
  convertDetails: NotRequired[list[ConvertDetailsItem]]
  """Conversion detail rows."""

class Response200(TypedDict):
  """Dust log response."""
  data: NotRequired[list[DataItem]]
  """Dust conversion groups."""
  totalRecords: NotRequired[int | None]
  """Total records."""
  page: NotRequired[int | None]
  """Current page."""
  totalPageNum: NotRequired[int | None]
  """Total pages."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class DustLog(AuthSpotMixin):
  async def dust_log(
    self,
    *,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    page: int | None = None,
    limit: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns historical dust conversion records for the signed account.

    Args:
      start_time: Start time in milliseconds.
      end_time: End time in milliseconds.
      page: Page number; default 1.
      limit: Page size; max 1000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#dustlog"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
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
    r = await self.signed_request('GET', '/api/v3/capital/convert', params=params)
    return self.output(r.text, adapter, validate)

  async def dust_log_paged(self, *, start_time: Timestamp | None = None, end_time: Timestamp | None = None, limit: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `dust_log` until the response reports the final page."""
    page = 1
    while True:
      response = await self.dust_log(start_time=start_time, end_time=end_time, limit=limit, timestamp=timestamp, page=page, validate=validate)
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
