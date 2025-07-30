from typing_extensions import Literal
from dataclasses import dataclass
from decimal import Decimal
from trading_sdk.streams.depth import Depth as DepthTDK, Book
from mexc.sdk import SdkMixin

def level(limit: int | None) -> Literal[5, 10, 20]:
  if limit is None:
    return 20
  elif limit < 5:
    return 5
  elif limit < 10:
    return 10
  else:
    return 20

@dataclass
class Depth(DepthTDK, SdkMixin):
  async def depth(self, symbol: str, *, limit: int | None = None):
    async for book in self.client.streams.depth(symbol, level(limit)):
      yield Book(
        bids=[Book.Entry(price=Decimal(e.price), qty=Decimal(e.qty)) for e in book.bids],
        asks=[Book.Entry(price=Decimal(e.price), qty=Decimal(e.qty)) for e in book.asks]
      )
