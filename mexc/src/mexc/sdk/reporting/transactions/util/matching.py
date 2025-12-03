from typing_extensions import Iterable, Sequence, Literal, Mapping, MutableMapping
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

from trading_sdk.reporting import Posting

TimeMode = Literal['eq', 'ge', 'le']

@dataclass
class PostingMatcher:
  postings: Sequence[Posting]
  index: Mapping[str, Mapping[str, Mapping[datetime, MutableMapping[int, Posting]]]]

  @classmethod
  def of(cls, postings: Sequence[Posting]):
    idx = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for i, p in enumerate(postings):
      idx[p.asset][p.tag][p.time][i] = p
    return cls(postings, idx)

  def candidates(self, p_hat: Posting, *, time_mode: TimeMode = 'eq') -> MutableMapping[int, Posting]:
    group = self.index[p_hat.asset][p_hat.tag]
    if time_mode == 'eq':
      return group[p_hat.time]
    elif time_mode == 'ge':
      ts = [t for t in group.keys() if p_hat.time <= t]
    else:
      ts = [t for t in group.keys() if t <= p_hat.time]
    out: dict[int, Posting] = {}
    for t in ts:
      out.update(group[t])
    return out

  def use(self, key: int):
    p = self.postings[key]
    del self.index[p.asset][p.tag][p.time][key]

  def insert(self, key: int):
    p = self.postings[key]
    self.index[p.asset][p.tag][p.time][key] = p

  def match(self, postings: Iterable[Posting], *, time_mode: TimeMode = 'eq') -> list[int] | None:
    """Match the postings to the postings in the matcher. The matched postings are removed from the matcher, preventing double-matching."""
    out = []
    for p_hat in postings:
      candidates = self.candidates(p_hat, time_mode=time_mode)
      if len(candidates) == 0:
        for k in out:
          self.insert(k) # restore the used postings
        return None
      elif len(candidates) == 1:
        k = next(iter(candidates.keys()))
      else:
        k = min(candidates.keys(), key=lambda i: abs(p_hat.change - candidates[i].change))
      self.use(k)
      out.append(k)
    return out
