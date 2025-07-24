from decimal import Decimal
from trading_sdk.spot.user_data.open_orders import OpenOrders as OpenOrdersTDK, OrderState
from mexc.api.spot.user_data import OpenOrders as Client
from mexc.core import timestamp
from mexc.sdk import SdkMixin

class OpenOrders(OpenOrdersTDK, SdkMixin[Client]):
  Client = Client

  async def open_orders(self, symbol: str) -> list[OrderState]:
    r = await self.client.open_orders(symbol)
    match r:
      case list(orders):
        return [
          OrderState(
            id=o['orderId'],
            price=Decimal(o['price']),
            quantity=Decimal(o['origQty']),
            filled_quantity=Decimal(o['executedQty']),
            time=timestamp.parse(o['time']),
            side=o['side'],
          )
          for o in orders
        ]
      case err:
        raise RuntimeError(err)
