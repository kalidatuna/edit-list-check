# CSV format

Each row places one source range on a single output timeline. The four
required columns are `source`, `in`, `out`, and `timeline_start`. Column order
may vary. Extra columns are ignored.

All times are `HH:MM:SS.mmm` with exactly three millisecond digits. The
checker uses decimal arithmetic. `in` and `out` are positions in the source;
the output clip ends at `timeline_start + out - in`. Gaps are valid. Layers,
transitions, speed changes, audio tracks, and frame-rate conversion are not
represented. The tool is intended for simple cut lists and preflight checks,
not as a full EDL interchange format.

The [sample list](../examples/edits.csv) references illustrative filenames.
Run it with `--no-files`, or put those files beneath `--media-root`.
