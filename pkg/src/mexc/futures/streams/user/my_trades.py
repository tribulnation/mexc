from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from typed_core.ws.streams import Stream
from mexc.core import validator, TypedDict
from mexc.futures.streams.core import AuthedStreamsMixin, Reply

class Side(Enum):
  open_long = 1
  close_short = 2
  open_short = 3
  close_long = 4

class Deal(TypedDict):
  category: int
  externalOid: str
  fee: Decimal
  feeCurrency: str
  id: str
  isSelf: bool
  orderId: str
  positionMode: int
  price: Decimal
  profit: Decimal
  side: Side
  symbol: str
  taker: bool
  timestamp: int
  vol: Decimal
  """Base asset amount, in volume units"""

validate_response = validator(Deal)

@dataclass
class MyTrades(AuthedStreamsMixin):
  async def my_trades(self, *, validate: bool = True) -> Stream[Deal, None, None]:
    """Subscribe to your future trades.

    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://www.mexc.com/api-docs/futures/websocket-api#fill-details)
    """
    stream = await self.auth_ws.subscribe('personal.order.deal')
    async def parsed_stream():
      async for msg in stream:
        yield validate_response(msg) if self.validate(validate) else msg
    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
