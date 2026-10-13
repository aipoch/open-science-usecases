"""Real HTTP downloads for all source combinations and switching each resource kind."""
import contextlib
import copy
import hashlib
from http.server import ThreadingHTTPServer
import io
import itertools
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import threading
from unittest.mock import patch

from test_extract_science import DownloadHandler, package_bytes
from test_publish import GitFixture, SCRIPTS, publisher
from test_resource_sources import Store
import extract_science


class RemoteResourcesTests(GitFixture):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), DownloadHandler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.http.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown(); cls.http.server_close(); cls.thread.join()

    def setUp(self):
        super().setUp()
        self.http.requests = []; self.http.head_requests = []; self.http.responses = {}
        self.package = package_bytes()

    def set_source(self, kind, remote, suffix=''):
        resource = self.entry[kind]
        body = self.package if kind == 'case' else {'cover': b'cover-v1', 'introduction': b'intro-v1'}[kind]
        path = self.root / resource['path']
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        url_path = '/' + kind + suffix + Path(resource['file_name']).suffix
        self.http.responses[url_path] = body
        resource.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                        release_url=self.url+url_path if remote else '')
        if remote:
            path.unlink()

    def staged(self, plan, store):
        return publisher.prepare_resources(self.root, plan, store, self.root / 'sources')

    def test_eight_combinations_prepare_download_once_extract_and_publish(self):
        for flags in itertools.product((False, True), repeat=3):
            with self.subTest(flags=flags), contextlib.redirect_stdout(io.StringIO()):
                self.http.requests = []
                for kind, remote in zip(publisher.KINDS, flags):
                    self.set_source(kind, remote)
                self.write_manifest(); after = self.commit()
                plan = publisher.prepare(self.root, None, after)
                store = Store(None); store.clears = []
                store.clear_extracted = store.clears.append
                plan = self.staged(plan, store)
                plan = extract_science.expand_plan(self.root, plan, self.root / 'staging')
                publisher.apply(self.root, plan, store)
                self.assertEqual(len(self.http.requests), sum(flags))
                self.assertEqual(len(set(self.http.requests)), sum(flags))
                self.assertEqual(store.clears, ['a-case'])
                self.assertEqual(store.manifest, (self.root / 'manifest.json').read_text())
                for kind in publisher.KINDS:
                    self.assertIn('a-case/'+self.entry[kind]['file_name'], store.writes)

    def test_every_source_switch_forces_upload_despite_target_metadata(self):
        for kind in publisher.KINDS:
            for before_remote, after_remote, url_suffix in [(False, True, ''), (True, False, ''), (True, True, '-new')]:
                with self.subTest(kind=kind, transition=(before_remote,after_remote)), contextlib.redirect_stdout(io.StringIO()):
                    for k in publisher.KINDS:
                        self.set_source(k, False)
                    self.set_source(kind, before_remote)
                    old = copy.deepcopy(self.entries)
                    self.set_source(kind, after_remote, url_suffix)
                    self.write_manifest(); after = self.commit()
                    plan = publisher.prepare(self.root, json.dumps(old), after)
                    self.assertEqual(len(plan['candidates']), 1)
                    item = plan['candidates'][0]
                    self.assertTrue(item['force_upload'])
                    store = Store(plan['baseline']); store.clear_extracted = lambda name: None
                    store.objects[item['key']] = {'ContentLength': item['bytes'], 'Metadata': {'sha256': item['sha256']}}
                    plan = self.staged(plan, store)
                    self.assertEqual(store.heads, [])
                    if kind == 'case':
                        plan = extract_science.expand_plan(self.root, plan, self.root / 'staging')
                    publisher.apply(self.root, plan, store)
                    self.assertIn(item['key'], store.writes)

    def test_remote_candidate_dedup_uses_target_without_downloading_source(self):
        self.set_source('cover', True)
        self.write_manifest(); after = self.commit()
        # Unchanged URL with changed digest is a candidate, not a forced source switch.
        old = copy.deepcopy(self.entries); old[0]['cover']['sha256'] = 'f'*64
        plan = publisher.prepare(self.root, json.dumps(old), after)
        item = plan['candidates'][0]; store = Store(plan['baseline'])
        store.objects[item['key']] = {'ContentLength': item['bytes'], 'Metadata': {'sha256': item['sha256']}}
        plan = self.staged(plan, store)
        self.assertEqual(self.http.requests, [])
        with contextlib.redirect_stdout(io.StringIO()):
            publisher.apply(self.root, plan, store)
        self.assertEqual(store.heads, [item['key'], item['key']])
        self.assertNotIn(item['key'], store.writes)

    def test_remote_size_sha_and_truncation_fail_before_writes(self):
        for kind in publisher.KINDS:
            self.set_source(kind, True)
            self.write_manifest(); after = self.commit()
            old = copy.deepcopy(self.entries); old[0][kind]['release_url'] = ''
            plan = publisher.prepare(self.root, json.dumps(old), after)
            from urllib.parse import urlsplit
            url_path = urlsplit(self.entry[kind]['release_url']).path
            valid = self.http.responses[url_path]
            for body in (valid[:-1], valid+b'x', bytes([valid[0]^1])+valid[1:]):
                with self.subTest(kind=kind, body_length=len(body)):
                    self.http.responses[url_path] = body
                    store = Store(plan['baseline'])
                    with self.assertRaises(ValueError):
                        self.staged(plan, store)
                    self.assertEqual(store.writes, [])
            self.set_source(kind, False)

    def test_extracted_inventory_omission_injection_and_rehashed_tampering_fail(self):
        self.set_source('case', True)
        self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, None, after)
        store = Store(None); store.clear_extracted = lambda name: self.fail('unexpected delete')
        with contextlib.redirect_stdout(io.StringIO()):
            plan = extract_science.expand_plan(self.root, self.staged(plan, store), self.root / 'staging')
        for mutation in ('omit', 'rename', 'rehash', 'force'):
            altered = copy.deepcopy(plan)
            item = next(f for f in altered['files'] if f['key'].endswith('/extracted/uploads/project/data.csv'))
            if mutation == 'omit':
                altered['files'].remove(item)
            elif mutation == 'rename':
                item['key'] = item['key'].replace('data.csv', 'other.csv')
            elif mutation == 'rehash':
                body = b'tampered data'
                Path(item['path']).write_bytes(body)
                item.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
            else:
                altered['candidates'][0]['force_upload'] = True
            publisher.group_files(altered)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                publisher.apply(self.root, altered, store)
            self.assertEqual(store.writes, [])

    def check_classified_manifest(self, plan):
        result = subprocess.run(
            [sys.executable, '-B', str(SCRIPTS / 'check_structure.py'), 'manifest'],
            cwd=self.root, env={**os.environ, 'CASES_JSON': json.dumps(plan['cases'])},
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def classify_resources(self):
        for kind, directory in zip(publisher.KINDS, ('分类/物理/图片', 'packages/deep/session', 'docs/zh')):
            resource = self.entry[kind]
            old = self.root / resource['path']
            resource['path'] = directory + '/' + resource['file_name']
            if old.exists():
                old.unlink()
        shutil.rmtree(self.root / 'usecases')
        self.entry['title'] = 'Display title unrelated to any directory'

    def test_classified_eight_combinations_check_head_then_prepare_and_publish(self):
        self.classify_resources()
        for flags in itertools.product((False, True), repeat=3):
            with self.subTest(flags=flags), contextlib.redirect_stdout(io.StringIO()):
                self.http.requests = []; self.http.head_requests = []
                for kind, remote in zip(publisher.KINDS, flags):
                    self.set_source(kind, remote)
                    if remote:
                        # Remote resources do not depend on an unrelated local resource's parent.
                        shutil.rmtree((self.root / self.entry[kind]['path']).parent)
                self.write_manifest(); after = self.commit()
                plan = publisher.prepare(self.root, None, after)
                self.check_classified_manifest(plan)
                expected = ['/' + kind + Path(self.entry[kind]['file_name']).suffix
                            for kind, remote in zip(publisher.KINDS, flags) if remote]
                self.assertCountEqual(self.http.head_requests, expected)
                self.assertEqual(self.http.requests, [])
                store = Store(None); store.clears = []
                store.clear_extracted = store.clears.append
                plan = self.staged(plan, store)
                plan = extract_science.expand_plan(self.root, plan, self.root / 'staging')
                publisher.apply(self.root, plan, store)
                self.assertCountEqual(self.http.requests, expected)
                self.assertEqual(store.clears, ['a-case'])
                self.assertEqual(store.manifest, (self.root / 'manifest.json').read_text())
                for kind in publisher.KINDS:
                    key = 'a-case/' + self.entry[kind]['file_name']
                    self.assertEqual(store.objects[key]['Metadata']['sha256'], self.entry[kind]['sha256'])

    def test_remote_path_only_reclassification_checks_head_without_downloading_or_uploading(self):
        self.classify_resources()
        for kind in publisher.KINDS:
            self.set_source(kind, True)
        self.write_manifest(); self.commit()
        for kind in publisher.KINDS:
            with self.subTest(kind=kind), contextlib.redirect_stdout(io.StringIO()):
                old = json.dumps(self.entries)
                self.entry[kind]['path'] = 'remote/新分类/' + kind + '/' + self.entry[kind]['file_name']
                self.write_manifest(); after = self.commit()
                plan = publisher.prepare(self.root, old, after)
                self.http.head_requests = []
                self.check_classified_manifest(plan)
                self.assertCountEqual(self.http.head_requests, ['/cover.png', '/case.science', '/introduction.md'])
                self.assertEqual(plan['candidates'], [])
                self.assertEqual(plan['packages'], [])
                store = Store(old)
                store.objects = {'a-case/extracted/session.json': b'existing replay'}
                store.clear_extracted = lambda name: self.fail('path-only move cleared a package')
                publisher.apply(self.root, plan, store)
                self.assertEqual(store.objects, {'a-case/extracted/session.json': b'existing replay'})
                self.assertEqual(store.heads, [])
                self.assertEqual(set(store.writes), {'manifest.json'})
                self.assertEqual(self.http.requests, [])
                self.assertEqual(json.loads(store.manifest), self.entries)
