"""Exercise the actual migrated repository index against a historical S3 baseline."""
import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path

from test_publish import GitFixture, publisher
from test_resource_sources import Store


class MigrationTests(GitFixture):
    def test_real_migrated_manifest_has_no_resource_work_and_is_committed(self):
        repository = Path(__file__).resolve().parents[2]
        target_text = (repository / 'manifest.json').read_text()
        entries = publisher.read_manifest(target_text, 'migrated repository', legacy=False)
        baseline = copy.deepcopy(entries)
        resource_objects = {}
        for old, entry in zip(baseline, entries):
            del old['catalog'], old['catalog_name']
            for kind in publisher.KINDS:
                resource = entry[kind]
                old[kind]['path'] = resource['path'].removeprefix('usecases/')
                if kind != 'case':
                    del old[kind]['release_url']
                source = repository / resource['path']
                if not resource['release_url']:
                    self.assertEqual(publisher.file_integrity(source), (resource['bytes'], resource['sha256'].lower()))
                    destination = self.root / resource['path']
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    # Read-only links avoid duplicating hundreds of MB; no test writes these resources.
                    os.link(source, destination)
                resource_objects[entry['name']+'/'+resource['file_name']] = resource['sha256'].encode()
                resource_objects[entry['name']+'/extracted/keep'] = b'unchanged extracted bytes'
        (self.root / 'manifest.json').write_text(target_text)
        self.git('add', 'manifest.json')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'test: migrated manifest')
        after = self.git('rev-parse', 'HEAD')
        baseline_text = json.dumps(baseline)
        plan = publisher.prepare(self.root, baseline_text, after)
        self.assertEqual(plan['candidates'], [])
        self.assertEqual(plan['packages'], [])
        self.assertTrue(all(step['files'] == [] and step['packages'] == [] for step in plan['steps']))
        store = Store(baseline_text)
        store.objects = copy.deepcopy(resource_objects)
        with contextlib.redirect_stdout(io.StringIO()):
            publisher.apply(self.root, plan, store)
        self.assertEqual(store.manifest, target_text)
        self.assertEqual(store.objects, resource_objects)
        self.assertEqual(store.heads, [])
        self.assertTrue(store.writes)
        self.assertEqual(set(store.writes), {'manifest.json'})
