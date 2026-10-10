"""Byte-preserving restoration and hostile archive fixtures, without network access."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from extract_science import unpack


def declaration(path, data, **fields):
    return dict(path=path, sizeBytes=len(data), checksum=hashlib.sha256(data).hexdigest(), **fields)


def valid_files():
    files = {
        'session.json': b'{ "version": 2, "session": {"id":"old-id", "path":"$DATA/uploads/id",'
                        b'"history":"$DATA/uploads/id in prose"}}\r\n',
        'records.json': b'{ "id": "old-id", "filename":"plot.svg", "mimeType":"image/svg+xml" }\n',
        'README.md': b'# Original metadata\r\n',
        'ro-crate-metadata.json': b'{ "@context": "https://w3id.org/ro/crate/1.2/context" }\n',
    }
    inventory = [declaration(name, data) for name, data in files.items()]
    return files, inventory


def archive_bytes(files, inventory, extra=(), features=()):
    files = dict(files)
    files['manifest.json'] = json.dumps(dict(format='open-science-session', schemaVersion=1,
                                            inventory=inventory, requiredFeatures=list(features)),
                                        indent=2).encode() + b'\r\n'
    result = io.BytesIO()
    with tarfile.open(fileobj=result, mode='w:gz') as archive:
        for name, data in files.items():
            member = tarfile.TarInfo(name); member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
        for member, data in extra:
            archive.addfile(member, io.BytesIO(data))
    return result.getvalue()


class UnpackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / 'fixture.science'
        self.output = self.root / 'extracted'
        self.output.mkdir()
        self.files, self.inventory = valid_files()

    def restore(self, **kwargs):
        self.package.write_bytes(archive_bytes(self.files, self.inventory, **kwargs))
        unpack(self.package, self.output)

    def add_object(self, path='objects/not-derived-from-key', key='uploads/id', data=b'<svg/>'):
        self.files[path] = data
        self.inventory.append(declaration(path, data, storageKey=key))

    def test_restores_storage_keys_hidden_files_and_preserves_all_metadata_bytes(self):
        self.add_object(key='artifacts/p/s/.provenance/v/content')
        notebook = b'{ "id":"old", "path":"$DATA/uploads/id" }\r\n'
        self.add_object('objects/notebook', 'notebooks/p/s/document', notebook)
        self.restore()
        self.assertEqual((self.output / 'artifacts/p/s/.provenance/v/content').read_bytes(), b'<svg/>')
        self.assertEqual((self.output / 'notebooks/p/s/document').read_bytes(), notebook)
        with tarfile.open(self.package) as archive:
            for name in (*valid_files()[0], 'manifest.json'):
                self.assertEqual((self.output / name).read_bytes(), archive.extractfile(name).read())
        self.assertFalse((self.output / 'objects').exists())
        self.assertFalse((self.output / 'data').exists())

    def test_content_dedupe_restores_each_key_from_one_archive_object(self):
        self.add_object()
        self.inventory.append({**self.inventory[-1], 'storageKey': 'artifacts/p/.hidden/content'})
        self.restore(features=['content-dedupe'])
        self.assertEqual((self.output / 'uploads/id').read_bytes(), b'<svg/>')
        self.assertEqual((self.output / 'artifacts/p/.hidden/content').read_bytes(), b'<svg/>')

    def test_duplicate_inventory_requires_content_dedupe_and_distinct_keys(self):
        self.add_object()
        self.inventory.append({**self.inventory[-1], 'storageKey': 'uploads/other'})
        with self.assertRaises(ValueError):
            self.restore()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_unsafe_storage_paths_rejected_before_any_output(self):
        for key in ['../escape', '/absolute', 'C:/drive', 'C:drive', 'a\\b', 'a//b', 'a/./b',
                    'a/../b', 'a\x00b', 'a\nb', 'a:b', 'a/CON.txt', 'a/NUL', 'a/trailing.',
                    'a/trailing ', 'objects/copy', 'manifest.json', 'session.json/nested']:
            with self.subTest(key=key):
                self.files, self.inventory = valid_files()
                self.add_object(key=key)
                with self.assertRaises(ValueError):
                    self.restore()
                self.assertEqual(list(self.output.iterdir()), [])

    def test_portable_output_collisions_and_file_directory_conflicts_preflighted(self):
        for left, right in [('uploads/A', 'uploads/a'), ('uploads/é', 'uploads/e\u0301'),
                            ('uploads/file', 'uploads/file/child'), ('Uploads/a', 'uploads/b'),
                            ('uploads/a', 'uploads/a'), ('README.md', 'uploads/b')]:
            with self.subTest(left=left, right=right):
                self.files, self.inventory = valid_files()
                self.add_object('objects/a', left)
                self.add_object('objects/b', right)
                with self.assertRaises(ValueError):
                    self.restore()
                self.assertEqual(list(self.output.iterdir()), [])

    def test_archive_paths_links_specials_duplicates_and_collisions_preflighted(self):
        bad_members = []
        for name in ['../escape', '/absolute', 'C:/drive', 'objects//x', 'records.json',
                     'RECORDS.json', 'records.json/child', 'obj/A', 'obj/a/child']:
            bad_members.append((tarfile.TarInfo(name), b''))
        for kind in [tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE, tarfile.CHRTYPE, tarfile.BLKTYPE]:
            item = tarfile.TarInfo('objects/special'); item.type = kind; item.linkname = 'session.json'
            bad_members.append((item, b''))
        for member in bad_members:
            with self.subTest(name=member[0].name, kind=member[0].type):
                with self.assertRaises(ValueError):
                    self.restore(extra=[member])
                self.assertEqual(list(self.output.iterdir()), [])

    def test_archive_member_collisions_are_rejected_even_when_all_files_are_declared(self):
        for left, right in [('meta/A', 'meta/a'), ('meta/é', 'meta/e\u0301'),
                            ('meta/file', 'meta/file/child'), ('Meta/a', 'meta/b')]:
            with self.subTest(left=left, right=right):
                self.files, self.inventory = valid_files()
                for path in (left, right):
                    self.files[path] = b'metadata'
                    self.inventory.append(declaration(path, b'metadata'))
                with self.assertRaises(ValueError):
                    self.restore()
                self.assertEqual(list(self.output.iterdir()), [])

    def test_dedupe_conflicting_declarations_or_duplicate_keys_are_rejected(self):
        for change in ({'checksum': '0' * 64}, {'sizeBytes': 1}, {'storageKey': 'uploads/id'}):
            with self.subTest(change=change):
                self.files, self.inventory = valid_files()
                self.add_object()
                self.inventory.append({**self.inventory[-1], 'storageKey': 'uploads/other', **change})
                with self.assertRaises(ValueError):
                    self.restore(features=['content-dedupe'])
                self.assertEqual(list(self.output.iterdir()), [])

    def test_pax_sparse_file_without_extents_is_rejected(self):
        # PAX represents a hole-only sparse file with an empty, not absent, extent list.
        member = tarfile.TarInfo('objects/hole')
        member.pax_headers = {'GNU.sparse.size': '1024'}
        self.inventory.append(declaration('objects/hole', bytes(1024), storageKey='uploads/hole'))
        with self.assertRaises(ValueError):
            self.restore(extra=[(member, b'')])
        self.assertEqual(list(self.output.iterdir()), [])

    def test_inventory_size_and_checksum_must_match_each_restored_file(self):
        self.add_object()
        for field, value in [('sizeBytes', 0), ('sizeBytes', True), ('checksum', '0' * 64),
                             ('checksum', 'invalid')]:
            with self.subTest(field=field, value=value):
                original = self.inventory[-1][field]
                self.inventory[-1][field] = value
                with self.assertRaises(ValueError):
                    self.restore()
                self.inventory[-1][field] = original

    def test_metadata_corruption_and_undeclared_payload_are_rejected(self):
        self.files['records.json'] = self.files['records.json'].replace(b'old-id', b'new-id')
        with self.assertRaises(ValueError):
            self.restore()
        self.files, self.inventory = valid_files()
        self.files['credentials.env'] = b'should never be restored'
        with self.assertRaises(ValueError):
            self.restore()

    def test_hidden_tar_members_after_end_marker_are_rejected(self):
        data = archive_bytes(self.files, self.inventory)
        trailing = io.BytesIO()
        with tarfile.open(fileobj=trailing, mode='w') as archive:
            archive.addfile(tarfile.TarInfo('../escape'))
        self.package.write_bytes(gzip.compress(gzip.decompress(data) + trailing.getvalue()))
        with self.assertRaises(ValueError):
            unpack(self.package, self.output)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_corrupt_gzip_trailer_and_truncation_are_rejected(self):
        data = archive_bytes(self.files, self.inventory)
        for broken in [data[:-8], data[:-8] + bytes([data[-8] ^ 1]) + data[-7:]]:
            with self.subTest(length=len(broken)):
                self.package.write_bytes(broken)
                with self.assertRaises((OSError, EOFError, ValueError, tarfile.TarError)):
                    unpack(self.package, self.output)
                self.assertEqual(list(self.output.iterdir()), [])

    def test_nonempty_output_and_symlink_output_are_not_touched(self):
        marker = self.output / 'keep'; marker.write_bytes(b'keep')
        with self.assertRaises(ValueError):
            self.restore()
        self.assertEqual(marker.read_bytes(), b'keep')
        alias = self.root / 'alias'; alias.symlink_to(self.output, target_is_directory=True)
        with self.assertRaises(ValueError):
            unpack(self.package, alias)
        self.assertEqual(marker.read_bytes(), b'keep')
