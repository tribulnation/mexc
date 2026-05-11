from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Withdrawal address."""
  coin: NotRequired[str | None]
  """Asset."""
  network: NotRequired[str | None]
  """Network."""
  address: NotRequired[str | None]
  """Withdrawal address."""
  addressTag: NotRequired[str | None]
  """Address label/tag."""
  memo: NotRequired[str | None]
  """Address memo."""

class Response200(TypedDict):
  """Withdrawal address lookup response."""
  data: NotRequired[list[Item]]
  """Withdrawal addresses."""
  totalRecords: NotRequired[int | None]
  """Total records."""
  page: NotRequired[int | None]
  """Current page."""
  totalPageNum: NotRequired[int | None]
  """Total pages."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class WithdrawAddress(AuthSpotMixin):
  async def withdraw_address(
    self,
    *,
    coin: str | None = None,
    page: int | None = None,
    limit: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns saved withdrawal addresses for the signed account.

    Args:
      coin: Asset filter.
      page: Page number; default 1.
      limit: Records per page.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#withdraw-address-supporting-network"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if coin is not None:
      params['coin'] = coin
    if page is not None:
      params['page'] = page
    if limit is not None:
      params['limit'] = limit
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/withdraw/address', params=params)
    return self.output(r.text, adapter, validate)

  async def withdraw_address_paged(self, *, coin: str | None = None, limit: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `withdraw_address` until the response reports the final page."""
    page = 1
    while True:
      response = await self.withdraw_address(coin=coin, limit=limit, timestamp=timestamp, page=page, validate=validate)
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
