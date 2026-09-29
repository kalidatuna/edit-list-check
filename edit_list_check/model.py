"""Shared edit list records."""

from dataclasses import asdict, dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Clip:
    row: int
    source: str
    source_in: Decimal
    source_out: Decimal
    timeline_start: Decimal

    @property
    def timeline_end(self) -> Decimal:
        return self.timeline_start + self.source_out - self.source_in


@dataclass(frozen=True)
class Finding:
    row: int
    code: str
    message: str

    def to_dict(self) -> dict:
        return asdict(self)
