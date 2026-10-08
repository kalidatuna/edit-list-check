import pathlib, tempfile, unittest
from edit_list_check.read_csv import read_clips

class DuplicateColumnTests(unittest.TestCase):
    def test_duplicate_named_headers_are_reported_instead_of_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / 'edits.csv'
            path.write_text('source,in,out,timeline_start,source\na.mp4,00:00:00.000,00:00:01.000,00:00:00.000,b.mp4\n')
            clips, findings = read_clips(path)
            self.assertEqual(clips, [])
            self.assertEqual([(finding.row, finding.code) for finding in findings], [(1, 'duplicate-column')])
            self.assertIn('source', findings[0].message)
