from typing_extensions import TypedDict
from mexc.core import UIMixin, lazy_validator, DEFAULT_VALIDATE

class Data(TypedDict):
  oldOrderId: str
  newOrderId: str

class Response(TypedDict):
  code: int
  msg: str
  timestamp: int
  data: Data | None

validate_response = lazy_validator(Response)

class EditOrder(UIMixin):
  async def edit_order(
    self, *, orderId: str, price: str, quantity: str,
    validate: bool = DEFAULT_VALIDATE,
  ) -> Response:
    r = await self.ui_request('POST', '/api/platform/spot/order/modify', json={
      'orderId': orderId,
      'quantity': quantity,
      'price': price,
    })
    return validate_response(r.text) if validate else r.json()