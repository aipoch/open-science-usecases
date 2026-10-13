"""Unified resource rules, isolated source preparation and target-side deduplication."""
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

from test_publish import GitFixture, publisher
import check_structure as checker


class Store:
    def __init__(self, baseline=None):
        self.manifest = baseline
        self.objects = {}
        self.heads = []
        self.writes = []

    def head(self, key):
        self.heads.append(key)
        return copy.deepcopy(self.objects.get(key))

    def read_manifest(self):
        return self.manifest

    def commit_manifest(self, path):
        self.manifest = path.read_text()
        self.writes.append('manifest.json')

    def refresh_cdn(self, case_name=None):
        pass

    def upload(self, path, key):
        size, sha = publisher.file_integrity(path)
        self.objects[key] = {'ContentLength': size, 'Metadata': {'sha256': sha}}
        self.writes.append(key)

    def verify_upload(self, key, size, sha):
        assert self.objects[key] == {'ContentLength': size, 'Metadata': {'sha256': sha}}


class SourcesTests(GitFixture):
    def setUp(self):
        super().setUp()
        if not self.entry['cover']['path'].startswith('usecases/'):
            (self.root / 'usecases').mkdir()
            (self.root / 'A Case').rename(self.root / 'usecases/A Case')
            for kind in ('cover', 'case', 'introduction'):
                self.entry[kind]['path'] = 'usecases/' + self.entry[kind]['path']
                self.entry[kind]['release_url'] = ''
            self.write_manifest()
            self.base = self.commit()

    def stage(self, plan, store):
        return publisher.prepare_resources(self.root, plan, store, self.root / 'staging')

    def test_path_migration_only_updates_index(self):
        old = copy.deepcopy(self.entries)
        for kind in ('cover', 'case', 'introduction'):
            old[0][kind]['path'] = old[0][kind]['path'].removeprefix('usecases/')
            if kind != 'case':
                del old[0][kind]['release_url']
        baseline = json.dumps(old)
        plan = publisher.prepare(self.root, baseline, self.base)
        self.assertEqual(plan['packages'], [])
        self.assertEqual(plan['candidates'], [])
        store = Store(baseline)
        publisher.apply(self.root, plan, store)
        self.assertEqual(store.manifest, (self.root / 'manifest.json').read_text())
        self.assertEqual(set(store.writes), {'manifest.json'})
        self.assertEqual(store.heads, [])

    def test_eight_source_combinations_without_body_download(self):
        for flags in itertools.product((False, True), repeat=3):
            with self.subTest(flags=flags):
                entry = copy.deepcopy(self.entry)
                for kind, remote in zip(('cover', 'case', 'introduction'), flags):
                    resource = entry[kind]
                    path = self.root / resource['path']
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(b'original')
                    if remote:
                        path.unlink()
                        resource['release_url'] = 'https://example.invalid/' + resource['file_name'].replace(' ', '-')
                if all(flags):
                    shutil.rmtree(self.root / 'usecases/A Case')
                self.assertEqual(checker.schema_errors(entry), [])
                self.assertEqual(checker.source_errors(self.root, entry), [])
                with patch.object(checker, 'validate_head_size') as head:
                    previous = Path.cwd()
                    os.chdir(self.root)
                    self.addCleanup(os.chdir, previous)
                    (self.root / 'manifest.json').write_text(json.dumps([entry]))
                    self.assertEqual(checker.validate_manifest(checker.selected_cases([entry])), [])
                    self.assertEqual(head.call_count, sum(flags))
                    os.chdir(previous)

    def test_metadata_dedup_and_revalidation(self):
        self.change()
        plan = self.plan()
        store = Store(plan['baseline'])
        key = 'a-case/A Case.png'
        store.objects[key] = {'ContentLength': 8, 'Metadata': {'sha256': self.entry['cover']['sha256'].upper()}}
        staged = self.stage(plan, store)
        self.assertEqual([f['key'] for f in staged['files']], ['manifest.json'])
        self.assertEqual(staged['decisions'][0]['action'], 'skip')
        publisher.apply(self.root, staged, store)
        self.assertNotIn(key, store.writes)
        store.manifest = plan['baseline']
        store.objects[key]['ContentLength'] = 9
        with self.assertRaisesRegex(ValueError, 'skip|changed'):
            publisher.apply(self.root, staged, store)

    def test_source_switch_forces_each_kind_even_with_same_target_sha(self):
        for kind in ('cover', 'case', 'introduction'):
            old = copy.deepcopy(self.entries)
            old[0][kind]['release_url'] = 'https://example.invalid/' + old[0][kind]['file_name'].replace(' ', '-')
            plan = publisher.prepare(self.root, json.dumps(old), self.base)
            candidate = plan['candidates'][0]
            self.assertTrue(candidate['force_upload'])
            self.assertEqual(candidate['kind'], kind)
            store = Store(plan['baseline'])
            store.objects[candidate['key']] = {'ContentLength': 8, 'Metadata': {'sha256': candidate['sha256']}}
            staged = self.stage(plan, store)
            self.assertEqual(store.heads, [])
            self.assertIn(candidate['key'], [f['key'] for f in staged['files']])
            self.assertEqual(bool(plan['packages']), kind == 'case')

    def test_schema_rejects_bad_fields_and_accepts_independent_names(self):
        self.entry['title'] = 'Unrelated display title'
        self.entry['name'] = 'different-name'
        self.assertEqual(checker.schema_errors(self.entry), [])
        for field, value in [('bytes', True), ('sha256', 'x'*64), ('file_name', None),
                             ('path', 'usecases/x/../a.png'), ('path', 'Old/a.png'),
                             ('release_url', None), ('release_url', ' '), ('release_url', 'file:///tmp/a.png')]:
            entry = copy.deepcopy(self.entry)
            entry['cover'][field] = value
            with self.subTest(field=field, value=value):
                self.assertTrue(checker.schema_errors(entry))

    def test_tampered_plan_and_staged_file_rejected_before_writes(self):
        self.change()
        plan = self.plan()
        store = Store(plan['baseline'])
        staged = self.stage(plan, store)
        missing = copy.deepcopy(staged)
        missing['files'] = [f for f in missing['files'] if f['key'] == 'manifest.json']
        with self.assertRaises(ValueError):
            publisher.apply(self.root, missing, store)
        Path(staged['files'][0]['path']).write_bytes(b'corrupt!')
        with self.assertRaises(ValueError):
            publisher.apply(self.root, staged, store)
        self.assertEqual(store.writes, [])

    def test_metadata_variants_and_head_errors(self):
        self.change()
        plan = self.plan()
        key = plan['candidates'][0]['key']
        for head in (None, {}, {'ContentLength': 8}, {'ContentLength': 8, 'Metadata': {}},
                     {'ContentLength': 8, 'Metadata': {'sha256': 'f'*64}},
                     {'ContentLength': 9, 'Metadata': {'sha256': self.entry['cover']['sha256']}}):
            with self.subTest(head=head):
                store = Store(plan['baseline']); store.objects[key] = head
                staged = self.stage(plan, store)
                self.assertEqual(staged['decisions'][0]['action'], 'upload')
                self.assertEqual(store.heads, [key])
        for error in (PermissionError('403'), OSError('network')):
            store = Store(plan['baseline'])
            with patch.object(store, 'head', side_effect=error), self.assertRaises(OSError):
                self.stage(plan, store)
            self.assertEqual(store.writes, [])

    def test_forged_skip_forced_or_missing_evidence_is_rejected(self):
        self.change()
        raw = self.plan(); store = Store(raw['baseline'])
        staged = self.stage(raw, store)
        staged['decisions'][0].update(action='skip', head=None)
        staged['files'] = staged['files'][-1:]
        publisher.group_files(staged)
        with self.assertRaisesRegex(ValueError, 'skip'):
            publisher.apply(self.root, staged, store)
        old = copy.deepcopy(self.entries)
        old[0]['cover']['release_url'] = 'https://example.invalid/cover.png'
        raw = publisher.prepare(self.root, json.dumps(old), self.git('rev-parse', 'HEAD'))
        staged = self.stage(raw, store)
        item = raw['candidates'][0]
        staged['decisions'][0].update(action='skip', reason='target SHA and size match',
                                     head={'ContentLength': item['bytes'], 'Metadata': {'sha256': item['sha256']}})
        staged['files'] = staged['files'][-1:]; publisher.group_files(staged)
        with self.assertRaisesRegex(ValueError, 'skip'):
            publisher.apply(self.root, staged, store)
        self.assertEqual(store.writes, [])

    def test_omitting_forced_candidate_is_rejected(self):
        old = copy.deepcopy(self.entries); old[0]['introduction']['release_url'] = 'https://example.invalid/i.md'
        raw = publisher.prepare(self.root, json.dumps(old), self.base)
        raw['candidates'] = []; raw['files'] = raw['files'][-1:]; publisher.group_files(raw)
        store = Store(raw['baseline'])
        with self.assertRaises(ValueError):
            publisher.apply(self.root, raw, store)
        self.assertEqual(store.writes, [])

    def test_legacy_missing_introduction_can_be_upgraded(self):
        old = copy.deepcopy(self.entries); del old[0]['introduction']
        plan = publisher.prepare(self.root, json.dumps(old), self.base)
        self.assertEqual([f['kind'] for f in plan['candidates']], ['introduction'])

    def test_changed_name_uses_existing_record_and_residual_objects(self):
        old = copy.deepcopy(self.entries)
        self.entry['name'] = 'new-name'; self.write_manifest(); after = self.commit()
        existing = copy.deepcopy(self.entry)
        plan = publisher.prepare(self.root, json.dumps(old+[existing]), after)
        self.assertEqual(plan['candidates'], [])
        plan = publisher.prepare(self.root, json.dumps(old), after)
        self.assertEqual(len(plan['candidates']), 3)
        store = Store(plan['baseline'])
        for item in plan['candidates']:
            store.objects[item['key']] = {'ContentLength': item['bytes'], 'Metadata': {'sha256': item['sha256']}}
        staged = self.stage(plan, store)
        self.assertEqual([f['kind'] for f in staged['files'] if 'kind' in f], ['case'])
        self.assertEqual(len(staged['packages']), 1)

    def test_local_checkout_mutation_is_rejected_during_preparation(self):
        self.change(); plan = self.plan()
        (self.root / self.entry['cover']['path']).write_bytes(b'tampered')
        store = Store(plan['baseline'])
        with self.assertRaises(Exception):
            self.stage(plan, store)
        self.assertEqual(store.writes, [])

    def test_size_and_filename_changes_are_candidates(self):
        for field, value in [('bytes', 7), ('sha256', 'f'*64), ('file_name', 'old.png')]:
            old = copy.deepcopy(self.entries)
            old[0]['cover'][field] = value
            if field == 'file_name':
                old[0]['cover']['path'] = 'usecases/A Case/old.png'
            plan = publisher.prepare(self.root, json.dumps(old), self.base)
            self.assertEqual(plan['candidates'][0]['reasons'], [field])
            self.assertEqual(plan['packages'], [])

    def test_target_s3_head_missing_permission_and_network(self):
        from test_publish import PublishTests
        store_path, env = PublishTests.s3_fixture(self)
        with patch.dict(os.environ, env):
            store = publisher.S3(env['AWS_TARGET_FOLDER'])
            self.assertIsNone(store.head('absent.png'))
            for code in ('AccessDenied', 'RequestTimeout', '500'):
                with patch.dict(os.environ, {'FAKE_S3_HEAD_ERROR': code}), self.assertRaises(ValueError):
                    store.head('absent.png')

    def test_untracked_local_source_cannot_enter_fixed_checkout_publication(self):
        self.git('rm', '--cached', self.entry['cover']['path'])
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'test: remove tracked resource')
        plan = publisher.prepare(self.root, None, self.git('rev-parse', 'HEAD'))
        store = Store(None)
        with self.assertRaisesRegex(ValueError, 'committed'):
            self.stage(plan, store)
        self.assertEqual(store.writes, [])
