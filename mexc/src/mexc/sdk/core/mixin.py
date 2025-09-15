from dataclasses import dataclass

from mexc import MEXC


@dataclass
class SdkMixin:
  client: MEXC
  validate: bool = True
  recvWindow: int | None = None

  @classmethod
  def env(cls, *, validate: bool = True, recvWindow: int | None = None):
    import os
    return cls.new(
      api_key=os.environ['MEXC_ACCESS_KEY'], api_secret=os.environ['MEXC_SECRET_KEY'],
      validate=validate, recvWindow=recvWindow
    )

  @classmethod
  def new(cls, api_key: str, api_secret: str, *, validate: bool = True, recvWindow: int | None = None):
    client = MEXC.new(api_key=api_key, api_secret=api_secret)
    return cls(client=client, validate=validate, recvWindow=recvWindow)

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)