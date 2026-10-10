"""Execute publication diagnostics without GitHub or S3 access."""
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest


class PublicationDiagnosticsTests(unittest.TestCase):
    def test_decisions_are_visible_in_logs_and_summary(self):
        workflow = (Path(__file__).resolve().parents[1] / 'workflows/check-structure.yml').read_text()
        marker = '      - name: Explain publication result\n'
        self.assertIn(marker, workflow)
        step = workflow.split(marker, 1)[1]
        self.assertIn('if: always()', step)
        script = textwrap.dedent(step.split('        run: |\n', 1)[1])
        cases = [
            ({'JOB_STATUS': 'failure', 'PLAN_OUTCOME': 'failure'}, 'preparation failed'),
            ({'JOB_STATUS': 'failure', 'PLAN_OUTCOME': 'success'}, 'failed'),
            ({'JOB_STATUS': 'cancelled'}, 'cancelled'),
            ({'PLAN_OUTCOME': 'success', 'HAS_UPLOADS': 'false'}, 'matches S3'),
            ({'PLAN_OUTCOME': 'success', 'HAS_UPLOADS': 'true', 'APPLY_OUTCOME': 'success'}, 'completed'),
            ({'PLAN_OUTCOME': 'skipped'}, 'did not complete'),
        ]
        defaults = {'JOB_STATUS': 'success', 'PLAN_OUTCOME': 'skipped',
                    'APPLY_OUTCOME': 'skipped', 'HAS_UPLOADS': ''}
        for overrides, expected in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as directory:
                summary = Path(directory) / 'summary.md'
                summary.write_text('Existing summary\n')
                result = subprocess.run(['bash', '-e', '-u', '-o', 'pipefail', '-c', script],
                                        env={**os.environ, **defaults, **overrides,
                                             'GITHUB_STEP_SUMMARY': str(summary)},
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertIn(expected, summary.read_text())
                self.assertTrue(summary.read_text().startswith('Existing summary\n'))
