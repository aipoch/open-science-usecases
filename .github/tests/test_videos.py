"""Video declarations and publication use isolated Git, HTTP and fake S3."""
import copy
import contextlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import socket
import threading
import unittest
from unittest.mock import MagicMock, patch

from test_publish import GitFixture, publisher
import check_structure as checker
import video_resources as videos
from test_resource_sources import Store


def internal_video():
    return {'type': 's3', 'file_path': 'a-case/demo.mp4', 'file_name': 'demo.mp4',
            'bytes': 3, 'sha256': 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'}


class VideoSchemaTests(GitFixture):
    def test_invalid_video_fields_and_paths_fail_without_network(self):
        for fields in ({'type': 'vimeo'}, {'file_path': 'another-case/demo.mp4'},
                       {'file_path': 'a-case/../demo.mp4'}, {'file_path': 'a-case/%2e%2e/demo.mp4'},
                       {'bytes': True}, {'bytes': 0}, {'sha256': 'a' * 63},
                       {'file_name': 'other.mp4'}, {'media_platform': 'none'}):
            with self.subTest(fields=fields):
                self.entry['video'] = {**internal_video(), **fields}
                self.assertTrue(checker.schema_errors(self.entry))

    def test_three_video_types_preserve_the_required_filename(self):
        for video in (internal_video(),
                      {'type': 'external', 'file_path': 'https://media.example/demo.mp4',
                       'file_name': 'demo.mp4', 'bytes': 3},
                      {'type': 'youtube', 'file_path': 'https://youtu.be/abcdefghijk',
                       'file_name': 'Case demonstration'}):
            with self.subTest(kind=video['type']):
                self.entry['video'] = video
                self.assertEqual(checker.schema_errors(self.entry), [])
                broken = copy.deepcopy(self.entry)
                del broken['video']['file_name']
                self.assertTrue(checker.schema_errors(broken))

    def test_video_only_change_preserves_existing_resource_plan(self):
        self.entry['video'] = internal_video()
        self.write_manifest(); self.commit()
        plan = self.plan()
        self.assertEqual(plan['candidates'], [])
        self.assertEqual(plan['packages'], [])
        self.assertEqual(self.keys(plan), ['manifest.json'])
        self.assertEqual(json.loads(plan['steps'][0]['manifest'])[0]['video'], internal_video())

    def test_global_schema_rejects_unchanged_invalid_video(self):
        self.entry['video'] = {**internal_video(), 'type': 'unknown'}
        self.write_manifest()
        with contextlib.chdir(self.root):
            self.assertTrue(checker.validate_manifest([]))

    def test_bad_neighbor_resource_reports_schema_errors_instead_of_crashing(self):
        self.entry['video'] = internal_video()
        self.entry['cover'] = None
        self.assertTrue(checker.schema_errors(self.entry))

    def test_youtube_hosts_and_single_video_ids_are_validated(self):
        for url in ('https://www.youtube.com/watch?v=abcdefghijk', 'https://youtu.be/abcdefghijk',
                    'https://www.youtube.com/shorts/abcdefghijk', 'https://www.youtube.com/live/abcdefghijk'):
            self.assertEqual(videos.youtube_id(url), 'abcdefghijk')
        for url in ('https://youtube.com.evil.test/watch?v=abcdefghijk',
                    'https://youtube.com/playlist?list=abcdefghijk', 'https://youtu.be/short',
                    'https://youtube.com/watch?v=abcdefghijk&v=otherother1'):
            self.assertIsNone(videos.youtube_id(url))


class VideoHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.server.requests.append((self.command, self.path))
        status, headers, body = self.server.response
        if self.path == '/redirect':
            status, headers = 302, {'Location': '/video'}
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()

    def do_GET(self):
        self.server.requests.append((self.command, self.path))
        status, headers, body = self.server.response
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class VideoProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), VideoHandler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.http.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown(); cls.http.server_close(); cls.thread.join()

    def setUp(self):
        self.http.requests = []
        self.http.response = (200, {'Content-Length': '3', 'Content-Type': 'video/mp4'}, b'abc')

    def test_external_redirect_preserves_head_without_get(self):
        with patch.object(videos, 'check_public_url'):
            videos.check_external(self.url + '/redirect', 3)
        self.assertEqual(self.http.requests, [('HEAD', '/redirect'), ('HEAD', '/video')])

    def test_external_rejects_wrong_size_html_and_missing_length(self):
        for headers in ({'Content-Length': '2', 'Content-Type': 'video/mp4'},
                        {'Content-Length': '3', 'Content-Type': 'text/html'},
                        {'Content-Type': 'video/mp4'}):
            with self.subTest(headers=headers), patch.object(videos, 'check_public_url'):
                self.http.response = (200, headers, b'')
                with self.assertRaises(ValueError):
                    videos.check_external(self.url + '/video', 3)

    def test_probe_retries_rate_limits_but_never_turns_them_into_success(self):
        self.http.response = (429, {}, b'')
        with patch.object(videos, 'check_public_url'), patch.object(videos.time, 'sleep'):
            with self.assertRaisesRegex(ValueError, 'three attempts'):
                videos.check_external(self.url + '/video', 3)
        self.assertEqual(self.http.requests, [('HEAD', '/video')] * 3)
        self.http.response = (404, {}, b''); self.http.requests = []
        with patch.object(videos, 'check_public_url'), self.assertRaisesRegex(ValueError, '404'):
            videos.check_external(self.url + '/video', 3)
        self.assertEqual(self.http.requests, [('HEAD', '/video')])

    def test_oversized_youtube_metadata_is_rejected(self):
        self.http.response = (200, {}, b'x' * 65537)
        with patch.object(videos, 'check_public_url'), patch.object(videos, 'OEMBED_URL', self.url + '/oembed'):
            with self.assertRaisesRegex(ValueError, '64 KiB'):
                videos.check_youtube('https://youtu.be/abcdefghijk')

    def test_s3_sdk_uses_fixed_bucket_key_and_no_get(self):
        import boto3
        from botocore.stub import Stubber
        client = boto3.client('s3', region_name='us-east-1', aws_access_key_id='testing',
                              aws_secret_access_key='testing')
        head = {'ContentLength': 3, 'Metadata': {'sha256': internal_video()['sha256']}}
        with Stubber(client) as stub:
            stub.add_response('head_object', head, {'Bucket': 'statics-aipochcom-prod',
                                                    'Key': 'open-science/usecases/a-case/demo.mp4'})
            with patch('boto3.session.Session.client', return_value=client):
                videos.validate_video({'name': 'a-case', 'video': internal_video()})
            stub.assert_no_pending_responses()

    def test_missing_s3_credentials_is_a_validation_error(self):
        from botocore.exceptions import NoCredentialsError
        with patch('boto3.session.Session.client', side_effect=NoCredentialsError()):
            with self.assertRaisesRegex(ValueError, 'credentials'):
                videos.validate_video({'name': 'a-case', 'video': internal_video()})

    def test_youtube_requires_valid_video_metadata_not_just_http_200(self):
        valid = {'type': 'video', 'provider_name': 'YouTube', 'title': 'Demo',
                 'html': '<iframe src="https://www.youtube.com/embed/abcdefghijk"></iframe>'}
        with patch.object(videos, 'check_public_url'), patch.object(videos, 'OEMBED_URL', self.url + '/oembed'):
            for body, good in ((valid, True), ({'type': 'link'}, False), ('html page', False)):
                data = json.dumps(body).encode()
                self.http.response = (200, {'Content-Type': 'application/json'}, data)
                if good:
                    videos.check_youtube('https://youtu.be/abcdefghijk')
                else:
                    with self.assertRaises(ValueError):
                        videos.check_youtube('https://youtu.be/abcdefghijk')

    def test_internal_requires_size_and_custom_metadata(self):
        entry = {'name': 'a-case', 'video': internal_video()}
        good = {'ContentLength': 3, 'Metadata': {'sha256': internal_video()['sha256']}}
        for head in (None, {'ContentLength': 3, 'Metadata': {}},
                     {**good, 'ContentLength': 4}, {**good, 'Metadata': {'sha256': 'f' * 64}}):
            with self.subTest(head=head), patch.object(videos, 's3_head', return_value=head):
                with self.assertRaises(ValueError):
                    videos.validate_video(entry)
        with patch.object(videos, 's3_head', return_value=good):
            videos.validate_video(entry)

    def test_public_url_blocks_private_networks_and_unsafe_redirect_targets(self):
        for url in ('http://example.com/a', 'https://127.0.0.1/a', 'https://user:pass@example.com/a',
                    'https://[::1]/a', 'https://example.com:444/a'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                videos.check_public_url(url)

    def test_dns_rebinding_cannot_connect_to_an_unvalidated_address(self):
        public = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('93.184.216.34', 443))]
        private = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 443))]
        connection = MagicMock()
        connection.connect.side_effect = RuntimeError('intercept connection')
        with patch.object(videos.socket, 'getaddrinfo', side_effect=[public, private]), \
                patch.object(videos.socket, 'socket', return_value=connection):
            with self.assertRaisesRegex(RuntimeError, 'intercept connection'):
                videos.request('https://public.example/video', 'HEAD')
        self.assertEqual(connection.connect.call_args.args[0], ('93.184.216.34', 443))


