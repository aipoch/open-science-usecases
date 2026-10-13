"""Observable case checkpoints and fresh-run recovery against a local AWS boundary."""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

from test_publish import GitFixture, SCRIPTS, publisher


class PublicationStepsTests(GitFixture):
    def test_head_insert_updates_removals_order_and_exact_final_sync(self):
        old = copy.deepcopy(self.entries)
        b = self.add_case('B Case', 'b-case')
        c = self.add_case('C Case', 'c-case')
        remote = copy.deepcopy(b); remote['name'] = 'remote-only'
        old.append(remote)
        self.entry['title'] = 'Updated A'
        self.entries = [self.entry, c, b]
        self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, json.dumps(old), after)
        steps = plan['steps']
        self.assertEqual([s['operation'] for s in steps],
                         ['ADD_CASE', 'ADD_CASE', 'UPDATE_CASE', 'REMOVE_CASE', 'REORDER', 'FINAL_SYNC'])
        self.assertEqual([s['name'] for s in steps[:2]], ['b-case', 'c-case'])
        previous = old
        for step in steps[:-2]:
            current = json.loads(step['manifest'])
            before = {e['name']: e for e in previous}
            after = {e['name']: e for e in current}
            self.assertEqual([name for name in before.keys() | after.keys()
                              if before.get(name) != after.get(name)], [step['name']])
            if step['operation'] == 'ADD_CASE':
                self.assertEqual(current[0]['name'], step['name'])
            previous = current
        self.assertEqual(steps[3]['files'], [])
        self.assertEqual(json.loads(steps[-2]['manifest']), self.entries)
        self.assertEqual(steps[-1]['manifest'], (self.root / 'manifest.json').read_text())

    def test_unchanged_and_format_only_still_have_final_sync(self):
        for baseline in (json.dumps(self.entries), json.dumps(self.entries, indent=4)):
            with self.subTest(baseline=baseline):
                plan = publisher.prepare(self.root, baseline, self.base)
                self.assertEqual([s['operation'] for s in plan['steps']], ['FINAL_SYNC'])
                self.assertEqual(plan['steps'][0]['files'], [])

    def test_order_only_has_explicit_reorder_then_final_sync(self):
        self.add_case('B Case', 'b-case'); self.write_manifest(); self.commit()
        plan = publisher.prepare(self.root, json.dumps(self.entries[::-1]), self.git('rev-parse', 'HEAD'))
        self.assertEqual([s['operation'] for s in plan['steps']], ['REORDER', 'FINAL_SYNC'])
        self.assertTrue(all(not s['files'] for s in plan['steps']))

    def test_failed_third_case_restarts_from_second_manifest(self):
        # All packages are unchanged; this isolates per-case resource commits.
        self.add_case('B Case', 'b-case'); self.add_case('C Case', 'c-case')
        self.write_manifest(); self.commit()
        baseline = json.dumps(self.entries)
        for entry in self.entries:
            resource = entry['introduction']
            import hashlib
            (self.root / resource['path']).write_bytes(b'new description')
            resource.update(bytes=15, sha256=hashlib.sha256(b'new description').hexdigest())
        self.write_manifest(); self.commit()
        fake = self.root / 'bin'; fake.mkdir()
        aws = fake / 'aws'
        aws.write_text('#!' + sys.executable + '\n' + Path(__file__).with_name('fake_s3.py').read_text())
        aws.chmod(0o755)
        store = self.root / 's3'; target = store / 'bucket/cases'; target.mkdir(parents=True)
        (target / 'manifest.json').write_text(baseline)
        plan_file = self.root / 'plan.json'
        env = {**os.environ, 'PATH': str(fake) + os.pathsep + os.environ['PATH'],
               'FAKE_S3_ROOT': str(store), 'AWS_TARGET_FOLDER': 's3://bucket/cases',
               'AWS_DISTRIBUITION_ID': 'test-distribution'}
        def run(*args, fail=None):
            return subprocess.run([sys.executable, '-B', str(SCRIPTS / 'publish.py'), *args],
                                  cwd=self.root, env={**env, **(fail or {})}, capture_output=True, text=True)
        result = run('--after', self.git('rev-parse', 'HEAD'), '--prepare', str(plan_file))
        self.assertEqual(result.returncode, 0, result.stderr)
        prepared = run('--prepare-resources', str(plan_file), '--output', str(self.root / 'sources'))
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        result = run('--apply-plan', str(plan_file), fail={'FAKE_S3_FAIL_MANIFEST_CASE': 'c-case'})
        self.assertNotEqual(result.returncode, 0)
        actual = json.loads((target / 'manifest.json').read_text())
        self.assertEqual(actual[:2], self.entries[:2])
        self.assertNotEqual(actual[2], self.entries[2])
        self.assertTrue((target / 'c-case/C Case.md').is_file())
        status = json.loads((self.root / 'plan/status.json').read_text())
        self.assertEqual([s['status'] for s in status['steps']], ['completed', 'completed', 'failed', 'waiting'])
        result = run('--after', self.git('rev-parse', 'HEAD'), '--prepare', str(plan_file))
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(plan_file.read_text())
        self.assertEqual([(s['operation'], s['name']) for s in plan['steps']],
                         [('UPDATE_CASE', 'c-case'), ('FINAL_SYNC', None)])
        prepared = run('--prepare-resources', str(plan_file), '--output', str(self.root / 'sources'))
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        result = run('--apply-plan', str(plan_file))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((target / 'manifest.json').read_bytes(), (self.root / 'manifest.json').read_bytes())
        calls = [json.loads(line) for line in (store / 'calls.jsonl').read_text().splitlines()]
        self.assertEqual(sum(c[:2] == ['cloudfront', 'create-invalidation'] for c in calls), 4)
        self.assertIn('waiting', result.stdout)
        self.assertIn('uploading', result.stdout)
        self.assertIn('completed', result.stdout)


