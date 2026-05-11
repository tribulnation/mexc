from typing_extensions import Literal
from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import StreamsMixin, Reply
from mexc.spot.streams.core.proto import PublicAggreBookTickerV3Api

Aggregation = Literal['100ms', '10ms']

def channel_name(symbol: str, aggregation: Aggregation):
  return f'spot@public.aggre.bookTicker.v3.api.pb@{aggregation}@{symbol}'

@dataclass
class BookTicker(StreamsMixin):
  async def book_ticker(
    self, symbol: str, aggregation: Aggregation = '100ms',
  ) -> Stream[PublicAggreBookTickerV3Api, Reply, Reply]:
    """
    Subscribe to best bid/ask updates for a spot symbol.

    Args:
      symbol: Spot symbol, for example `BTCUSDT`.
      aggregation: Update aggregation interval.

    References:
      - [MEXC spot WebSocket market streams](https://www.mexc.com/api-docs/spot-v3/websocket-market-streams#bookticker-streams)
    """
    stream = await self.subscribe(channel_name(symbol, aggregation))

    async def parsed_stream():
      async for proto in stream:
        if proto.public_aggre_book_ticker is not None:
          yield proto.public_aggre_book_ticker

    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
