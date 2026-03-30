from typing_extensions import AsyncIterable
from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.core import validator, TypedDict
from mexc.futures.streams.core import StreamsMixin, Reply

class Ticker(TypedDict):
  ...

validate_response = validator(list[Ticker])

@dataclass
class Tickers(StreamsMixin):
  async def tickers(self, *, validate: bool = True) -> Stream[list[Ticker], Reply, Reply]:
    """Subscribe to all future instrument tickers.

    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://mexcdevelop.github.io/apidocs/contract_v1_en/#filter-subscription)
    """
    stream = await self.ws.subscribe('tickers')
    async def parsed_stream():
      async for msg in stream:
        yield validate_response(msg) if self.validate(validate) else msg
    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
