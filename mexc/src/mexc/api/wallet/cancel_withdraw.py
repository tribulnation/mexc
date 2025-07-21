from typing_extensions import TypedDict
from pydantic import RootModel
from mexc.core import AuthedMixin, timestamp as ts, ApiError

class WithdrawId(TypedDict):
  id: str

class Response(RootModel):
  root: WithdrawId | ApiError

class CancelWithdraw(AuthedMixin):
  async def cancel_withdraw(
    self, id: str, *,
    timestamp: int | None = None, validate: bool = True,
  ) -> ApiError | WithdrawId:
    """Cancel a withdrawal, given its ID.
    
    - `id`: The ID of the withdrawal to cancel. Will be returned by the `withdraw` endpoint.
    - `timestamp`: The timestamp for the request, in milliseconds (default: now).
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#cancel-withdraw)
    """
    params = {
      'id': id, 'timestamp': timestamp or ts.now(),
    }
    r = await self.signed_request('DELETE', '/api/v3/capital/withdraw', params)
    return Response.model_validate_json(r.text).root if validate else r.json()
