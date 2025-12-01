from typing_extensions import Literal
from decimal import Decimal
from datetime import timezone
import pandas as pd
from trading_sdk.reporting.types import CryptoWithdrawal, Fee

from .. import util

def parse_entry(row: pd.Series) -> CryptoWithdrawal:
  asset = str(row['Crypto'])
  fee_amount = Decimal(str(row['Trading Fee']))
  fee = Fee(fee_amount, asset) if fee_amount > 0 else None
  memo = str(row['memo'])
  if memo == '--':
    memo = None
  return CryptoWithdrawal(
    asset=asset,
    qty=Decimal(str(row['Settlement Amount'])),
    tx_id=str(row['TxID']),
    network=str(row['Network']),
    time=util.ensure_datetime(row['Time(UTC)']),
    address=str(row['Withdrawal Address']),
    memo=memo,
    fee=fee,
    tag='Spot Withdraw',
    fee_tag='Spot Withdrawal Fees',
  )

class withdrawals:
  """Parsing MEXC's withdrawals log.

  *This data is already included in the spot statement.*

    It must be downloaded as an Excel file from:
    
    > [Data Export](https://www.mexc.com/support/data-export) > `Funding History` > `Withdrawal History` > `Excel`

    **Expected schema:**

    - `Status`
    - `Time`
    - `Crypto`
    - `Network`
    - `Settlement Amount`	
    - `Withdrawal Address`
    - `memo`
    - `Trading Fee`
    - `TxID`
    """

  matching_mode: Literal['ge'] = 'ge'

  schema: util.Schema = {
    'Status': str,
    'Time': str,
    'Crypto': str,
    'Network': str,
    'Settlement Amount': str,
    'Withdrawal Address': str,
    'memo': str,
    'Trading Fee': str,
    'TxID': str,
  }

  @staticmethod
  def load(path: str, tz: timezone, *, skip_zero_changes: bool = True) -> pd.DataFrame:
    df = pd.read_excel(path, dtype={'Settlement Amount': str, 'Trading Fee': str})
    util.validate_schema(df, withdrawals.schema)
    if skip_zero_changes:
      df.drop(df[df['Settlement Amount'].astype(float) == 0].index, inplace=True) # type: ignore
    df.drop(df[df['Status'] != 'Withdrawal Successful'].index, inplace=True) # type: ignore
    df.reset_index(drop=True, inplace=True)
    df['Time(UTC)'] = pd.to_datetime(df['Time']).dt.tz_localize(tz).dt.tz_convert(timezone.utc)
    return df

  @staticmethod
  def parse(path: str, tz: timezone, *, skip_zero_changes: bool = True):
    """Parse withdrawals log excel file.

    - `path`: Path to excel file
    - `tz`: Timezone of the times in the log
    """
    df = withdrawals.load(path, tz, skip_zero_changes=skip_zero_changes)
    for posting in withdrawals.parse_df(df):
      yield posting

  @staticmethod
  def parse_df(df: pd.DataFrame):
    for _, row in df.iterrows():
      yield parse_entry(row)