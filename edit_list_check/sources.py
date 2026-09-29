"""Keep source paths inside the chosen media folder."""

from pathlib import Path

from .model import Clip, Finding


def check_sources(clips: list[Clip], media_root: Path) -> list[Finding]:
    root = media_root.resolve()
    findings: list[Finding] = []
    for clip in clips:
        relative = Path(clip.source)
        if relative.is_absolute() or ".." in relative.parts:
            findings.append(Finding(clip.row, "unsafe-source", clip.source))
            continue
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            findings.append(Finding(clip.row, "unsafe-source", clip.source))
        elif not target.is_file():
            findings.append(Finding(clip.row, "missing-source-file", clip.source))
    return findings
