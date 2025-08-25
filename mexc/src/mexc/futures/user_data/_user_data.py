from dataclasses import dataclass
from .funding_rate_history import FundingRateHistory

@dataclass
class UserData(FundingRateHistory):
  ...