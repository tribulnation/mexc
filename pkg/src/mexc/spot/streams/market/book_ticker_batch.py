from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import StreamsMixin, Reply
from mexc.spot.streams.core.proto import PublicBookTickerBatchV3Api

def channel_name(symbol: str):
  return f'spot@public.bookTicker.batch.v3.api.pb@{symbol}'

@dataclass
class BookTickerBatch(StreamsMixin):
  async def book_ticker_batch(self, symbol: str) -> Stream[PublicBookTickerBatchV3Api, Reply, Reply]:
    """
    Subscribe to batch best bid/ask updates for a spot symbol.

    Args:
      symbol: Spot symbol, for example `BTCUSDT`.

    References:
      - [MEXC spot WebSocket market streams](https://www.mexc.com/api-docs/spot-v3/websocket-market-streams#bookticker-streams)
    """
    stream = await self.subscribe(channel_name(symbol))

    async def parsed_stream():
      async for proto in stream:
        if proto.public_book_ticker_batch is not None:
          yield proto.public_book_ticker_batch

    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
