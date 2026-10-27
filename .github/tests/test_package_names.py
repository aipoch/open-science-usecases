from pathlib import Path
import runpy
import unittest

CHECK = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts' / 'check_package_names.py'))


class PackageNamingTests(unittest.TestCase):
    def entry(self):
        return {'name': 'example', 'case': {'file_name': 'Example-case.science',
                'path': 'AI Research/Example case/Example-case.science', 'release_url': ''}}

    def test_spaces_in_directories_are_allowed(self):
        entry = self.entry()
        self.assertEqual(CHECK['naming_errors']([entry], [entry['case']['path']]), [])

    def test_manifest_filename_and_final_path_segment_are_checked(self):
        for field in ('file_name', 'path'):
            entry = self.entry()
            entry['case'][field] = entry['case'][field].replace('Example-case', 'Example case')
            self.assertTrue(CHECK['naming_errors']([entry]))

    def test_percent_encoded_download_filename_is_checked(self):
        entry = self.entry()
        entry['case']['release_url'] = 'https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/resolve/main/AI%20Research/Example%20case/Example-case.science'
        self.assertEqual(CHECK['naming_errors']([entry]), [])
        entry['case']['release_url'] = entry['case']['release_url'].replace('Example-case.science', 'Example%20case.science')
        self.assertTrue(CHECK['naming_errors']([entry]))

    def test_unlisted_tracked_packages_and_unicode_whitespace_are_checked(self):
        self.assertTrue(CHECK['naming_errors']([], ['folder/unlisted package.science']))
        entry = self.entry()
        entry['case']['file_name'] = 'Example\u00a0case.science'
        self.assertTrue(CHECK['naming_errors']([entry]))

    def test_cover_markdown_and_package_contents_are_outside_naming_scope(self):
        self.assertEqual(CHECK['naming_errors']([], ['AI Research/My case.md', 'AI Research/My case.png']), [])


if __name__ == '__main__':
    unittest.main()
