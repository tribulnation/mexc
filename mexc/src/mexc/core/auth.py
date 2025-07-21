from dataclasses import dataclass
from urllib.parse import urlencode, quote
import hashlib
import hmac
from .client import ClientMixin

def sign(query_string: str, *, secret: str) -> str:
  return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def encode_query(obj) -> str:
  import json
  return (json.dumps(obj, separators=(',', ':'))) # binance can't cope with spaces, it seems

@dataclass
class AuthedMixin(ClientMixin):
  api_key: str
  api_secret: str

  @property
  def headers(self) -> dict:
    return { 'X-MEXC-APIKEY': self.api_key }

  def sign(self, query_string: str) -> str:
    return sign(query_string, secret=self.api_secret)
  
  def signed_query(self, params: dict) -> str:
    def fix(v):
      # fix bools, which would show otherwise as "hello=True" instead of "hello=true"
      if isinstance(v, bool):
        return str(v).lower()
      else:
        return v
    fixed_params = [(k, fix(v)) for k, v in params.items()]
    query = urlencode(fixed_params, quote_via=quote)
    return query + '&signature=' + self.sign(query)
  
  async def authed_request(self, method: str, path: str, params: dict = {}, *, base_url: str | None = None):
    return await self.request(method, path, headers=self.headers, params=params, base_url=base_url)
  
  async def signed_request(self, method: str, path: str, params: dict = {}, *, base_url: str | None = None):
    return await self.request(method, path + '?' + self.signed_query(params), headers=self.headers, base_url=base_url)