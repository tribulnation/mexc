from dataclasses import dataclass
from .spot import Spot
from .wallet import Wallet

@dataclass
class MEXC(Spot, Wallet):
  ...
