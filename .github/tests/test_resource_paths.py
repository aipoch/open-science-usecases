"""Resource paths locate sources independently of catalog classification directories."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys

from test_publish import GitFixture, SCRIPTS, publisher
from test_resource_sources import Store
from test_extract_science import package_bytes
import check_structure as checker
import extract_science


class ResourcePathTests(GitFixture):
    def relocate(self, directories):
        for kind, directory in zip(publisher.KINDS, directories):
            resource = self.entry[kind]
            source = self.root / resource['path']
            target = self.root / directory / resource['file_name']
            target.parent.mkdir(parents=True, exist_ok=True)
            source.rename(target)
            resource['path'] = target.relative_to(self.root).as_posix()
        self.write_manifest()
        return self.commit()

    def check_manifest_cli(self, expected=0):
        selected = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'check_structure.py'),
                                   'directories', '--base', self.base], cwd=self.root,
                                  capture_output=True, text=True, check=True)
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'check_structure.py'), 'manifest'],
                                cwd=self.root, env={**os.environ, 'CASES_JSON': selected.stdout},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stderr)

    def test_category_paths_pass_check_and_path_only_publication_keeps_objects(self):
        self.relocate(('catalog/science/physics/covers', 'packages/physics', 'docs/zh/physics'))
        self.check_manifest_cli()
        self.assertEqual(checker.check_declarations(self.root, self.base, self.git('rev-parse', 'HEAD')), [])
        plan = self.plan()
        self.assertEqual(plan['candidates'], [])
        self.assertEqual(plan['packages'], [])
        store = Store(plan['baseline']); store.objects = {'a-case/A Case.png': b'keep'}
        with contextlib.redirect_stdout(io.StringIO()):
            publisher.apply(self.root, plan, store)
        self.assertEqual(store.objects, {'a-case/A Case.png': b'keep'})
        self.assertEqual(set(store.writes), {'manifest.json'})
        self.assertEqual(store.heads, [])

    def test_root_and_old_layout_resources_are_valid_current_and_baseline_paths(self):
        self.relocate(('', 'Old', 'category/subcategory'))
        self.check_manifest_cli()
        for legacy in (False, True):
            self.assertEqual(publisher.read_manifest(json.dumps(self.entries), 'fixture', legacy=legacy), self.entries)
        self.assertEqual(checker.source_errors(self.root, self.entry), [])

    def test_remote_cover_does_not_require_its_directory_when_other_resources_are_local(self):
        self.relocate(('absent/covers', 'packages', 'docs'))
        (self.root / self.entry['cover']['path']).unlink()
        (self.root / 'absent/covers').rmdir(); (self.root / 'absent').rmdir()
        self.entry['cover']['release_url'] = 'https://example.invalid/cover.png'
        self.write_manifest(); self.commit()
        self.assertEqual(checker.schema_errors(self.entry), [])
        self.assertEqual(checker.source_errors(self.root, self.entry), [])
        self.assertTrue(self.plan()['candidates'][0]['force_upload'])

    def test_all_remote_classified_paths_need_no_local_directories(self):
        entry = copy.deepcopy(self.entry)
        for kind in publisher.KINDS:
            entry[kind].update(path='remote/catalog/'+kind+'/'+entry[kind]['file_name'],
                               release_url='https://example.invalid/'+kind+Path(entry[kind]['file_name']).suffix)
        self.assertEqual(checker.schema_errors(entry), [])
        self.assertEqual(checker.source_errors(self.root, entry), [])

    def test_nested_parent_symlink_rejected_for_each_local_resource(self):
        self.relocate(('catalog/covers/deep', 'catalog/packages/deep', 'catalog/docs/deep'))
        for directory in ('covers', 'packages', 'docs'):
            with self.subTest(directory=directory):
                parent = self.root / 'catalog' / directory
                saved = self.root / (directory+'-saved')
                parent.rename(saved)
                parent.symlink_to(saved, target_is_directory=True)
                self.assertTrue(checker.source_errors(self.root, self.entry))
                parent.unlink(); saved.rename(parent)

    def test_arbitrary_paths_still_reject_absolute_traversal_and_drive_names(self):
        for path in ('/A Case.png', '../A Case.png', 'catalog/../A Case.png',
                     'catalog//A Case.png', './A Case.png', 'C:/A Case.png', 'C:A Case.png',
                     'catalog\\A Case.png', 'catalog/\nA Case.png'):
            entry = copy.deepcopy(self.entry)
            entry['cover'].update(path=path, file_name=path.split('/')[-1])
            with self.subTest(path=path):
                self.assertTrue(checker.schema_errors(entry))

    def test_classified_resources_prepare_and_extract_using_each_declared_path(self):
        package = package_bytes()
        path = self.root / self.entry['case']['path']; path.write_bytes(package)
        size, checksum = publisher.file_integrity(path)
        self.entry['case'].update(bytes=size, sha256=checksum)
        after = self.relocate(('covers/physics', 'catalog/science/physics/session', 'introductions/zh'))
        plan = publisher.prepare(self.root, None, after)
        store = Store(None); store.clears = []; store.clear_extracted = store.clears.append
        with contextlib.redirect_stdout(io.StringIO()):
            plan = publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
            plan = extract_science.expand_plan(self.root, plan, self.root / 'staging')
            publisher.apply(self.root, plan, store)
        for kind in publisher.KINDS:
            self.assertIn('a-case/'+self.entry[kind]['file_name'], store.writes)
        self.assertEqual(store.clears, ['a-case'])
        self.assertEqual(store.manifest, (self.root / 'manifest.json').read_text())

    def test_git_treats_special_resource_names_as_literal_paths(self):
        for filename in (':cover.png', 'cover[1]*?.png'):
            with self.subTest(filename=filename):
                resource = self.entry['cover']
                (self.root / resource['path']).rename(self.root / filename)
                resource.update(path=filename, file_name=filename)
                self.write_manifest(); after = self.commit()
                self.assertEqual(checker.check_declarations(self.root, self.base, after), [])
                plan = self.plan(); store = Store(plan['baseline'])
                plan = publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
                with contextlib.redirect_stdout(io.StringIO()):
                    publisher.apply(self.root, plan, store)
                self.assertIn('a-case/'+filename, store.writes)

    def test_each_resource_path_only_move_updates_index_without_object_operations(self):
        for kind in publisher.KINDS:
            with self.subTest(kind=kind), contextlib.redirect_stdout(io.StringIO()):
                before = self.git('rev-parse', 'HEAD')
                resource = self.entry[kind]
                target = self.root / '分类 /物理[1]/:素材' / resource['file_name']
                target.parent.mkdir(parents=True, exist_ok=True)
                (self.root / resource['path']).rename(target)
                resource['path'] = target.relative_to(self.root).as_posix()
                self.write_manifest(); after = self.commit()
                self.check_manifest_cli()
                self.assertEqual(checker.check_declarations(self.root, before, after), [])
                plan = self.plan(before=before)
                self.assertEqual(plan['candidates'], [])
                self.assertEqual(plan['packages'], [])
                store = Store(plan['baseline'])
                store.objects = {'a-case/' + r['file_name']: b'original'
                                 for r in (self.entry[k] for k in publisher.KINDS)}
                original = copy.deepcopy(store.objects)
                store.clear_extracted = lambda name: self.fail('path-only move deleted objects')
                publisher.apply(self.root, plan, store)
                self.assertEqual(store.objects, original)
                self.assertEqual(store.heads, [])
                self.assertEqual(set(store.writes), {'manifest.json'})
                self.assertEqual(json.loads(store.manifest), self.entries)

    def test_missing_declared_path_never_falls_back_to_old_directory(self):
        for kind in publisher.KINDS:
            resource = self.entry[kind]
            old_path = resource['path']
            for missing_parent in (True, False):
                with self.subTest(kind=kind, missing_parent=missing_parent):
                    parent = self.root / ('absent' if missing_parent else 'empty') / kind
                    if not missing_parent:
                        parent.mkdir(parents=True, exist_ok=True)
                    resource['path'] = (parent / resource['file_name']).relative_to(self.root).as_posix()
                    self.write_manifest(); self.commit()
                    self.check_manifest_cli(expected=1)
                    with self.assertRaisesRegex(ValueError, 'Missing|missing'):
                        self.plan()
                    self.assertTrue((self.root / old_path).is_file())
            resource['path'] = old_path

    def test_moved_content_with_stale_sha_fails_git_declaration_check_for_each_kind(self):
        for kind in publisher.KINDS:
            with self.subTest(kind=kind):
                before = self.git('rev-parse', 'HEAD')
                resource = self.entry[kind]
                target = self.root / '分类[1]' / resource['file_name']
                target.parent.mkdir(exist_ok=True)
                (self.root / resource['path']).rename(target)
                target.write_bytes(b'modified')
                resource['path'] = target.relative_to(self.root).as_posix()
                self.write_manifest(); after = self.commit()
                errors = checker.check_declarations(self.root, before, after)
                self.assertEqual(len(errors), 1)
                self.assertIn('synchronize', errors[0])

    def test_literal_old_path_detects_stale_sha_after_second_move(self):
        resource = self.entry['cover']
        first = self.root / ':cover[1]*?.png'
        (self.root / resource['path']).rename(first)
        resource.update(path=first.name, file_name=first.name)
        self.write_manifest(); before = self.commit()
        target = self.root / '新分类' / first.name
        target.parent.mkdir(); first.rename(target)
        target.write_bytes(b'modified')
        resource['path'] = target.relative_to(self.root).as_posix()
        self.write_manifest(); after = self.commit()
        self.assertTrue(checker.check_declarations(self.root, before, after))

    def test_each_ancestor_and_leaf_symlink_is_rejected_by_check_and_preparation(self):
        self.relocate(('covers/a/b', 'packages/a/b', 'docs/a/b'))
        for kind in publisher.KINDS:
            resource = self.entry[kind]
            parts = resource['path'].split('/')
            for depth in range(1, len(parts) + 1):
                for dangling in (False, True):
                    with self.subTest(kind=kind, depth=depth, dangling=dangling):
                        path = self.root.joinpath(*parts[:depth])
                        saved = self.root / 'saved-source'
                        path.rename(saved)
                        try:
                            path.symlink_to(self.root / 'nonexistent' if dangling else saved,
                                            target_is_directory=saved.is_dir())
                            self.check_manifest_cli(expected=1)
                            with self.assertRaisesRegex(ValueError, 'symlink|regular file'):
                                self.plan()
                        finally:
                            path.unlink(); saved.rename(path)

    def test_source_parent_replaced_after_plan_fails_before_download_or_write(self):
        self.relocate(('covers/a/b', 'packages/a/b', 'docs/a/b'))
        plan = publisher.prepare(self.root, None, self.git('rev-parse', 'HEAD'))
        store = Store(None)
        directory = self.root / 'packages/a'
        saved = self.root / 'saved-source'; directory.rename(saved)
        directory.symlink_to(saved, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
        self.assertEqual(store.heads, [])
        self.assertEqual(store.writes, [])

    def test_local_git_integrity_uses_literal_path_even_with_matching_glob_decoy(self):
        resource = self.entry['cover']
        original = self.root / resource['path']
        filename = 'cover[1]*?.png'
        target = self.root / filename
        original.rename(target)
        resource.update(path=filename, file_name=filename)
        (self.root / 'cover1decoy.png').write_bytes(b'original')
        self.write_manifest(); self.commit()
        plan = self.plan(); store = Store(plan['baseline'])
        target.write_bytes(b'modified')
        with self.assertRaises((ValueError, subprocess.CalledProcessError)):
            publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
        self.assertEqual(store.writes, [])

    def test_root_and_special_parent_paths_publish_all_resources_and_extract(self):
        layouts = (
            ('', '', ''),
            (':(glob)/封面[1]*?', '--packages/层级', "notes/it's a category"),
        )
        for layout in layouts:
            with self.subTest(layout=layout), contextlib.redirect_stdout(io.StringIO()):
                package = package_bytes()
                source = self.root / self.entry['case']['path']
                source.write_bytes(package)
                self.entry['case'].update(bytes=len(package), sha256=publisher.file_integrity(source)[1])
                after = self.relocate(layout)
                plan = publisher.prepare(self.root, None, after)
                self.check_manifest_cli()
                store = Store(None); store.clears = []
                store.clear_extracted = store.clears.append
                plan = publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
                plan = extract_science.expand_plan(self.root, plan, self.root / 'staging')
                publisher.apply(self.root, plan, store)
                self.assertEqual(store.clears, ['a-case'])
                self.assertIn('a-case/extracted/session.json', store.writes)
                for kind in publisher.KINDS:
                    self.assertIn('a-case/' + self.entry[kind]['file_name'], store.writes)
                self.assertEqual(json.loads(store.manifest), self.entries)

    def test_modified_glob_decoy_does_not_block_literal_resource_preparation(self):
        resource = self.entry['cover']
        filename = 'cover[1]*?.png'
        (self.root / resource['path']).rename(self.root / filename)
        resource.update(path=filename, file_name=filename)
        decoy = self.root / 'cover1decoy.png'
        decoy.write_bytes(b'original')
        self.write_manifest(); self.commit()
        plan = self.plan(); store = Store(plan['baseline'])
        decoy.write_bytes(b'modified')
        staged = publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
        resource_file = next(f for f in staged['files'] if f['key'] == 'a-case/' + filename)
        self.assertEqual(Path(resource_file['path']).read_bytes(), b'original')
        with contextlib.redirect_stdout(io.StringIO()):
            publisher.apply(self.root, staged, store)
        self.assertEqual(set(store.writes), {'a-case/' + filename, 'manifest.json'})
