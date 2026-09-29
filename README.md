# Edit List Check

Validate a simple CSV video edit list before rendering. The checker catches
invalid timecodes, empty or reversed source ranges, timeline overlaps, and
missing or unsafe source paths. It has no dependencies beyond Python 3.10.

```sh
python3 -m edit_list_check edits.csv --media-root ./media
python3 -m edit_list_check edits.csv --media-root ./media --json
```

CSV columns are `source,in,out,timeline_start`. Timecodes use
`HH:MM:SS.mmm`. The source range is half open: `in` is included and `out` is
excluded. `timeline_start` places the clip on the output timeline. Gaps are
allowed; overlaps are reported. Source paths are relative to `--media-root`.
Use `--no-files` to check timing before media is present.

Exit status is 0 for valid input, 1 for findings, and 2 for invalid arguments
or an unreadable CSV. See [the format guide](docs/format.md) and
[example](examples/edits.csv).
