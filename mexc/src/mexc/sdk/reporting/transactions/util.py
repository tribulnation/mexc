from typing_extensions import TypedDict, Literal, Mapping, Any, Iterable, Protocol
import re
from datetime import datetime, timezone
import pandas as pd

from trading_sdk.reporting import Operation

class Module(Protocol):
  matching_mode: Literal['eq', 'ge']

  def parse(self, path: str, tz: timezone, /, *, skip_zero_changes: bool = True) -> Iterable[Operation]:
    ...

class Details(TypedDict):
  source: Literal['spot', 'futures']
  type: str

def ensure_datetime(x) -> datetime:
  return x if isinstance(x, datetime) else datetime.fromisoformat(str(x))

Schema = Mapping[str|re.Pattern, type|re.Pattern]

def find_key(d: Mapping[str, Any], key: str | re.Pattern) -> str | None:
  if isinstance(key, str):
    if key in d:
      return key
  else:
    for k in d.keys():
      if key.match(k):
        return k

def validate_schema(df: pd.DataFrame, schema: Schema):
  for expected_key, expected_type in schema.items():
    key = find_key(df.dtypes, expected_key)
    if key is None:
      raise ValueError(f'Column "{expected_key}" not found')
    
    if isinstance(expected_type, re.Pattern):
      ok = df[key].astype(str).str.match(expected_type).all()
      if not ok:
        raise ValueError(f'Column "{expected_key}" has invalid values (expected it to match {expected_type.pattern})')
    elif expected_type is not Any and len(df) > 0:
      row = df.iloc[0]
      if not isinstance(row[key], expected_type):
        raise ValueError(f'Column "{expected_key}" has type {type(row[key])} (expected {expected_type})')