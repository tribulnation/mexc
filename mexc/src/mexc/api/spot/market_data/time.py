from typing_extensions import TypedDict
from pydantic import RootModel
from mexc.core import ClientMixin, ApiError

class ServerTime(TypedDict):
  serverTime: int

class Response(RootModel):
  root: ServerTime | ApiError

class Time(ClientMixin):
  async def time(self, validate: bool = True) -> ApiError | ServerTime:
    """Get the server time.
    
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#check-server-time)
    """
    r = await self.request('GET', '/api/v3/time')
    return Response.model_validate_json(r.text).root if validate else r.json()