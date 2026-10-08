import pathlib, tempfile, unittest
from edit_list_check.read_csv import read_clips

class CsvLineNumberTests(unittest.TestCase):
    def test_findings_identify_physical_lines_after_blank_and_multiline_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / 'edits.csv'
            cases = ['\na.mp4,bad,00:00:01.000,00:00:00.000\n', '\"a\nname.mp4\",bad,00:00:01.000,00:00:00.000\n']
            for data in cases:
                with self.subTest(data=data):
                    path.write_text('source,in,out,timeline_start\n' + data)
                    clips, findings = read_clips(path)
                    self.assertEqual(clips, [])
                    self.assertEqual(findings[0].row, 3)
