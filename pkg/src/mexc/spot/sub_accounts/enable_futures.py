from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class EnableFuturesRequest(TypedDict):
  subAccount: NotRequired[str]
  """Sub-account name whose futures capability should be enabled."""

class EnableFuturesItem(TypedDict):
  """Sub-account futures enablement record."""
  subAccount: NotRequired[str | None]
  """Sub-account name."""
  isFuturesEnabled: NotRequired[bool | None]
  """Whether futures was enabled."""
  timestamp: NotRequired[str | datetime | None]
  """Response time."""

class EnableFuturesResponse(TypedDict):
  """Sub-account futures enablement result."""
  code: NotRequired[str | int | None]
  """Upstream result code when present."""
  message: NotRequired[str | None]
  """Upstream result message when present."""
  data: NotRequired[list[EnableFuturesItem]]
  """Enablement result records when present."""

Response: type[EnableFuturesResponse | ErrorResponse] = EnableFuturesResponse | ErrorResponse # type: ignore
adapter = validator(Response)

class EnableFutures(AuthSpotMixin):
  async def enable_futures(
    self,
    *,
    sub_account: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> EnableFuturesResponse:
    """Enables futures capability for a sub-account. The exact non-broker Spot endpoint is docs-ambiguous in the current official Spot V3 page.

    Args:
      sub_account: Sub-account name whose futures capability should be enabled. Parameter inferred from the requested path and official broker analogue because current Spot docs omit this exact operation.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#sub-account-endpoints)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if sub_account is not None:
      params['subAccount'] = sub_account
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/sub-account/futures', params=params)
    return self.output(r.text, adapter, validate)
