from typing_extensions import Any
from abc import abstractmethod
from dataclasses import dataclass, field
import asyncio
from .base import RpcSocketClient, Restart

@dataclass
class MultiplexRpcSocketClient(RpcSocketClient):
  """Multiplexed request/response socket client. It uses IDs to identify requests and responses."""
  replies: dict[int, asyncio.Future[str|bytes|Restart]] = field(default_factory=dict)
  counter: int = 0

  @abstractmethod
  def parse_response(self, msg: str | bytes) -> tuple[int, Any]:
    ...

  def on_msg(self, msg: str | bytes | Restart):
    if isinstance(msg, Restart):
      for future in self.replies.values():
        future.set_result(Restart())
      self.replies.clear()
    else:
      id, result = self.parse_response(msg)
      self.replies[id].set_result(result)

  @abstractmethod
  async def send(self, id: int, msg):
    ...

  async def request(self, msg):
    id = self.counter
    self.counter += 1
    while True:
      self.replies[id] = asyncio.Future()
      await self.send(id, msg)
      res = await self.replies[id]
      del self.replies[id]
      if isinstance(res, Restart):
        continue
      return res
