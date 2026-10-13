"""Real temporary Git trees; only external upload is replaced."""
import copy
import hashlib
import shutil
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import publish as publisher


class GitFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.git('init', '-q')
        self.git('config', 'core.autocrlf', 'false')
        (self.root / '.git/info/exclude').write_text('sources/\nstaging/\ns3/\nbin/\nplan*\npublication*\nresource-publication/\nscience-publication/\n')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        self.entries = []
        self.write_manifest()
        self.initial = self.commit()
        self.entry = self.add_case('A Case', 'a-case')
        self.write_manifest()
        self.base = self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.PIPE).decode().strip()

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-qm', 'test: fixture')
        return self.git('rev-parse', 'HEAD')

    def add_case(self, title, name):
        entry = {'title': title, 'name': name}
        for kind, ext in [('cover', 'png'), ('case', 'science'), ('introduction', 'md')]:
            file = title + '.' + ext
            path = 'usecases/' + title + '/' + file
            (self.root / 'usecases' / title).mkdir(parents=True, exist_ok=True)
            (self.root / path).write_bytes(b'original')
            entry[kind] = {'path': path, 'file_name': file, 'bytes': 8, 'sha256': hashlib.sha256(b'original').hexdigest()}
            entry[kind]['release_url'] = ''
        self.entries.append(entry)
        return entry

    def write_manifest(self):
        (self.root / 'manifest.json').write_text(json.dumps(self.entries))

    def change(self, kind='cover', declaration=None):
        resource = self.entry[kind]
        (self.root / resource['path']).write_bytes(b'modified')  # Same length.
        resource['sha256'] = (hashlib.sha256(b'modified').hexdigest() if declaration is None
                              else declaration if len(declaration) == 64 else declaration * 64)
        self.write_manifest()
        return self.commit()

    def plan(self, before=None, after=None):
        baseline = self.git('show', (before or self.base) + ':manifest.json')
        return publisher.prepare(self.root, baseline, after or self.git('rev-parse', 'HEAD'))

    def ready(self, plan):
        class EmptyTarget:
            def head(self, key):
                return None
        return publisher.prepare_resources(self.root, plan, EmptyTarget(), self.root / 'sources')

    def keys(self, plan):
        return [item['key'] for item in plan['files']]


