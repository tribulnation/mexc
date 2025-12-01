from typing_extensions import Literal
from decimal import Decimal
from datetime import timezone
import re
import pandas as pd
from trading_sdk.reporting.types import Trade, Fee

from .. import util

fee_regex = re.compile(r'([-\d\.]+)([A-Z0-9]+)$')

def parse_entry(row: pd.Series) -> Trade:
  fee_amount = Decimal(str(row['fee_amount']))
  if fee_amount == 0:
    fee = None
  else:
    fee = Fee(fee_amount, str(row['fee_asset']))
  return Trade(
    base=str(row['base']),
    quote=str(row['quote']),
    qty=Decimal(str(row['Executed Amount'])),
    price=Decimal(str(row['Filled Price'])),
    liquidity='TAKER' if row['Role'] == 'Taker' else 'MAKER',
    time=util.ensure_datetime(row['Time(UTC)']),
    side='BUY' if row['Side'] == 'Buy' else 'SELL',
    fee=fee,
    base_tag='Spot Spot Trading',
    quote_tag='Spot Spot Trading',
    fee_tag='Spot Spot Trading Fees',
  )

class spot_trades:
  """Parsing MEXC's spot trades log.

  *This data is already included in the spot statement.*

    It must be downloaded as an Excel file from:
    
    > [Data Export](https://www.mexc.com/support/data-export) > `Spot` > `Spot Trade History` > `Excel`

    **Expected schema:**

    - `Pairs :: <base>_<quote>`
    - `Time`
    - `Side :: Buy | Sell`
    - `Filled Price`
    - `Executed Amount :: Quantity`
    - `Fee :: <amount><asset>`
    - `Role :: Taker | Maker`
    """

  matching_mode: Literal['eq'] = 'eq'

  schema: util.Schema = {
    'Pairs': re.compile(r"^.+_.+$"),
    'Time': str,
    'Side': re.compile(r"^(Buy|Sell)$"),
    'Filled Price': str,
    'Executed Amount': str,
    'Fee': fee_regex,
    'Role': re.compile(r"^(Taker|Maker)$"),
  }

  @staticmethod
  def load(path: str, tz: timezone, *, skip_zero_changes: bool = True) -> pd.DataFrame:
    df = pd.read_excel(path, dtype={'Filled Price': str, 'Executed Amount': str})
    util.validate_schema(df, spot_trades.schema)
    if skip_zero_changes:
      df.drop(df[df['Executed Amount'].astype(float) == 0].index, inplace=True) # type: ignore
      df.reset_index(drop=True, inplace=True)
    df[['base', 'quote']] = df['Pairs'].str.split('_', expand=True)
    df[['fee_amount', 'fee_asset']] = df['Fee'].str.extract(fee_regex)
    df['Time(UTC)'] = pd.to_datetime(df['Time']).dt.tz_localize(tz).dt.tz_convert(timezone.utc)
    return df

  @staticmethod
  def parse(path: str, tz: timezone, *, skip_zero_changes: bool = True):
    """Parse spot trades history excel file.

    - `path`: Path to excel file
    - `tz`: Timezone of the times in the log
    """
    df = spot_trades.load(path, tz, skip_zero_changes=skip_zero_changes)
    for posting in spot_trades.parse_df(df):
      yield posting

  @staticmethod
  def parse_df(df: pd.DataFrame):
    for _, row in df.iterrows():
      yield parse_entry(row)