from dataclasses import dataclass
from typing_extensions import TypedDict, NotRequired, Literal
from pydantic import BaseModel
from mexc.core import UIMixin

class Data(BaseModel):
  oldOrderId: str
  newOrderId: str

class Response(BaseModel):
  code: int
  msg: str
  timestamp: int
  data: Data | None = None

class EditOrder(UIMixin):
  async def edit_order(
    self, *, orderId: str, price: str, quantity: str,
    validate: bool = True,
  ) -> Response:
    r = await self.ui_request('POST', '/api/platform/spot/order/modify', json={
      'orderId': orderId,
      'quantity': quantity,
      'price': price,
    })
    return Response.model_validate_json(r.text) if validate else r.json()