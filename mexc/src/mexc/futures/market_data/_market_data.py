from dataclasses import dataclass
from .candles import Candles
from .contract_info import ContractInfo
from .funding_rate import FundingRate
from .funding_rate_history import FundingRateHistory

@dataclass
class MarketData(
  Candles,
  ContractInfo,
  FundingRate,
  FundingRateHistory,
):
  ...