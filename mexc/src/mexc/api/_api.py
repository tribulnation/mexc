from dataclasses import dataclass
from .spot import Spot
from .wallet import Wallet

@dataclass
class MEXC(Spot, Wallet):
  ...


async def main(API_KEY: str, API_SECRET: str):


  async with MEXC(API_KEY, API_SECRET) as client:
    r = await client.place_order('BTCUSDT', {
      'price': '100000',
      'quantity': '0.001',
      'side': '',
      'type': 'LIMIT',
    })