class VideoPublicationTests(GitFixture):
    def test_failed_video_keeps_old_manifest_and_writes_no_resources(self):
        baseline = json.dumps(self.entries)
        self.entry['video'] = internal_video()
        self.write_manifest(); self.commit()
        plan = self.ready(self.plan())
        store = Store(baseline)
        with patch.object(videos, 's3_head', return_value=None), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(Exception):
                publisher.apply(self.root, plan, store)
        self.assertEqual(store.manifest, baseline)
        self.assertEqual(store.writes, [])

    def test_video_only_publish_checks_reference_and_refreshes_case_cache(self):
        baseline = json.dumps(self.entries)
        self.entry['video'] = internal_video()
        self.write_manifest(); self.commit()
        plan = self.ready(self.plan())
        store = Store(baseline); refreshed = []
        store.refresh_cdn = refreshed.append
        head = {'ContentLength': 3, 'Metadata': {'sha256': internal_video()['sha256']}}
        with patch.object(videos, 's3_head', return_value=head), contextlib.redirect_stdout(io.StringIO()):
            publisher.apply(self.root, plan, store)
        self.assertEqual(json.loads(store.manifest)[0]['video'], internal_video())
        self.assertEqual(set(store.writes), {'manifest.json'})
        self.assertIn('a-case', refreshed)

    def test_local_metadata_command_outputs_actual_file_integrity(self):
        file = self.root / 'demo.mp4'; file.write_bytes(b'abc')
        script = Path(videos.__file__)
        result = subprocess.run([sys.executable, '-B', str(script), 'metadata', '--case', 'a-case', str(file)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), internal_video())

    def test_metadata_rejects_empty_files_and_symlinks(self):
        file = self.root / 'demo.mp4'; file.touch()
        link = self.root / 'link.mp4'; link.symlink_to(file)
        for path in (file, link):
            result = subprocess.run([sys.executable, '-B', videos.__file__, 'metadata', '--case', 'a-case', str(path)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, '')

    def test_removing_video_never_reads_or_deletes_the_video_object(self):
        old = copy.deepcopy(self.entries); old[0]['video'] = internal_video()
        baseline = json.dumps(old)
        plan = publisher.prepare(self.root, baseline, self.base)
        store = Store(baseline)
        plan = publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
        with patch.object(videos, 's3_head', side_effect=AssertionError('unexpected video access')):
            with contextlib.redirect_stdout(io.StringIO()):
                publisher.apply(self.root, plan, store)
        self.assertNotIn('video', json.loads(store.manifest)[0])
        self.assertEqual(set(store.writes), {'manifest.json'})

    def test_switch_from_s3_to_youtube_uses_platform_probe_only(self):
        old = copy.deepcopy(self.entries); old[0]['video'] = internal_video()
        baseline = json.dumps(old)
        self.entry['video'] = {'type': 'youtube', 'file_path': 'https://youtu.be/abcdefghijk', 'file_name': 'Demo'}
        self.write_manifest(); self.commit()
        store = Store(baseline)
        plan = publisher.prepare(self.root, baseline, self.git('rev-parse', 'HEAD'))
        plan = publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
        with patch.object(videos, 's3_head', side_effect=AssertionError('unexpected S3 video access')):
            with patch.object(videos, 'check_youtube', side_effect=ValueError('video unavailable')):
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(Exception):
                    publisher.apply(self.root, plan, store)
        self.assertEqual(store.manifest, baseline)

    def test_untrusted_cli_reports_s3_as_deferred_and_checks_schema(self):
        self.entry['video'] = internal_video(); self.write_manifest(); self.commit()
        cases = self.root / 'selected.json'
        cases.write_text(json.dumps(checker.selected_cases(self.entries)))
        result = subprocess.run([sys.executable, '-B', checker.__file__, 'videos',
                                 '--cases-file', str(cases), '--skip-s3'], cwd=self.root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('DEFERRED', result.stderr)
        self.entry['video']['bytes'] = False; self.write_manifest()
        cases.write_text(json.dumps(checker.selected_cases(self.entries)))
        failed = subprocess.run([sys.executable, '-B', checker.__file__, 'videos',
                                 '--cases-file', str(cases), '--skip-s3'], cwd=self.root,
                                capture_output=True, text=True)
        self.assertNotEqual(failed.returncode, 0)

    def test_unchanged_video_is_not_reprobed_for_title_edits(self):
        self.entry['video'] = internal_video(); self.write_manifest(); previous = self.commit()
        self.entry['title'] = 'Updated'; self.write_manifest(); self.commit()
        cases = self.root / 'selected.json'; cases.write_text(json.dumps(checker.selected_cases(self.entries)))
        result = subprocess.run([sys.executable, '-B', checker.__file__, 'videos', '--base', previous,
                                 '--cases-file', str(cases)], cwd=self.root,
                                env={**os.environ, 'AWS_EC2_METADATA_DISABLED': 'true'}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        baseline = self.git('show', previous + ':manifest.json')
        plan = publisher.prepare(self.root, baseline, self.git('rev-parse', 'HEAD'))
        store = Store(baseline)
        plan = publisher.prepare_resources(self.root, plan, store, self.root / 'sources')
        with patch.object(videos, 's3_head', side_effect=AssertionError('unexpected probe')):
            with contextlib.redirect_stdout(io.StringIO()):
                publisher.apply(self.root, plan, store)
        self.assertEqual(json.loads(store.manifest)[0]['title'], 'Updated')


if __name__ == '__main__':
    unittest.main()
