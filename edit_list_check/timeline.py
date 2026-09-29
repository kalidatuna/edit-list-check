"""Check clip source ranges and output timeline placement."""

from .model import Clip, Finding


def check_timeline(clips: list[Clip]) -> list[Finding]:
    findings: list[Finding] = []
    valid: list[Clip] = []
    for clip in clips:
        if clip.source_out <= clip.source_in:
            findings.append(Finding(clip.row, "empty-range", "out must be after in"))
        else:
            valid.append(clip)
    previous = None
    for clip in sorted(valid, key=lambda item: (item.timeline_start, item.row)):
        if previous is not None and clip.timeline_start < previous.timeline_end:
            findings.append(
                Finding(clip.row, "overlap", f"overlaps row {previous.row} on timeline")
            )
        if previous is None or clip.timeline_end > previous.timeline_end:
            previous = clip
    return findings
