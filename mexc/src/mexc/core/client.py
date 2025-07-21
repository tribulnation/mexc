from dataclasses import dataclass, field
from functools import wraps
import httpx

MEXC_SPOT_API_BASE = 'https://api.mexc.com'
MEXC_FUTURES_API_BASE = 'https://contract.mexc.com'

@dataclass
class ClientMixin:
  spot_api_base: str = field(default=MEXC_SPOT_API_BASE, kw_only=True)
  futures_api_base: str = field(default=MEXC_FUTURES_API_BASE, kw_only=True)

  async def __aenter__(self):
    self._client = httpx.AsyncClient()
    return self
  
  async def __aexit__(self, *args):
    if self._client is not None:
      await self._client.aclose()
      self._client = None

  @property
  def client(self) -> httpx.AsyncClient:
    client = getattr(self, '_client', None)
    if client is None:
      raise RuntimeError('Please use as context manager: `async with ...: ...`')
    return client
  
  @staticmethod
  def with_client(fn):
    @wraps(fn)
    async def wrapper(self, *args, **kwargs):
      if getattr(self, '_client', None) is None:
        async with self:
          return await fn(self, *args, **kwargs)
      else:
        return await fn(self, *args, **kwargs)
      
    return wrapper

  @with_client
  async def request(
    self, method: str, path: str, params: dict | None = None, *,
    headers: dict | None = None, cookies: dict | None = None,
    base_url: str | None = None,
  ):
    base = base_url or self.spot_api_base
    return await self.client.request(method, base + path, params=params, headers={
      'User-Agent': 'trading-sdk',
      **(headers or {}),
    }, cookies=cookies)
