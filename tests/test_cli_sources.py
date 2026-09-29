import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from edit_list_check.cli import main


class CliSourceTests(unittest.TestCase):
    def test_source_files_and_json(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "edits.csv").write_text(
                "source,in,out,timeline_start\n"
                "missing.mp4,00:00:00.000,00:00:01.000,00:00:00.000\n"
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main([str(root / "edits.csv"), "--media-root", directory, "--json"])
            self.assertEqual(result, 1)
            self.assertEqual(json.loads(output.getvalue())[0]["code"], "missing-source-file")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(root / "edits.csv"), "--no-files"]), 0)

    def test_parent_path_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "edits.csv").write_text(
                "source,in,out,timeline_start\n"
                "../secret.mp4,00:00:00.000,00:00:01.000,00:00:00.000\n"
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([str(root / "edits.csv"), "--media-root", directory]), 1)
            self.assertIn("unsafe-source", output.getvalue())


if __name__ == "__main__":
    unittest.main()
