"""Exercise the versioned static site through the real publisher and Git checks."""
import hashlib
import json
from unittest.mock import patch

from test_publish import GitFixture, publisher
import check_structure
from test_parallel_publication import MemoryS3


class ExperienceTests(GitFixture):
    def setUp(self):
        super().setUp()
        self.directory = self.root / 'usecases/A Case/experience'
        self.directory.mkdir()
        (self.directory / 'index.html').write_text('<video src="intro.mp4"></video>')
        (self.directory / 'nested').mkdir()
        (self.directory / 'nested/model.bin').write_bytes(b'model')

    def declare(self):
        self.git('add', '--', str(self.directory))
        path = self.directory.relative_to(self.root).as_posix()
        revision = self.git('rev-parse', self.git('write-tree') + ':' + path)
        self.entry['experience'] = {'path': path, 'revision': revision}
        self.write_manifest()
        return self.commit()

    def test_publish_local_and_remote_dependencies_then_replace_one_scene(self):
        film = b'film'
        source = {'release_url': 'https://github.com/aipoch/open-science-usecases/releases/download/test/film.mp4',
                  'bytes': len(film), 'sha256': hashlib.sha256(film).hexdigest()}
        (self.directory / '.experience-sources.json').write_text(json.dumps({'intro.mp4': source}))
        after = self.declare()
        self.assertEqual(check_structure.check_declarations(self.root, self.base, after), [])
        plan = self.plan()
        store = MemoryS3(plan['baseline'])
        prefix = 'a-case/experience/' + self.entry['experience']['revision'] + '/'
        with patch('extract_science.download', side_effect=lambda url, path, item: path.write_bytes(film)):
            publisher.apply(self.root, plan, store, self.root / 'publication', prepare_cases=True)
        self.assertEqual(set(store.objects), {prefix + n for n in ('intro.mp4', 'nested/model.bin', 'index.html')})
        self.assertEqual(store.objects[prefix + 'intro.mp4'], film)
        self.assertEqual(publisher.prepare(self.root, store.baseline, after)['candidates'], [])
        (self.directory / 'nested/model.bin').write_bytes(b'changed')
        stale = self.commit()
        with self.assertRaisesRegex(ValueError, 'revision'):
            check_structure.check_declarations(self.root, after, stale)
        new = self.declare()
        changed = publisher.prepare(self.root, store.baseline, new)
        self.assertFalse(changed['packages'])
        self.assertTrue(all(not item['key'].startswith(prefix) for item in changed['candidates']))

    def test_reject_invalid_sources_before_upload(self):
        sources = self.directory / '.experience-sources.json'
        base = {'release_url': 'https://github.com/aipoch/open-science-usecases/releases/download/test/file',
                'bytes': 1, 'sha256': 'a' * 64}
        for target, changes in [('nested/model.bin', {}), ('../escape', {}), ('clip.mp4', {'release_url': 'https://example.org/file'})]:
            with self.subTest(target=target):
                sources.write_text(json.dumps({target: {**base, **changes}}))
                self.declare()
                with self.assertRaises(ValueError):
                    self.plan()
        sources.unlink()
        (self.directory / 'index.html').unlink()
        self.declare()
        with self.assertRaisesRegex(ValueError, 'index.html'):
            self.plan()
        (self.directory / 'index.html').symlink_to('nested/model.bin')
        self.declare()
        with self.assertRaisesRegex(ValueError, 'invalid experience file'):
            self.plan()
