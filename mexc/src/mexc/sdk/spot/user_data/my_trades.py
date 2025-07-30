from typing_extensions import Sequence, AsyncIterable
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from trading_sdk.spot.user_data.my_trades import MyTrades as MyTradesTDK, Trade
from mexc.api.spot.user_data import MyTrades as Client
from mexc.core import timestamp
from mexc.sdk import SdkMixin

async def _my_trades(
  client: Client, symbol: str, *, limit: int | None = None,
  start: datetime | None = None, end: datetime | None = None
) -> list[Trade]:
  r = await client.my_trades(symbol, limit=limit, start=start, end=end)
  match r:
    case list(trades):
      return [
        Trade(
          id=t['id'],
          price=Decimal(t['price']),
          qty=Decimal(t['qty']),
          time=timestamp.parse(t['time']),
          side='BUY' if t['isBuyer'] else 'SELL',
          maker=t['isMaker'],
        )
        for t in trades
      ]
    case err:
      raise RuntimeError(err)

async def _paginate_trades_forward(
  client: Client, symbol: str, *, limit: int | None = None,
  start: datetime, end: datetime | None = None,
) -> AsyncIterable[Sequence[Trade]]:
  """Paginate trades forwards from the `start`"""
  ids = set()
  while end is None or start < end:
    trades = await _my_trades(client, symbol, limit=limit, start=start, end=end)
    new_trades = [t for t in reversed(trades) if t.id not in ids] # ordered by time
    if not new_trades:
      break
    ids.update(t.id for t in new_trades)
    yield new_trades
    start = new_trades[-1].time

async def _paginate_trades_backward(
  client: Client, symbol: str, *, limit: int | None = None,
  start: datetime | None = None, end: datetime,
) -> AsyncIterable[Sequence[Trade]]:
  """Paginate trades backwards from the `end`"""
  ids = set()
  while start is None or start < end:
    trades = await _my_trades(client, symbol, limit=limit, start=start, end=end)
    new_trades = [t for t in trades if t.id not in ids] # ordered backwards by time
    if not new_trades:
      break
    ids.update(t.id for t in new_trades)
    yield new_trades
    end = new_trades[-1].time

@dataclass
class MyTrades(MyTradesTDK, SdkMixin):
  async def my_trades(
    self, symbol: str, *, limit: int | None = None,
    start: datetime | None = None, end: datetime | None = None
  ) -> AsyncIterable[Sequence[Trade]]:
    spot = self.client.spot
    if start and end:
      async for trades in _paginate_trades_forward(spot, symbol, start=start, end=end, limit=limit):
        yield trades
    elif start:
      async for trades in _paginate_trades_forward(spot, symbol, start=start, limit=limit):
        yield trades
    elif end:
      async for trades in _paginate_trades_backward(spot, symbol, end=end, limit=limit):
        yield trades
    else:
      async for trades in _paginate_trades_backward(spot, symbol, end=datetime.now(), limit=limit):
        yield trades
