"""Command line interface for CSV validation."""

import argparse
import json
from pathlib import Path

from .read_csv import read_clips
from .sources import check_sources
from .timeline import check_timeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a CSV edit list")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--media-root", type=Path, default=Path("."))
    parser.add_argument("--no-files", action="store_true", help="skip source file checks")
    parser.add_argument("--json", action="store_true", help="write machine-readable findings")
    args = parser.parse_args(argv)
    try:
        clips, findings = read_clips(args.csv_file)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    findings.extend(check_timeline(clips))
    if not args.no_files:
        findings.extend(check_sources(clips, args.media_root))
    findings.sort(key=lambda item: (item.row, item.code, item.message))
    if args.json:
        print(json.dumps([finding.to_dict() for finding in findings], indent=2))
    else:
        for finding in findings:
            print(f"row {finding.row}: {finding.code}: {finding.message}")
        print(f"{len(clips)} clip(s), {len(findings)} finding(s)")
    return 1 if findings else 0
