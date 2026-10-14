"""Exercise the full-manifest allowlist without network access."""
import copy
import json
import subprocess
import sys

from test_publish import GitFixture, SCRIPTS


class ReleaseURLTests(GitFixture):
    def check_urls(self):
        self.write_manifest()
        return subprocess.run(
            [sys.executable, '-B', str(SCRIPTS / 'check_structure.py'), 'release-urls'],
            cwd=self.root, capture_output=True, text=True)

    def test_accepts_local_sources_and_both_allowed_repositories(self):
        prefixes = (
            '',
            'https://github.com/aipoch/open-science-usecases/releases/download/v1/',
            'https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/resolve/main/',
        )
        for prefix in prefixes:
            with self.subTest(prefix=prefix):
                for kind, suffix in (('cover', 'png'), ('case', 'science'), ('introduction', 'md')):
                    self.entry[kind]['release_url'] = prefix + 'A%20Case%3F.' + suffix + '?download=1' if prefix else ''
                result = self.check_urls()
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_untrusted_urls_for_each_resource_kind(self):
        github = 'https://github.com/aipoch/open-science-usecases/'
        huggingface = 'https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/'
        urls = (
            'https://example.com/case.science',
            'https://github.com/roxi3906/open-science-usecases/case.science',
            github.replace('https:', 'http:') + 'case.science',
            github.replace('github.com', 'github.com.evil.test') + 'case.science',
            github.replace('github.com', 'github.com@evil.test') + 'case.science',
            github.replace('github.com', 'github.com:8443') + 'case.science',
            github.rstrip('/') + '-fork/case.science',
            huggingface.rstrip('/') + '-fork/case.science',
            huggingface.replace('AIPOCH-AI', 'someone-else') + 'case.science',
            github + '../other/case.science',
            huggingface + '%2e%2e/other/case.science',
            github + '%252e%252e%252fother/case.science',
            github + 'a/../../other/case.science',
            github + 'a\\..\\case.science',
            github + '%0acase.science',
            '//github.com/aipoch/open-science-usecases/case.science',
            ' ', None, 42,
        )
        original = copy.deepcopy(self.entry)
        for kind in ('cover', 'case', 'introduction'):
            for url in urls:
                with self.subTest(kind=kind, url=url):
                    self.entries = [copy.deepcopy(original)]
                    self.entries[0][kind]['release_url'] = url
                    result = self.check_urls()
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn('a-case', result.stderr)
                    self.assertIn(kind, result.stderr)
                    self.assertIn('release_url', result.stderr)

    def test_rejects_unchanged_entry_even_when_no_cases_are_selected(self):
        self.entry['cover']['release_url'] = 'https://example.com/cover.png'
        self.write_manifest()
        self.commit()
        result = self.check_urls()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('release_url', result.stderr)

    def test_rejects_malformed_manifest(self):
        (self.root / 'manifest.json').write_text('{broken')
        result = subprocess.run(
            [sys.executable, '-B', str(SCRIPTS / 'check_structure.py'), 'release-urls'],
            cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('JSON', result.stderr)