class PublicationBoundaryTests(GitFixture):
    def setUp(self):
        super().setUp()
        fake = self.root / 'bin'; fake.mkdir()
        aws = fake / 'aws'
        aws.write_text('#!' + sys.executable + '\n' + Path(__file__).with_name('fake_s3.py').read_text())
        aws.chmod(0o755)
        self.store = self.root / 's3'; self.target = self.store / 'bucket/cases'
        self.target.mkdir(parents=True)
        self.baseline = (self.root / 'manifest.json').read_text()
        (self.target / 'manifest.json').write_text(self.baseline)
        self.plan_file = self.root / 'plan.json'
        self.env = {**os.environ, 'PATH': str(fake) + os.pathsep + os.environ['PATH'],
                    'FAKE_S3_ROOT': str(self.store), 'AWS_TARGET_FOLDER': 's3://bucket/cases',
                    'AWS_DISTRIBUITION_ID': 'test-distribution'}

    def cli(self, *args, overrides=None, success=True):
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'publish.py'), *args],
                                cwd=self.root, env={**self.env, **(overrides or {})},
                                text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def prepare_run(self):
        self.cli('--prepare', str(self.plan_file), '--after', self.git('rev-parse', 'HEAD'))
        self.cli('--prepare-resources', str(self.plan_file), '--output', str(self.root / 'sources'))
        return json.loads(self.plan_file.read_text())

    def apply_run(self, **kwargs):
        return self.cli('--apply-plan', str(self.plan_file), **kwargs)

    def calls(self):
        path = self.store / 'calls.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def status(self):
        return json.loads((self.root / 'plan/status.json').read_text())['steps']

    def test_empty_first_publication_is_conditional_and_refreshes_cdn(self):
        (self.target / 'manifest.json').unlink()
        self.entries = []; self.write_manifest(); self.commit()
        self.prepare_run(); self.apply_run()
        puts = [c for c in self.calls() if c[:2] == ['s3api', 'put-object']]
        self.assertEqual(len(puts), 1)
        self.assertIn('--if-none-match', puts[0])
        self.assertEqual(self.status()[0]['status'], 'completed')
        self.assertEqual((self.target / 'manifest.json').read_bytes(), b'[]')

    def test_metadata_only_and_removal_do_not_touch_resources(self):
        self.entry['title'] = 'Changed title'; self.write_manifest(); self.commit()
        self.prepare_run(); self.apply_run()
        self.assertFalse(any(c[0] == 's3' for c in self.calls()))
        for key in ('a-case/A Case.science', 'a-case/extracted/old'):
            path = self.target / key; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(b'keep')
        self.entries = []; self.write_manifest(); self.commit()
        plan = self.prepare_run(); self.apply_run()
        self.assertEqual([s['operation'] for s in plan['steps']], ['REMOVE_CASE', 'FINAL_SYNC'])
        self.assertFalse(any(c[0] == 's3' for c in self.calls()))
        self.assertEqual((self.target / 'a-case/extracted/old').read_bytes(), b'keep')
        self.assertEqual((self.target / 'a-case/A Case.science').read_bytes(), b'keep')

    def test_sort_then_exact_final_bytes_and_cdn_per_step(self):
        self.add_case('B Case', 'b-case'); self.write_manifest(); self.commit()
        (self.target / 'manifest.json').write_text(json.dumps(self.entries[::-1]))
        # CRLF and a trailing blank line are part of the fixed repository blob.
        raw = (json.dumps(self.entries, indent=2).replace('\n', '\r\n') + '\r\n\r\n').encode()
        (self.root / 'manifest.json').write_bytes(raw); self.commit()
        plan = self.prepare_run(); self.apply_run()
        self.assertEqual([s['operation'] for s in plan['steps']], ['REORDER', 'FINAL_SYNC'])
        self.assertEqual((self.target / 'manifest.json').read_bytes(), raw)
        calls = self.calls()
        self.assertEqual(sum(c[:2] == ['cloudfront', 'create-invalidation'] for c in calls), 2)
        self.assertTrue(all('--if-match' in c for c in calls if c[:2] == ['s3api', 'put-object']))
        self.assertFalse(any(c[0] == 's3' for c in calls))
        import hashlib
        metadata = json.loads((self.store / 'metadata.json').read_text())
        self.assertEqual(metadata['bucket/cases/manifest.json']['sha256'], hashlib.sha256(raw).hexdigest())

    def test_manifest_only_steps_reject_tampered_resource_operations(self):
        self.prepare_run()
        plan = json.loads(self.plan_file.read_text())
        plan['steps'][0]['files'] = [{'key': 'unplanned/cover.png'}]
        self.plan_file.write_text(json.dumps(plan))
        self.apply_run(success=False)
        self.assertFalse(any(c[0] == 's3' or c[:2] == ['s3api', 'put-object'] for c in self.calls()))

    def test_publication_overrides_aws_text_output_for_parsed_responses(self):
        self.change()
        self.env['AWS_DEFAULT_OUTPUT'] = 'text'
        self.prepare_run(); self.apply_run()
        self.assertEqual((self.target / 'a-case/A Case.png').read_bytes(), b'modified')
        self.assertEqual((self.target / 'manifest.json').read_bytes(),
                         (self.root / 'manifest.json').read_bytes())
        self.assertTrue(all(s['status'] == 'completed' and s['cdn'] == 'completed'
                            for s in self.status()))
        for command in ('get-object', 'head-object', 'create-invalidation'):
            calls = [c for c in self.calls() if c[1] == command]
            self.assertTrue(calls, command + ' was not exercised')
            for call in calls:
                self.assertIn('--output', call)
                self.assertEqual(call[call.index('--output') + 1], 'json')

    def test_sha_case_only_skips_resource_uploads(self):
        self.entry['cover']['sha256'] = self.entry['cover']['sha256'].upper()
        self.write_manifest(); self.commit()
        self.prepare_run(); self.apply_run()
        self.assertFalse(any(c[0] == 's3' for c in self.calls()))

    def test_resource_failure_prevents_manifest_and_later_steps(self):
        self.change(); self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_FAIL': 'cp'}, success=False)
        self.assertEqual((self.target / 'manifest.json').read_text(), self.baseline)
        self.assertEqual([s['status'] for s in self.status()], ['failed', 'waiting'])
        self.assertFalse(any(c[0] == 'cloudfront' or c[:2] == ['s3api', 'put-object'] for c in self.calls()))
        self.assertEqual(self.status()[0]['files'][0]['status'], 'failed')

    def test_uploaded_object_verification_failure_blocks_manifest(self):
        self.change(); self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_BAD_HEAD': '1'}, success=False)
        self.assertEqual((self.target / 'manifest.json').read_text(), self.baseline)
        self.assertFalse(any(c[:2] == ['s3api', 'put-object'] for c in self.calls()))

    def test_manifest_conflict_stops_without_cdn_or_final_sync(self):
        self.change(); self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_CONFLICT': '1'}, success=False)
        self.assertEqual((self.target / 'manifest.json').read_text(), self.baseline)
        self.assertFalse(any(c[0] == 'cloudfront' for c in self.calls()))
        self.assertFalse(self.status()[0]['manifest_committed'])

    def test_conflict_on_identical_final_manifest_is_not_swallowed(self):
        self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_CONFLICT': '1'}, success=False)
        self.assertFalse(any(c[0] == 'cloudfront' for c in self.calls()))

    def test_uncertain_put_success_is_resolved_by_readback(self):
        self.change(); self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_TIMEOUT_AFTER_PUT': '1'})
        self.assertTrue(all(s['status'] == 'completed' for s in self.status()))
        self.assertEqual((self.target / 'manifest.json').read_bytes(), (self.root / 'manifest.json').read_bytes())

    def test_cdn_request_and_wait_failures_resume_via_final_sync(self):
        self.change()
        for operation in ('create-invalidation', 'wait'):
            with self.subTest(operation=operation):
                (self.target / 'manifest.json').write_text(self.baseline)
                self.prepare_run()
                self.apply_run(overrides={'FAKE_S3_FAIL': operation}, success=False)
                state = self.status()[0]
                self.assertEqual(state['status'], 'failed')
                self.assertEqual(state['cdn'], 'failed')
                self.assertTrue(state['manifest_committed'])
                self.assertEqual(self.status()[1]['status'], 'waiting')
                plan = self.prepare_run()
                self.assertEqual([s['operation'] for s in plan['steps']], ['FINAL_SYNC'])
                self.apply_run()
                self.assertEqual(self.status()[0]['cdn'], 'completed')

    def test_final_sync_failure_restarts_with_only_final_sync(self):
        self.change(); self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_FAIL_PUT_NUMBER': '2'}, success=False)
        self.assertEqual([s['status'] for s in self.status()], ['completed', 'failed'])
        plan = self.prepare_run()
        self.assertEqual([s['operation'] for s in plan['steps']], ['FINAL_SYNC'])
        self.apply_run()

    def test_changed_baseline_stops_before_any_resource_write(self):
        self.change(); self.prepare_run()
        (self.target / 'manifest.json').write_text('[]')
        self.apply_run(success=False)
        self.assertTrue(all(c[:2] in (['s3api', 'get-object'], ['s3api', 'head-object']) for c in self.calls()))

    def test_tampered_manifest_plan_and_original_bytes_block_writes(self):
        self.change(); plan = self.prepare_run()
        modified = copy.deepcopy(plan); modified['steps'][0]['manifest'] = '[]'
        self.plan_file.write_text(json.dumps(modified)); self.apply_run(success=False)
        self.plan_file.write_text(json.dumps(plan))
        Path(plan['files'][0]['path']).write_bytes(b'tampered')
        self.apply_run(success=False)
        self.assertTrue(all(c[:2] in (['s3api', 'get-object'], ['s3api', 'head-object']) for c in self.calls()))

    def test_native_rerun_and_missing_cdn_configuration_block_writes(self):
        self.change(); self.prepare_run()
        for overrides in ({'GITHUB_RUN_ATTEMPT': '2'}, {'AWS_DISTRIBUITION_ID': ''}):
            self.apply_run(overrides=overrides, success=False)
        self.assertTrue(all(c[:2] in (['s3api', 'get-object'], ['s3api', 'head-object']) for c in self.calls()))

    def test_every_checkpoint_has_reviewable_files_manifest_and_events(self):
        self.change(); plan = self.prepare_run(); self.apply_run()
        for step in plan['steps']:
            folder = self.root / 'plan/steps' / ('%03d-%s' % (step['id'], step['name'] or step['operation'].lower()))
            self.assertEqual((folder / 'manifest.json').read_bytes(), step['manifest'].encode())
            self.assertEqual(json.loads((folder / 'files.json').read_text()), step['files'])
        events = [json.loads(line) for line in (self.root / 'plan/events.jsonl').read_text().splitlines()]
        for step in plan['steps']:
            phases = [(e['phase'], e['status']) for e in events if e['step'] == step['id']]
            self.assertLess(phases.index(('manifest', 'completed')), phases.index(('cdn', 'uploading')))
            self.assertEqual(phases[-1], ('step', 'completed'))

    def test_changed_case_invalidates_resources_and_final_sync_repairs_prior_cdn_failure(self):
        self.change(); self.prepare_run(); self.apply_run()
        invalidations = [c for c in self.calls() if c[:2] == ['cloudfront', 'create-invalidation']]
        self.assertEqual(invalidations[0][invalidations[0].index('--paths') + 1:],
                         ['/cases/manifest.json', '/cases/a-case/*'])
        # The unconditional final step also repairs resource caches from earlier failed runs.
        self.assertEqual(invalidations[-1][invalidations[-1].index('--paths') + 1:], ['/cases/*'])

    def test_acknowledged_put_with_failed_readback_records_commit(self):
        self.change(); self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_FAIL_READ_AFTER_PUT': '1'}, success=False)
        state = self.status()[0]
        self.assertTrue(state['manifest_committed'])
        self.assertFalse(state['manifest_verified'])
        self.assertEqual(state['status'], 'failed')
        self.assertEqual(state['cdn'], 'waiting')
        self.assertNotEqual((self.target / 'manifest.json').read_text(), self.baseline)

    def test_uncertain_put_and_failed_readback_record_unknown_not_false(self):
        self.change(); self.prepare_run()
        self.apply_run(overrides={'FAKE_S3_TIMEOUT_AFTER_PUT': '1',
                                  'FAKE_S3_FAIL_READ_AFTER_PUT': '1'}, success=False)
        self.assertIsNone(self.status()[0]['manifest_committed'])
        self.assertFalse(self.status()[0]['manifest_verified'])
        self.assertEqual(self.status()[1]['status'], 'waiting')
