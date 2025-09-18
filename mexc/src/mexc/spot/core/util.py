from typing_extensions import TypedDict, Mapping, TypeGuard
from dataclasses import dataclass, field
from mexc.core import HttpMixin, ValidationMixin
from .auth import AuthHttpMixin

MEXC_SPOT_API_BASE = 'https://api.mexc.com'

@dataclass
class SpotMixin(HttpMixin, ValidationMixin):
  base_url: str = field(default=MEXC_SPOT_API_BASE, kw_only=True)

@dataclass
class AuthSpotMixin(AuthHttpMixin, ValidationMixin):
  base_url: str = field(default=MEXC_SPOT_API_BASE, kw_only=True)

class ErrorResponse(TypedDict):
  msg: str
  code: int

def is_error_response(r) -> TypeGuard[ErrorResponse]:
  return isinstance(r, Mapping) and 'msg' in r and 'code' in r