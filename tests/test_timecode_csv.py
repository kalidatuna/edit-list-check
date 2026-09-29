import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from edit_list_check.read_csv import read_clips
from edit_list_check.timecode import parse_timecode
from edit_list_check.timeline import check_timeline


class EditListTests(unittest.TestCase):
    def test_timecode_exact(self):
        self.assertEqual(parse_timecode("01:02:03.004"), Decimal("3723.004"))
        for bad in ("1:02:03.004", "00:60:00.000", "00:00:00", "-01:00:00.000"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_timecode(bad)

    def test_csv_and_overlap(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "edits.csv"
            file.write_text(
                "source,in,out,timeline_start\n"
                "a.mp4,00:00:00.000,00:00:02.000,00:00:00.000\n"
                "b.mp4,00:00:00.000,00:00:01.000,00:00:01.000\n"
            )
            clips, findings = read_clips(file)
            self.assertEqual(findings, [])
            self.assertEqual(check_timeline(clips)[0].code, "overlap")

    def test_bad_rows_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "edits.csv"
            file.write_text("source,in,out,timeline_start\na.mp4,nope,00:00:01.000,00:00:00.000\n")
            clips, findings = read_clips(file)
            self.assertEqual(clips, [])
            self.assertEqual((findings[0].row, findings[0].code), (2, "invalid-timecode"))


if __name__ == "__main__":
    unittest.main()
