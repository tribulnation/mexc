from typing_extensions import Literal
from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import StreamsMixin, Reply
from mexc.spot.streams.core.proto import PublicSpotKlineV3Api

Interval = Literal['Min1', 'Min5', 'Min15', 'Min30', 'Min60', 'Hour4', 'Hour8', 'Day1', 'Week1', 'Month1']

def channel_name(symbol: str, interval: Interval):
  return f'spot@public.kline.v3.api.pb@{symbol}@{interval}'

@dataclass
class Candles(StreamsMixin):
  async def candles(self, symbol: str, interval: Interval) -> Stream[PublicSpotKlineV3Api, Reply, Reply]:
    """Subscribe to klines (candles) for a given symbol.
    
    - `symbol`: The symbol being traded, e.g. `BTCUSDT`.
    - `interval`: The interval of the klines (default: 1m).

    > [MEXC API docs](https://www.mexc.com/api-docs/spot-v3/websocket-market-streams#k-line-streams)
    """
    stream = await self.subscribe(channel_name(symbol, interval))
    async def parsed_stream():
      async for proto in stream:
        if proto.public_spot_kline is not None:
          yield proto.public_spot_kline
    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
