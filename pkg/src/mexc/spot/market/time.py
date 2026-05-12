from datetime import datetime
from typing_extensions import TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

class TimeResponse(TypedDict):
  serverTime: datetime
  """Server timestamp in milliseconds."""

Response: type[TimeResponse | ErrorResponse] = TimeResponse | ErrorResponse # type: ignore
adapter = validator(Response)

class Time(SpotMixin):
  async def time(self, *, validate: bool | None = None) -> TimeResponse:
    """Return the current MEXC spot server time.

    Args:
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#check-server-time)
    """
    params = {}
    r = await self.request('GET', '/api/v3/time')
    return self.output(r.text, adapter, validate)
