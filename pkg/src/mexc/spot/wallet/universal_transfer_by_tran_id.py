from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Universal transfer detail."""
  tranId: NotRequired[str | None]
  """Transfer id."""
  clientTranId: NotRequired[str | None]
  """Client transfer id."""
  asset: NotRequired[str | None]
  """Asset."""
  amount: NotRequired[str | None]
  """Amount."""
  fromAccountType: NotRequired[str | None]
  """Source account type."""
  toAccountType: NotRequired[str | None]
  """Destination account type."""
  symbol: NotRequired[str | None]
  """Symbol."""
  status: NotRequired[str | None]
  """Transfer status."""
  timestamp: NotRequired[datetime | None]
  """Transfer timestamp."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class UniversalTransferByTranId(AuthSpotMixin):
  async def universal_transfer_by_tran_id(
    self,
    *,
    tran_id: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns a single universal transfer record by transfer id.

    Args:
      tran_id: Transfer id.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-user-universal-transfer-history-by-tranid"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if tran_id is not None:
      params['tranId'] = tran_id
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/transfer/tranId', params=params)
    return self.output(r.text, adapter, validate)
