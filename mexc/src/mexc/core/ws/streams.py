from typing_extensions import Any
from abc import abstractmethod
from dataclasses import dataclass, field
import asyncio
from .base import SocketClient, Restart

@dataclass
class StreamsSocketClient(SocketClient):
  """Multiplexed streams socket client, allowing subscription to multiple channels."""
  subscribers: dict[str, asyncio.Queue] = field(default_factory=dict)

  @abstractmethod
  async def request_subscription(self, channel: str, params=None):
    ...

  @abstractmethod
  async def request_unsubscription(self, channel: str):
    ...

  @abstractmethod
  def parse_msg(self, msg: str | bytes) -> tuple[str, Any]:
    ...

  def on_msg(self, msg: str | bytes | Restart):
    if isinstance(msg, Restart):
      for queue in self.subscribers.values():
        queue.put_nowait(Restart())
    else:
      channel, data = self.parse_msg(msg)
      if channel in self.subscribers:
        self.subscribers[channel].put_nowait(data)

  async def subscribe(self, channel: str, params=None):
    self.subscribers[channel] = asyncio.Queue()
    while True:
      await self.request_subscription(channel, params)
      while True:
        if (queue := self.subscribers.get(channel)) is None:
          return # unsubscribed
        val = await queue.get()
        if isinstance(val, Restart):
          await self.started.wait()
          break
        else:
          yield val

  async def unsubscribe(self, channel: str):
    del self.subscribers[channel]
    await self.request_unsubscription(channel)
    