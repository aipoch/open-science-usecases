"""Classification errors stop checking/publication before resource operations."""
import contextlib
import copy
import io
import json
import os
import subprocess
import sys

from test_publish import GitFixture, SCRIPTS, publisher
from test_resource_sources import Store
from test_extract_science import package_bytes
import extract_science
from publication_steps import build_steps
import check_structure as checker


class CatalogTests(GitFixture):
    def classified(self, catalog='Data Science', slug='data-science'):
        entry = copy.deepcopy(self.entry)
        entry.update(catalog=catalog, catalog_name=slug)
        for kind in publisher.KINDS:
            entry[kind]['path'] = catalog + '/assets/' + entry[kind]['file_name']
        return entry

    def test_converted_catalogs_allow_spaces_camel_case_and_punctuation(self):
        for catalog, slug in [('Data Science', 'data-science'), ('DataScience', 'data-science'),
                              ('AI_Research 2', 'ai-research-2'), ('C++', 'c')]:
            with self.subTest(catalog=catalog):
                self.assertEqual(checker.schema_errors(self.classified(catalog, slug)), [])

    def test_empty_pair_is_unclassified_and_preserves_arbitrary_resource_paths(self):
        self.assertEqual(checker.schema_errors(self.entry), [])
        self.assertEqual(publisher.read_manifest(json.dumps(self.entries), 'fixture', legacy=False),
                         self.entries)
        for catalog, slug in [('', 'data-science'), ('Data Science', '')]:
            entry = self.classified(catalog, slug)
            self.assertTrue(checker.schema_errors(entry))

    def test_missing_catalog_fields_are_rejected_for_targets_but_allowed_in_baselines(self):
        entry = copy.deepcopy(self.entry)
        entry.pop('catalog', None); entry.pop('catalog_name', None)
        self.assertEqual(checker.schema_errors(entry, legacy=True), [])
        for field in ('catalog', 'catalog_name'):
            errors = checker.schema_errors(entry)
            self.assertTrue(any(field in error for error in errors), errors)

    def test_all_remote_classification_does_not_require_local_directories(self):
        entry = self.classified()
        for kind in publisher.KINDS:
            entry[kind]['release_url'] = 'https://example.invalid/' + entry[kind]['file_name'].replace(' ', '-')
        self.assertEqual(checker.schema_errors(entry), [])
        self.assertEqual(checker.source_errors(self.root, entry), [])
        self.entries = [entry]; self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, None, after)
        self.assertEqual(len(plan['candidates']), 3)
        self.assertEqual(plan['packages'], [{'name': 'a-case', 'resource': entry['case']}])

    def test_unconvertible_or_unsafe_catalogs_are_not_silently_truncated(self):
        for catalog, slug in [('数据科学', 'data-science'), ('AI 研究', 'ai'), ('Café', 'cafe'),
                              ('AI🧪', 'ai'), ('---', ''), (' ', ''),
                              ('../Data', 'data'), ('A/B', 'a-b'), ('A\\B', 'a-b'),
                              ('A\nB', 'a-b'), ('C:', 'c')]:
            with self.subTest(catalog=catalog):
                self.assertTrue(checker.schema_errors(self.classified(catalog, slug)))
        for field in ('catalog', 'catalog_name'):
            for value in (None, 1, [], {}):
                entry = self.classified(); entry[field] = value
                with self.subTest(field=field, value=value):
                    self.assertTrue(checker.schema_errors(entry))

    def test_slug_must_match_conversion_and_paths_must_use_display_catalog(self):
        entry = self.classified(slug='something-else')
        self.assertTrue(checker.schema_errors(entry))
        for kind in publisher.KINDS:
            for prefix in ('data-science', 'Other', 'Data Science Extra'):
                entry = self.classified()
                entry[kind]['path'] = prefix + '/' + entry[kind]['file_name']
                with self.subTest(kind=kind, prefix=prefix):
                    self.assertTrue(checker.schema_errors(entry))

    def test_reused_catalog_is_valid_but_different_catalogs_cannot_share_slug(self):
        first = self.classified()
        second = self.classified(); second['name'] = 'another-case'
        self.assertEqual(publisher.read_manifest(json.dumps([first, second]), 'fixture', legacy=False),
                         [first, second])
        second = self.classified('Data_Science'); second['name'] = 'another-case'
        with self.assertRaisesRegex(ValueError, 'Data Science.*Data_Science|Data_Science.*Data Science'):
            publisher.read_manifest(json.dumps([first, second]), 'fixture', legacy=False)

    def test_legacy_mode_does_not_ignore_partial_or_invalid_classification(self):
        entry = self.classified(); del entry['catalog_name']
        self.assertTrue(checker.schema_errors(entry, legacy=True))
        entry = self.classified(slug='wrong')
        self.assertTrue(checker.schema_errors(entry, legacy=True))

    def test_collision_is_checked_even_when_no_entries_are_selected(self):
        first = self.classified()
        second = self.classified('Data_Science'); second['name'] = 'another-case'
        self.entries = [first, second]; self.write_manifest(); after = self.commit()
        for stage, arguments, environment in [('directories', ['--base', after], os.environ),
                                               ('manifest', [], {**os.environ, 'CASES_JSON': '[]'})]:
            result = subprocess.run([sys.executable, '-B', str(SCRIPTS/'check_structure.py'),
                                     stage, *arguments], cwd=self.root, env=environment,
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stderr)
            self.assertIn('collision', result.stderr)

    def test_collision_with_unchanged_entry_fails_directory_stage(self):
        first = self.classified()
        self.entries = [first]; self.write_manifest(); self.base = self.commit()
        second = self.classified('Data_Science'); second['name'] = 'another-case'
        self.entries.append(second); self.write_manifest(); self.commit()
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS/'check_structure.py'),
                                 'directories', '--base', self.base], cwd=self.root,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('data-science', result.stderr)
        self.assertIn('Data Science', result.stderr)
        self.assertIn('Data_Science', result.stderr)

    def test_classification_migration_from_legacy_baseline_only_updates_manifest(self):
        old = copy.deepcopy(self.entries)
        for entry in old:
            entry.pop('catalog', None); entry.pop('catalog_name', None)
        entry = self.classified()
        for kind in publisher.KINDS:
            source = self.root / self.entry[kind]['path']
            target = self.root / entry[kind]['path']
            target.parent.mkdir(parents=True, exist_ok=True); source.rename(target)
        self.entries = [entry]; self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, json.dumps(old), after)
        self.assertEqual(plan['candidates'], [])
        self.assertEqual(plan['packages'], [])
        self.assertEqual([s['operation'] for s in plan['steps']], ['UPDATE_CASE', 'FINAL_SYNC'])
        selected = subprocess.run([sys.executable, '-B', str(SCRIPTS/'check_structure.py'),
                                   'directories', '--base', self.base], cwd=self.root,
                                  capture_output=True, text=True, check=True)
        checked = subprocess.run([sys.executable, '-B', str(SCRIPTS/'check_structure.py'), 'manifest'],
                                 cwd=self.root, env={**os.environ, 'CASES_JSON': selected.stdout},
                                 capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(checker.check_declarations(self.root, self.base, after), [])
        store = Store(plan['baseline'])
        store.objects = {'a-case/A Case.png': b'original', 'a-case/extracted/keep': b'untouched'}
        original = copy.deepcopy(store.objects)
        with contextlib.redirect_stdout(io.StringIO()):
            publisher.apply(self.root, plan, store)
        self.assertEqual(store.objects, original)
        self.assertEqual(set(store.writes), {'manifest.json'})
        self.assertEqual(store.heads, [])
        self.assertEqual(store.manifest, (self.root/'manifest.json').read_text())

    def test_shared_catalog_rename_checkpoints_remain_valid_and_retry_after_cdn_failure(self):
        self.add_case('B Case', 'b-case')
        old = copy.deepcopy(self.entries)
        for previous, entry in zip(old, self.entries):
            previous.update(catalog='Data Science', catalog_name='data-science')
            entry.update(catalog='DataScience', catalog_name='data-science')
            for kind in publisher.KINDS:
                resource = entry[kind]
                previous[kind]['path'] = 'Data Science/assets/' + resource['file_name']
                target = self.root / 'DataScience' / resource['file_name']
                target.parent.mkdir(exist_ok=True)
                (self.root / resource['path']).rename(target)
                resource['path'] = target.relative_to(self.root).as_posix()
        self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, json.dumps(old), after)
        for step in plan['steps']:
            self.assertEqual(checker.catalog_errors(json.loads(step['manifest'])), [])
        store = Store(plan['baseline'])
        def fail_cdn(*args, **kwargs):
            raise RuntimeError('CDN failure')
        store.refresh_cdn = fail_cdn
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(RuntimeError, 'CDN failure'):
            publisher.apply(self.root, plan, store)
        retry = publisher.prepare(self.root, store.manifest, after)
        self.assertEqual(retry['candidates'], [])
        self.assertEqual(retry['packages'], [])
        store.refresh_cdn = lambda *args, **kwargs: None
        with contextlib.redirect_stdout(io.StringIO()):
            publisher.apply(self.root, retry, store)
        self.assertEqual(store.manifest, (self.root/'manifest.json').read_text())

    def test_catalog_replacement_does_not_publish_collision_before_removal(self):
        old = [self.classified()]
        new = [self.classified('DataScience')]; new[0]['name'] = 'replacement'
        steps = build_steps(old, new, json.dumps(new))
        for step in steps:
            self.assertEqual(checker.catalog_errors(json.loads(step['manifest'])), [])
        self.assertEqual(json.loads(steps[-1]['manifest']), new)

    def test_catalog_replacement_publishes_all_resources_before_group_checkpoint(self):
        old = [self.classified()]
        self.entries = []
        for title, name in [('B Case', 'b-case'), ('C Case', 'c-case')]:
            entry = self.add_case(title, name)
            entry.update(catalog='DataScience', catalog_name='data-science')
            for kind in publisher.KINDS:
                resource = entry[kind]
                target = self.root / 'DataScience' / name / resource['file_name']
                target.parent.mkdir(parents=True, exist_ok=True)
                (self.root/resource['path']).rename(target)
                resource['path'] = target.relative_to(self.root).as_posix()
                if kind == 'case':
                    target.write_bytes(package_bytes())
                    resource['bytes'], resource['sha256'] = publisher.file_integrity(target)
        self.write_manifest(); after = self.commit()
        plan = publisher.prepare(self.root, json.dumps(old), after)
        for step in plan['steps']:
            self.assertEqual(checker.catalog_errors(json.loads(step['manifest'])), [])
        store = Store(plan['baseline']); clears = []; refreshes = []
        store.clear_extracted = clears.append
        store.refresh_cdn = lambda case_name=None: refreshes.append(case_name)
        with contextlib.redirect_stdout(io.StringIO()):
            ready = publisher.prepare_resources(self.root, plan, store, self.root/'sources')
            ready = extract_science.expand_plan(self.root, ready, self.root/'staging')
            publisher.apply(self.root, ready, store)
        first_commit = store.writes.index('manifest.json')
        for entry in self.entries:
            for kind in publisher.KINDS:
                self.assertIn(entry['name']+'/'+entry[kind]['file_name'], store.writes[:first_commit])
            self.assertIn(entry['name']+'/extracted/session.json', store.writes[:first_commit])
        self.assertCountEqual(clears, ['b-case', 'c-case'])
        self.assertEqual(refreshes, ['b-case', 'c-case', None])
        self.assertEqual(store.manifest, (self.root/'manifest.json').read_text())
