from typing_extensions import Sequence, AsyncIterable
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from trading_sdk.types import ApiError
from trading_sdk.market.user_data.my_trades import SpotMyTrades, Trade

from mexc.spot.user_data import MyTrades as Client
from mexc.core import timestamp
from mexc.sdk.core import SdkMixin, wrap_exceptions, spot_name

async def _my_trades(
  client: Client, instrument: str, *, recvWindow: int | None = 60000,
  start: datetime | None = None, end: datetime | None = None
) -> list[Trade]:
  r = await client.my_trades(instrument, start=start, end=end, recvWindow=recvWindow)
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
          fee=Trade.Fee(
            asset=a,
            amount=Decimal(c),
          ) if (a := t.get('commissionAsset')) and (c := t.get('commission')) else None,
        )
        for t in trades
      ]
    case err:
      raise ApiError(err)

async def _paginate_trades_forward(
  client: Client, instrument: str, *, recvWindow: int | None = None,
  start: datetime, end: datetime | None = None,
) -> AsyncIterable[Sequence[Trade]]:
  """Paginate trades forwards from the `start`"""
  ids = set()
  while end is None or start < end:
    trades = await _my_trades(client, instrument, start=start, end=end)
    new_trades = [t for t in reversed(trades) if t.id not in ids] # ordered by time
    if not new_trades:
      break
    ids.update(t.id for t in new_trades)
    yield new_trades
    start = new_trades[-1].time

async def _paginate_trades_backward(
  client: Client, instrument: str, *, recvWindow: int | None = None,
  start: datetime | None = None, end: datetime,
) -> AsyncIterable[Sequence[Trade]]:
  """Paginate trades backwards from the `end`"""
  ids = set()
  while start is None or start < end:
    trades = await _my_trades(client, instrument, start=start, end=end)
    new_trades = [t for t in trades if t.id not in ids] # ordered backwards by time
    if not new_trades:
      break
    ids.update(t.id for t in new_trades)
    yield new_trades
    end = new_trades[-1].time

@dataclass
class MyTrades(SpotMyTrades, SdkMixin):
  @wrap_exceptions
  async def my_trades(
    self, instrument: str, /, *,
    start: datetime | None = None, end: datetime | None = None
  ) -> AsyncIterable[Sequence[Trade]]:
    spot = self.client.spot
    if start and end:
      async for trades in _paginate_trades_forward(spot, instrument, start=start, end=end, recvWindow=self.recvWindow):
        yield trades
    elif start:
      async for trades in _paginate_trades_forward(spot, instrument, start=start, recvWindow=self.recvWindow):
        yield trades
    elif end:
      async for trades in _paginate_trades_backward(spot, instrument, end=end, recvWindow=self.recvWindow):
        yield trades
    else:
      async for trades in _paginate_trades_backward(spot, instrument, end=datetime.now(), recvWindow=self.recvWindow):
        yield trades


  async def spot_my_trades(self, base: str, quote: str, /, *, start: datetime | None = None, end: datetime | None = None) -> AsyncIterable[Sequence[Trade]]:
    instrument = spot_name(base, quote)
    async for trades in self.my_trades(instrument, start=start, end=end):
      yield trades