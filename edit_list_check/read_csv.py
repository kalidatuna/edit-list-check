"""Read the four-column CSV format with row-level diagnostics."""

import csv
from pathlib import Path

from .model import Clip, Finding
from .timecode import parse_timecode

REQUIRED = ("source", "in", "out", "timeline_start")


def read_clips(path: Path) -> tuple[list[Clip], list[Finding]]:
    clips: list[Clip] = []
    findings: list[Finding] = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or any(name not in reader.fieldnames for name in REQUIRED):
            return [], [Finding(1, "missing-column", ", ".join(REQUIRED))]
        for row_number, record in enumerate(reader, 2):
            if not any(value for value in record.values() if isinstance(value, str)):
                continue
            if None in record or any(record.get(name) is None for name in REQUIRED):
                findings.append(Finding(row_number, "invalid-row", "wrong number of columns"))
                continue
            source = record["source"].strip()
            if not source:
                findings.append(Finding(row_number, "missing-source", "source is empty"))
                continue
            try:
                source_in = parse_timecode(record["in"])
                source_out = parse_timecode(record["out"])
                timeline_start = parse_timecode(record["timeline_start"])
            except ValueError as error:
                findings.append(Finding(row_number, "invalid-timecode", str(error)))
                continue
            clips.append(Clip(row_number, source, source_in, source_out, timeline_start))
    return clips, findings
