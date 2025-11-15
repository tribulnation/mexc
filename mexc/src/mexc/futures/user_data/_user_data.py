from dataclasses import dataclass
from .my_funding_history import MyFundingHistory
from .my_trades import MyTrades
from .positions import Positions

@dataclass
class UserData(MyFundingHistory, MyTrades, Positions):
  ...