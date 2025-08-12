from abc import abstractmethod
from dataclasses import dataclass, field
import asyncio
from .base import RpcSocketClient, Restart

@dataclass
class SerialRpcSocketClient(RpcSocketClient):
  """Serial request/response socket client. It uses a lock to serialize requests and responses."""
  lock: asyncio.Lock = field(default_factory=asyncio.Lock)
  replies: asyncio.Queue = field(default_factory=asyncio.Queue)

  def on_msg(self, msg: str | bytes | Restart):
    self.replies.put_nowait(msg)

  @abstractmethod
  async def send(self, msg):
    ...

  async def request(self, msg):
    while True:
      async with self.lock:
        await self.send(msg)
        res = await self.replies.get()
        if isinstance(res, Restart):
          continue
        return res
