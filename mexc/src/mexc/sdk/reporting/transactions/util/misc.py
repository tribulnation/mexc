from typing_extensions import Literal, Iterable, Protocol
from datetime import datetime, timezone

from trading_sdk.reporting import Operation

def ensure_datetime(x) -> datetime:
  return x if isinstance(x, datetime) else datetime.fromisoformat(str(x))