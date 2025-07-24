from typing_extensions import ClassVar, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')

@dataclass(frozen=True)
class SdkMixin(Generic[T]):
  Client: ClassVar[type]
  client: T
  validate: bool = True
  recvWindow: int | None = None

  @classmethod
  def new(cls, api_key: str, api_secret: str):
    client = cls.Client(api_key=api_key, api_secret=api_secret)
    return cls(client=client)