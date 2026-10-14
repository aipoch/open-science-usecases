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
            ({'PLAN_OUTCOME': 'success', 'HAS_UPLOADS': 'false'}, 'final manifest sync'),
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


class ConcurrentReporterTests(unittest.TestCase):
    def test_many_file_events_keep_console_and_snapshot_work_bounded(self):
        import contextlib
        import io
        import json
        from unittest.mock import patch
        from publication_steps import Reporter, atomic_json
        plan = {'after': 'fixture', 'steps': [{'id': 1, 'operation': 'ADD_CASE', 'name': 'case',
                'files': [{'key': 'case/' + str(n)} for n in range(1000)]}]}
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()) as log:
            reporter = Reporter(plan, Path(directory))
            state = reporter.state['steps'][0]
            with patch('publication_steps.time.monotonic', return_value=reporter.started), \
                    patch('publication_steps.atomic_json', wraps=atomic_json) as snapshots:
                for item in state['files']:
                    reporter.update(item, status='completed')
                    reporter.event(plan['steps'][0], 'file', 'completed', key=item['key'])
                self.assertEqual(snapshots.call_count, 0)
                reporter.summary()
                self.assertEqual(snapshots.call_count, 1)
            self.assertEqual(log.getvalue(), '')
            events = (Path(directory) / 'events.jsonl').read_text().splitlines()
            self.assertEqual(len(events), 1000)
            state = json.loads((Path(directory) / 'status.json').read_text())
            self.assertTrue(all(f['status'] == 'completed' for f in state['steps'][0]['files']))

    def test_failure_updates_cannot_resize_state_during_snapshot_on_python312(self):
        from concurrent.futures import ThreadPoolExecutor
        import contextlib
        import io
        import json
        from publication_steps import Reporter
        plan = {'after': 'fixture', 'steps': [{'id': 1, 'operation': 'ADD_CASE', 'name': 'case',
                'files': [{'key': 'case/' + str(n)} for n in range(30000)]}]}
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            reporter = Reporter(plan, Path(directory))
            state = reporter.state['steps'][0]
            def mutate():
                for i in range(20):
                    reporter.update(state, **{'failure_' + str(i): 'fixture'})
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(mutate), pool.submit(reporter.event, plan['steps'][0], 'step', 'failed')]
                for future in futures:
                    future.result()
            reporter.summary()
            saved = json.loads((Path(directory) / 'status.json').read_text())['steps'][0]
            self.assertTrue(all('failure_' + str(i) in saved for i in range(20)))