class PublishTests(GitFixture):
    # Publication must retain the cover extension accepted by the check stages.
    def test_image_cover_formats_are_preserved_in_publication_plan(self):
        for extension in ('jpg', 'JPEG', 'webp', 'gif', 'svg', 'avif'):
            with self.subTest(extension=extension):
                cover = self.entry['cover']
                filename = 'A Case.' + extension
                path = 'usecases/A Case/' + filename
                (self.root / cover['path']).rename(self.root / path)
                cover.update(file_name=filename, path=path)
                self.write_manifest()
                after = self.commit()
                plan = publisher.prepare(self.root, None, after)
                self.assertIn('a-case/' + filename, self.keys(plan))
                self.assertEqual(self.keys(publisher.prepare(self.root, json.dumps(self.entries), after)), ['manifest.json'])

    def test_nonimage_cover_is_rejected_by_publication(self):
        for extension in ('txt', 'pdf', 'mp4', 'unknown', 'png.gz'):
            with self.subTest(extension=extension):
                entry = copy.deepcopy(self.entry)
                entry['cover'].update(file_name='A Case.' + extension,
                                      path='A Case/A Case.' + extension)
                with self.assertRaises(ValueError):
                    publisher.read_manifest(json.dumps([entry]), 'fixture')

    def test_missing_s3_manifest_plans_every_declared_local_resource_and_package(self):
        plan = publisher.prepare(self.root, None, self.base)
        self.assertEqual(self.keys(plan), ['a-case/A Case.png', 'a-case/A Case.science',
                                          'a-case/A Case.md', 'manifest.json'])
        self.assertEqual(plan['packages'], [{'name': 'a-case', 'resource': self.entry['case']}])

    def test_s3_baseline_is_independent_of_git_ancestry(self):
        baseline = copy.deepcopy(self.entries)
        baseline[0]['cover']['sha256'] = 'f' * 64
        plan = publisher.prepare(self.root, json.dumps(baseline), self.base)
        self.assertEqual(self.keys(plan), ['a-case/A Case.png', 'manifest.json'])

    def test_incremental_uploads_skip_unchanged_resources(self):
        self.change(); self.change('introduction')
        self.assertEqual(self.keys(self.plan()),
                         ['a-case/A Case.png', 'a-case/A Case.md', 'manifest.json'])
        self.assertEqual(self.plan()['packages'], [])

    def test_package_changes_select_upload_and_extraction(self):
        self.change('case')
        self.assertEqual(self.keys(self.plan()), ['a-case/A Case.science', 'manifest.json'])
        self.assertEqual(self.plan()['packages'], [{'name': 'a-case', 'resource': self.entry['case']}])

    def test_remote_package_source_change_selects_upload_and_extraction(self):
        (self.root / self.entry['case']['path']).unlink()
        self.entry['case']['release_url'] = 'https://example.com/new.science'
        self.write_manifest(); self.commit()
        self.assertEqual(self.keys(self.plan()), ['a-case/A Case.science', 'manifest.json'])
        self.assertEqual(len(self.plan()['packages']), 1)

    def test_remote_to_local_switch_uploads_and_extracts(self):
        old = copy.deepcopy(self.entries)
        old[0]['case']['release_url'] = 'https://example.com/old.science'
        plan = publisher.prepare(self.root, json.dumps(old), self.base)
        self.assertEqual(self.keys(plan), ['a-case/A Case.science', 'manifest.json'])
        self.assertEqual(len(plan['packages']), 1)

    def test_new_case_and_unlisted_files(self):
        self.add_case('B Case', 'b-case'); self.write_manifest(); self.commit()
        (self.root / 'unlisted.txt').write_text('ignored')
        self.assertEqual(self.keys(self.plan()), ['b-case/B Case.png', 'b-case/B Case.science',
                                                 'b-case/B Case.md', 'manifest.json'])

    def test_unchanged_manifest_and_file_only_changes_skip(self):
        (self.root / self.entry['case']['path']).write_bytes(b'file-only edit')
        self.commit()
        self.assertEqual(self.keys(self.plan()), ['manifest.json'])
        self.assertEqual(self.plan()['packages'], [])

    def test_metadata_and_formatting_changes_publish_manifest_last(self):
        self.entry['title'] = 'Description only'; self.write_manifest(); self.commit()
        self.assertEqual(self.keys(self.plan()), ['manifest.json'])
        (self.root / 'manifest.json').write_text(json.dumps(self.entries, indent=2)); self.commit()
        self.assertEqual(self.keys(self.plan()), ['manifest.json'])

    def test_removed_entry_preserves_original_and_extracted_objects(self):
        objects = {'a-case/A Case.png': b'old', 'a-case/extracted/stale': b'keep'}
        self.entries = []; self.write_manifest(); self.commit()
        shutil.rmtree(self.root / 'usecases/A Case')
        plan = self.plan()
        self.assertEqual(self.keys(plan), ['manifest.json'])
        class Upload:
            manifest = plan['baseline']
            def read_manifest(inner):
                return inner.manifest
            def commit_manifest(inner, path):
                inner.manifest = path.read_text()
                objects['manifest.json'] = path.read_bytes()
            def refresh_cdn(inner, case_name=None, final=False):
                pass
            def upload(inner, path, key):
                objects[key] = path.read_bytes()
        publisher.apply(self.root, plan, Upload())
        self.assertEqual(objects, {'a-case/A Case.png': b'old',
                                  'a-case/extracted/stale': b'keep', 'manifest.json': b'[]'})

    def test_empty_first_publication_still_uploads_manifest(self):
        self.entries = []; self.write_manifest(); after = self.commit()
        self.assertEqual(self.keys(publisher.prepare(self.root, None, after)), ['manifest.json'])

    def test_missing_source_anywhere_in_changed_case_fails_during_preparation(self):
        self.change()
        for kind in ('cover', 'introduction', 'case'):
            with self.subTest(kind=kind):
                path = self.root / self.entry[kind]['path']
                data = path.read_bytes(); path.unlink()
                with self.assertRaisesRegex(ValueError, 'missing|Missing|source'):
                    self.plan()
                path.write_bytes(data)
        shutil.rmtree(self.root / 'usecases/A Case')
        with self.assertRaisesRegex(ValueError, 'directory'):
            self.plan()

    def test_dual_or_invalid_package_sources_fail(self):
        self.change()
        for url in ('https://example.com/a.science', ' ', 'file:///tmp/a.science'):
            with self.subTest(url=url):
                self.entry['case']['release_url'] = url; self.write_manifest(); self.commit()
                with self.assertRaises(ValueError):
                    self.plan()
        (self.root / self.entry['case']['path']).unlink()
        for url in ('', ' ', 'file:///tmp/a.science'):
            with self.subTest(url=url):
                self.entry['case']['release_url'] = url; self.write_manifest(); self.commit()
                with self.assertRaises(ValueError):
                    self.plan()

    def test_invalid_s3_manifest_never_means_first_publication(self):
        invalid = ['', '{', '{}', 'null', '[1]', '[{}]', '[{"name":"a","name":"b"}]']
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                publisher.prepare(self.root, text, self.base)
        for field, value in [('sha256', 'bad'), ('path', '../outside'), ('bytes', True)]:
            old = copy.deepcopy(self.entries); old[0]['cover'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                publisher.prepare(self.root, json.dumps(old), self.base)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            publisher.prepare(self.root, json.dumps(self.entries * 2), self.base)

    def test_missing_introduction_is_rejected(self):
        del self.entry['introduction']; self.write_manifest(); after = self.commit()
        with self.assertRaisesRegex(ValueError, 'introduction'):
            publisher.prepare(self.root, None, after)

    def test_case_name_is_independent_of_directory(self):
        self.entry['name'] = 'unrelated-name'; self.write_manifest(); self.commit()
        self.assertEqual(len(self.plan()['candidates']), 3)

    def test_wrong_checkout_or_modified_manifest_fails(self):
        self.change()
        with self.assertRaisesRegex(ValueError, 'Checkout'):
            publisher.prepare(self.root, None, self.base)
        (self.root / 'manifest.json').write_text('[]')
        with self.assertRaisesRegex(ValueError, 'manifest'):
            self.plan()

    def test_missing_later_upload_blocks_all_s3_writes_without_packages(self):
        self.change(); self.change('introduction'); plan = self.plan()
        (self.root / self.entry['introduction']['path']).unlink()
        calls = []
        class Upload:
            def upload(inner, path, key):
                calls.append(key)
        with self.assertRaisesRegex(ValueError, 'missing'):
            publisher.apply(self.root, plan, Upload())
        self.assertEqual(calls, [])

    def test_upload_failure_stops_before_later_resources_and_manifest(self):
        self.change(); self.change('introduction'); calls = []
        baseline = self.plan()['baseline']
        class Upload:
            def read_manifest(inner):
                return baseline
            def upload(inner, path, key):
                calls.append(key)
                raise OSError('upload failed')
        with self.assertRaises(OSError):
            publisher.apply(self.root, self.ready(self.plan()), Upload())
        self.assertEqual(calls, ['a-case/A Case.png'])

    def s3_fixture(self):
        fake = self.root / 'bin'; fake.mkdir()
        aws = fake / 'aws'
        aws.write_text('#!' + sys.executable + '\n' + Path(__file__).with_name('fake_s3.py').read_text())
        aws.chmod(0o755)
        s3 = self.root / 's3'; s3.mkdir()
        env = {**os.environ, 'PATH': str(fake) + os.pathsep + os.environ['PATH'],
               'FAKE_S3_ROOT': str(s3), 'AWS_TARGET_FOLDER': 's3://bucket/cases',
               'AWS_DISTRIBUITION_ID': 'test-distribution'}
        return s3, env

    def test_s3_get_only_missing_key_returns_none(self):
        s3, env = self.s3_fixture()
        with patch.dict(os.environ, env):
            store = publisher.S3(env['AWS_TARGET_FOLDER'])
            self.assertIsNone(store.read_manifest())
            target = s3 / 'bucket/cases/manifest.json'
            target.parent.mkdir(parents=True); target.write_text('[]')
            self.assertEqual(store.read_manifest(), '[]')
            for code in ('AccessDenied', 'NoSuchBucket', '404', 'SlowDown'):
                with self.subTest(code=code), patch.dict(os.environ, {'FAKE_S3_GET_ERROR': code}):
                    with self.assertRaises((ValueError, subprocess.CalledProcessError)):
                        store.read_manifest()

    def test_cli_upload_metadata_matches_verified_content(self):
        self.change(); plan = self.ready(self.plan())
        s3, env = self.s3_fixture()
        baseline = s3 / 'bucket/cases/manifest.json'
        baseline.parent.mkdir(parents=True); baseline.write_text(plan['baseline'])
        plan_file = self.root / 'plan.json'; plan_file.write_text(json.dumps(plan))
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'publish.py'), '--apply-plan', str(plan_file)],
                                cwd=self.root, env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        target = s3 / 'bucket/cases'
        self.assertEqual((target / 'a-case/A Case.png').read_bytes(), b'modified')
        metadata = json.loads((s3 / 'metadata.json').read_text())
        for key in ['a-case/A Case.png', 'manifest.json']:
            self.assertEqual(metadata['bucket/cases/' + key]['sha256'],
                             hashlib.sha256((target / key).read_bytes()).hexdigest())
        calls = [json.loads(line) for line in (s3 / 'calls.jsonl').read_text().splitlines()]
        self.assertEqual(calls[-1][:3], ['cloudfront', 'wait', 'invalidation-completed'])
