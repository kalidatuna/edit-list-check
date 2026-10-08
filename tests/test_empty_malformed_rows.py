import pathlib, tempfile, unittest
from edit_list_check.read_csv import read_clips

class MalformedEmptyRowTests(unittest.TestCase):
    def test_empty_required_fields_do_not_hide_extra_or_missing_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / 'edits.csv'
            for row in (',,,,extra', ',,'):
                with self.subTest(row=row):
                    path.write_text('source,in,out,timeline_start\n' + row + '\n')
                    clips, findings = read_clips(path)
                    self.assertEqual(clips, [])
                    self.assertEqual([finding.code for finding in findings], ['invalid-row'])
            path.write_text('source,in,out,timeline_start\n,,,\n')
            self.assertEqual(read_clips(path), ([], []))
