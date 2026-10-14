"""Exercise the real pipeline with deterministic overlap and case-local failures."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import threading
import time

from test_publish import GitFixture, publisher
from test_unpack import valid_files, declaration, archive_bytes


class MemoryS3:
    def __init__(self, baseline, overlap=1, fail_case=None, fail_cdn=None, latency=.002):
        self.latency = latency
        self.baseline = baseline
        self.overlap = overlap
        self.fail_case, self.fail_cdn = fail_case, fail_cdn
        self.lock = threading.Lock()
        self.gate = threading.Event()
        self.active = {}
        self.peak = self.peak_cases = 0
        self.per_case_peak = {}
        self.objects, self.commits, self.started, self.cleared = {}, [], [], []
        self.owner = threading.get_ident()

    def read_manifest(self):
        return self.baseline

    def head(self, key):
        value = self.objects.get(key)
        return {'ContentLength': len(value), 'Metadata': {'sha256': hashlib.sha256(value).hexdigest()}} if value is not None else None

    def clear_extracted(self, name):
        with self.lock:
            self.cleared.append(name)
            for key in list(self.objects):
                if key.startswith(name + '/extracted/'):
                    del self.objects[key]

    def upload(self, path, key):
        name = key.split('/')[0]
        with self.lock:
            self.started.append(key)
            self.active[name] = self.active.get(name, 0) + 1
            self.peak = max(self.peak, sum(self.active.values()))
            self.peak_cases = max(self.peak_cases, sum(n > 0 for n in self.active.values()))
            self.per_case_peak[name] = max(self.per_case_peak.get(name, 0), self.active[name])
            if sum(self.active.values()) >= self.overlap:
                self.gate.set()
        try:
            if not self.gate.wait(10):
                raise AssertionError('Expected concurrent transfers did not overlap')
            if name == self.fail_case:
                raise OSError('fixture upload failed for ' + name)
            time.sleep(self.latency)
            self.objects[key] = path.read_bytes()
        finally:
            with self.lock:
                self.active[name] -= 1

    def verify_upload(self, key, size, checksum):
        if not publisher.matching_head(self.head(key), {'bytes': size, 'sha256': checksum}):
            raise ValueError('fixture HEAD mismatch')

    def commit_manifest(self, path):
        assert threading.get_ident() == self.owner, 'Workers must never write the shared index'
        self.baseline = path.read_text()
        self.commits.append(json.loads(self.baseline))

    def refresh_cdn(self, name=None):
        if self.fail_cdn is not None and name == self.fail_cdn:
            raise OSError('fixture CDN failure')


class ParallelPublicationTests(GitFixture):
    def make_plan(self, count=5, objects=32):
        for n in range(1, count):
            self.add_case('Case ' + str(n), 'case-' + str(n))
        for entry in self.entries:
            files, inventory = valid_files()
            for n in range(objects):
                key = 'objects/' + str(n)
                files[key] = ('payload ' + str(n)).encode()
                inventory.append(declaration(key, files[key], storageKey='uploads/' + str(n)))
            data = archive_bytes(files, inventory)
            resource = entry['case']
            (self.root / resource['path']).write_bytes(data)
            resource.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        self.write_manifest()
        after = self.commit()
        return publisher.prepare(self.root, '[]', after, check_local=False)

    def execute(self, plan, s3, **kwargs):
        log = io.StringIO()
        with contextlib.redirect_stdout(log):
            publisher.apply(self.root, plan, s3, self.root / 'publication', prepare_cases=True, **kwargs)
        return log.getvalue()

    def statuses(self):
        return json.loads((self.root / 'publication/status.json').read_text())['steps']

    def test_four_cases_eight_files_overlap_and_index_has_one_writer(self):
        plan = self.make_plan()
        store = MemoryS3('[]', overlap=32)
        log = self.execute(plan, store)
        self.assertEqual(store.peak, 32)
        self.assertEqual(store.peak_cases, 4)
        self.assertTrue(all(n <= 8 for n in store.per_case_peak.values()))
        self.assertEqual(store.baseline, (self.root / 'manifest.json').read_text())
        self.assertEqual({entry['name'] for entry in store.commits[-1]}, {e['name'] for e in self.entries})
        self.assertTrue(all(s['status'] == 'completed' for s in self.statuses()))
        self.assertLess(len(log.splitlines()), 100)
        journal = (self.root / 'publication/events.jsonl').read_text()
        self.assertGreater(journal.count('"phase": "file"'), 300)

    def test_upload_failure_does_not_publish_failed_case_or_stop_other_cases(self):
        plan = self.make_plan()
        store = MemoryS3('[]', fail_case='a-case')
        with self.assertRaisesRegex(OSError, 'fixture upload failed'):
            self.execute(plan, store)
        self.assertEqual({e['name'] for e in json.loads(store.baseline)}, {'case-1', 'case-2', 'case-3', 'case-4'})
        self.assertTrue(all('a-case' not in {e['name'] for e in commit} for commit in store.commits))
        self.assertEqual(self.statuses()[-1]['status'], 'skipped')
        self.assertFalse(any(store.active.values()))
        self.assertLessEqual(sum(key.startswith('a-case/') for key in store.started), 8)

    def test_failed_extraction_is_local_and_never_clears_that_case(self):
        plan = self.make_plan(count=3)
        entry = self.entries[0]['case']
        data = b'not an archive'
        (self.root / entry['path']).write_bytes(data)
        entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, '[]', after, check_local=False)
        store = MemoryS3('[]')
        with self.assertRaises(Exception):
            self.execute(plan, store)
        self.assertNotIn('a-case', store.cleared)
        self.assertEqual({e['name'] for e in json.loads(store.baseline)}, {'case-1', 'case-2'})

    def test_missing_source_is_local_even_when_it_has_no_resource_candidate(self):
        self.make_plan(count=2)
        baseline = (self.root / 'manifest.json').read_text()
        self.entries[0]['title'] = 'Renamed'
        Path(self.root / self.entries[0]['cover']['path']).unlink()
        self.entry = self.entries[1]; self.change()
        plan = publisher.prepare(self.root, baseline, self.git('rev-parse', 'HEAD'), check_local=False)
        store = MemoryS3(baseline)
        with self.assertRaisesRegex(ValueError, 'missing'):
            self.execute(plan, store)
        published = {e['name']: e for e in json.loads(store.baseline)}
        self.assertNotEqual(published['a-case']['title'], 'Renamed')
        self.assertEqual(published['case-1'], self.entries[1])

    def test_cdn_failure_preserves_accepted_case_and_continues(self):
        plan = self.make_plan(count=3)
        store = MemoryS3('[]', fail_cdn='case-1')
        with self.assertRaisesRegex(OSError, 'CDN failure'):
            self.execute(plan, store)
        self.assertEqual(store.baseline, (self.root / 'manifest.json').read_text())
        failed = next(s for s in self.statuses() if s['name'] == 'case-1')
        self.assertTrue(failed['manifest_verified'])
        self.assertEqual(failed['cdn'], 'failed')
        self.assertEqual(self.statuses()[-1]['status'], 'completed')

    def test_fabricated_prepared_input_cannot_bypass_case_preparation(self):
        plan = self.make_plan(count=1)
        plan['files'] = [{'path': 'manifest.json', 'key': 'manifest.json'}]
        store = MemoryS3('[]')
        with self.assertRaises(ValueError):
            self.execute(plan, store)
        self.assertFalse(store.started or store.commits)

    def catalog_reuse_plan(self, shared_rename=False):
        self.make_plan(count=3, objects=2)
        baseline = copy.deepcopy(self.entries)
        old_labels = ['Data Science', 'Data Science' if shared_rename else 'Other', 'Free']
        old_ids = ['data-science', 'data-science' if shared_rename else 'other', 'free']
        for entry, label, identifier in zip(baseline, old_labels, old_ids):
            entry.update(catalog=label, catalog_name=identifier)
            for kind in publisher.KINDS:
                entry[kind]['path'] = label + '/' + entry['name'] + '/' + entry[kind]['file_name']
        new_labels = ['DataScience' if shared_rename else 'Biology', 'DataScience', 'Free']
        new_ids = ['data-science' if shared_rename else 'biology', 'data-science', 'free']
        for entry, label, identifier in zip(self.entries, new_labels, new_ids):
            entry.update(catalog=label, catalog_name=identifier)
            for kind in publisher.KINDS:
                item = entry[kind]
                target = self.root / label / entry['name'] / item['file_name']
                target.parent.mkdir(parents=True, exist_ok=True)
                (self.root / item['path']).rename(target)
                item['path'] = target.relative_to(self.root).as_posix()
            # Select actual writes so failure can be injected into the dependent group.
            item = entry['cover']; target = self.root / item['path']
            target.write_bytes(b'changed!')
            item.update(bytes=8, sha256=hashlib.sha256(b'changed!').hexdigest())
        self.write_manifest(); after = self.commit()
        text = json.dumps(baseline)
        return publisher.prepare(self.root, text, after, check_local=False), text

    def test_catalog_release_and_reuse_form_one_independent_commit_unit(self):
        from publication_runner import next_manifest
        plan, baseline = self.catalog_reuse_plan()
        groups = [s for s in plan['steps'] if s['operation'] not in ('REORDER', 'FINAL_SYNC')]
        self.assertEqual(len(groups), 2)
        group = next(s for s in groups if s['operation'] == 'UPDATE_CATALOG')
        self.assertEqual({e['name'] for e in group['after']}, {'a-case', 'case-1'})
        # Both completion orders must be valid against the accepted baseline.
        for order in (groups, list(reversed(groups))):
            current = baseline
            for step in order:
                current = next_manifest(current, step)
            self.assertEqual({e['name']: e for e in json.loads(current)},
                             {e['name']: e for e in self.entries})
        store = MemoryS3(baseline)
        self.execute(plan, store)
        self.assertEqual(store.baseline, (self.root / 'manifest.json').read_text())

    def test_interleaved_unrelated_case_is_not_absorbed_by_catalog_group(self):
        plan, baseline = self.catalog_reuse_plan(shared_rename=True)
        # Put the independent update between the two dependent operations.
        self.entries[:] = [self.entries[0], self.entries[2], self.entries[1]]
        self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, baseline, after, check_local=False)
        group = next(s for s in plan['steps'] if s['operation'] == 'UPDATE_CATALOG')
        self.assertEqual({e['name'] for e in group['after']}, {'a-case', 'case-1'})
        self.assertTrue(any(s['name'] == 'case-2' for s in plan['steps']))
        store = MemoryS3(baseline, fail_case='a-case')
        with self.assertRaises(OSError):
            self.execute(plan, store)
        published = {e['name']: e for e in json.loads(store.baseline)}
        self.assertEqual(published['case-2'], self.entries[1])

    def test_failed_catalog_group_does_not_block_unrelated_case(self):
        plan, baseline = self.catalog_reuse_plan()
        store = MemoryS3(baseline, fail_case='a-case')
        with self.assertRaises(OSError):
            self.execute(plan, store)
        published = {e['name']: e for e in json.loads(store.baseline)}
        old = {e['name']: e for e in json.loads(baseline)}
        self.assertEqual(published['a-case'], old['a-case'])
        self.assertEqual(published['case-1'], old['case-1'])
        self.assertEqual(published['case-2'], self.entries[2])
        self.assertFalse(any(key.startswith('case-1/') for key in store.started))

    def test_global_commit_conflict_stops_scheduling_and_drains_workers(self):
        import subprocess
        plan = self.make_plan(count=5, objects=8)
        store = MemoryS3('[]', overlap=32)
        def conflict(path):
            raise subprocess.CalledProcessError(1, ['fixture'], stderr='PreconditionFailed')
        store.commit_manifest = conflict
        with self.assertRaises(subprocess.CalledProcessError):
            self.execute(plan, store)
        self.assertFalse(store.commits)
        self.assertFalse(any(store.active.values()))
        self.assertEqual(len({key.split('/')[0] for key in store.started}), 4)
        self.assertEqual(self.statuses()[-1]['status'], 'waiting')

    def test_invalid_concurrency_fails_before_writes(self):
        plan = self.make_plan(count=1)
        for cases, files in [(0, 8), (4, 0), (17, 1), (4, 33), (16, 8)]:
            with self.subTest(cases=cases, files=files), self.assertRaises(ValueError):
                self.execute(plan, MemoryS3('[]'), case_workers=cases, file_workers=files)
