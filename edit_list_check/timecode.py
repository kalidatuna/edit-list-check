"""Parse fixed millisecond timecodes without floating point rounding."""

import re
from decimal import Decimal

_TIMECODE = re.compile(r"^(\d{2,}):([0-5]\d):([0-5]\d)\.(\d{3})$")


def parse_timecode(value: str) -> Decimal:
    match = _TIMECODE.fullmatch(value.strip())
    if not match:
        raise ValueError("expected HH:MM:SS.mmm")
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return Decimal(hours * 3600 + minutes * 60 + seconds) + Decimal(milliseconds) / 1000
