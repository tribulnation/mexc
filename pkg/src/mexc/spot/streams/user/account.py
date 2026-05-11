from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import UserStreamsMixin, Reply
from mexc.spot.streams.core.proto import PrivateAccountV3Api

@dataclass
class Account(UserStreamsMixin):
  async def account(self) -> Stream[PrivateAccountV3Api, Reply, Reply]:
    """
    Subscribe to spot account balance updates.

    References:
      - [MEXC spot WebSocket user streams](https://www.mexc.com/api-docs/spot-v3/websocket-user-data-streams#spot-account-update)
    """
    stream = await self.authed_subscribe('spot@private.account.v3.api.pb')

    async def parsed_stream():
      async for proto in stream:
        if proto.private_account is not None:
          yield proto.private_account

    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
