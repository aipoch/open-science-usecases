import copy
import sys
from pathlib import Path
from unittest.mock import patch
from test_publish import GitFixture
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import check_structure as checker


class DeclarationTests(GitFixture):
    def check(self, before=None):
        return checker.check_declarations(self.root, before or self.base, self.git('rev-parse', 'HEAD'))

    def test_same_size_change_requires_changed_declaration(self):
        # A changed entry is being published, so its file edits still need declarations.
        self.entry['introduction']['sha256'] = '3' * 64
        self.change(declaration='1')
        self.assertTrue(any('synchronize' in error for error in self.check()))
        self.change(declaration='2')
        self.assertEqual(self.check(), [])

    def test_file_only_change_is_ignored(self):
        (self.root / self.entry['cover']['path']).write_bytes(b'modified'); self.commit()
        self.assertEqual(self.check(), [])

    def test_file_changes_in_unchanged_entries_are_ignored(self):
        other = self.add_case('B Case', 'b-case')
        self.write_manifest(); self.base = self.commit()
        (self.root / other['cover']['path']).write_bytes(b'modified')
        self.change('cover')
        self.assertEqual(self.check(), [])

    def test_restored_file_can_be_published_after_file_only_deletion(self):
        # File-only batches can advance the baseline without changing published objects.
        path = self.root / self.entry['cover']['path']
        previous = self.base
        path.unlink(); self.base = self.commit()
        self.assertEqual(self.check(before=previous), [])
        self.change('cover')
        self.assertEqual(self.check(), [])

    def test_missing_and_malformed_declarations_on_related_resources(self):
        for declaration in (None, '', 'x' * 64, 'a' * 63, 123, {}, 'a' * 65):
            with self.subTest(declaration=declaration):
                self.entry['cover']['sha256'] = declaration
                self.write_manifest(); self.commit()
                self.assertTrue(any('64' in error for error in self.check()))
        del self.entry['cover']['sha256']; self.write_manifest(); self.commit()
        self.assertTrue(any('64' in error for error in self.check()))

    def test_new_local_resource_needs_sha(self):
        self.entry = self.add_case('B Case', 'b-case')
        del self.entry['cover']['sha256']; self.write_manifest(); self.commit()
        self.assertTrue(any('64' in error for error in self.check()))

    def test_new_local_source_and_rename_not_treated_as_same_path_edit(self):
        self.entry['case']['release_url'] = 'https://example.com/a.science'
        self.write_manifest(); remote = self.commit()
        self.entry['case']['release_url'] = ''; self.write_manifest(); self.commit()
        self.assertEqual(self.check(before=remote), [])
        old = self.git('rev-parse', 'HEAD')
        self.git('mv', 'A Case', 'Renamed')
        self.entry['name'] = 'renamed'
        for resource in (self.entry[kind] for kind in ('cover', 'case', 'introduction')):
            resource['path'] = resource['path'].replace('A Case/', 'Renamed/')
        self.write_manifest(); self.commit()
        self.assertEqual(self.check(before=old), [])  # Naming is the existing structure stage's job.

    def test_unchanged_legacy_resources_do_not_need_hash_migration(self):
        del self.entry['case']['sha256']; self.write_manifest(); legacy = self.commit()
        self.change('cover')
        (self.root / self.entry['case']['path']).unlink()
        self.assertEqual(self.check(before=legacy), [])

    def test_declarations_are_not_verified_against_resource_bytes(self):
        self.change(declaration='A')
        for kind in ('cover', 'case', 'introduction'):
            (self.root / self.entry[kind]['path']).unlink()
        self.assertEqual(self.check(), [])

    def test_case_only_sha_spelling_change_does_not_declare_new_content(self):
        self.entry['cover']['sha256'] = 'a' * 64; self.write_manifest(); old = self.commit()
        self.change(declaration='A')
        self.assertTrue(any('synchronize' in error for error in self.check(before=old)))

    def test_type_change_to_symlink_is_ignored_with_unchanged_manifest(self):
        path = self.root / self.entry['cover']['path']
        path.unlink(); path.symlink_to('../manifest.json'); self.commit()
        self.assertEqual(self.check(), [])
        self.entry['cover']['sha256'] = '2' * 64
        self.write_manifest(); self.commit()
        self.assertTrue(any('regular file' in error for error in self.check()))

    def test_unchanged_legacy_case_without_introduction_is_not_revalidated(self):
        del self.entry['introduction']; self.write_manifest(); legacy = self.commit()
        (self.root / 'tool.py').write_text('# tooling only'); self.commit()
        self.assertEqual(self.check(before=legacy), [])
