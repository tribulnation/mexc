from typing_extensions import Literal
from decimal import Decimal
from datetime import timezone
import pandas as pd
from trading_sdk.reporting import CryptoDeposit

from .. import util

def parse_entry(row: pd.Series) -> CryptoDeposit:
  return CryptoDeposit(
    asset=str(row['Crypto']),
    qty=Decimal(str(row['Deposit Amount'])),
    tx_id=str(row['TxID']),
    network=str(row['Network']),
    time=util.ensure_datetime(row['Time(UTC)']),
    tag='Spot Deposit'
  )

class deposits:
  """Parsing MEXC's (crypto) deposits log.

  *This data is already included in the spot statement.*

    It must be downloaded as an Excel file from:
    
    > [Data Export](https://www.mexc.com/support/data-export) > `Funding History` > `Deposit History` > `Excel`

    **Expected schema:**

    - `Status`
    - `Time`
    - `Crypto`
    - `Network`
    - `Deposit Amount`	
    - `TxID`
    """

  matching_mode: Literal['ge'] = 'ge'

  schema: util.Schema = {
    'Status': str,
    'Time': str,
    'Crypto': str,
    'Network': str,
    'Deposit Amount': str,
    'TxID': str,
  }

  @staticmethod
  def load(path: str, tz: timezone, *, skip_zero_changes: bool = True) -> pd.DataFrame:
    df = pd.read_excel(path, dtype={'Deposit Amount': str})
    util.validate_schema(df, deposits.schema)
    if skip_zero_changes:
      df.drop(df[df['Deposit Amount'].astype(float) == 0].index, inplace=True) # type: ignore
    df.drop(df[df['Status'] != 'Credited Successfully'].index, inplace=True) # type: ignore
    df.reset_index(drop=True, inplace=True)
    df['Time(UTC)'] = pd.to_datetime(df['Time']).dt.tz_localize(tz).dt.tz_convert(timezone.utc)
    return df

  @staticmethod
  def parse(path: str, tz: timezone, *, skip_zero_changes: bool = True):
    """Parse deposits log excel file.

    - `path`: Path to excel file
    - `tz`: Timezone of the times in the log
    """
    df = deposits.load(path, tz, skip_zero_changes=skip_zero_changes)
    for posting in deposits.parse_df(df):
      yield posting

  @staticmethod
  def parse_df(df: pd.DataFrame):
    for _, row in df.iterrows():
      yield parse_entry(row)