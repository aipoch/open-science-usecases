"""Real SDK HTTP requests to localhost only, plus transport configuration checks."""
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from publish import S3


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_PUT(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        with self.server.lock:
            self.server.objects[self.path] = (data, dict(self.headers))
            self.server.ports.add(self.client_address[1])
        self.send_response(200)
        self.send_header('ETag', '"' + hashlib.md5(data).hexdigest() + '"')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_HEAD(self):
        with self.server.lock:
            value = self.server.objects.get(self.path)
            self.server.ports.add(self.client_address[1])
        if self.path.endswith('/denied'):
            self.send_response(403)
            self.send_header('Content-Length', '0')
        elif value is None:
            self.send_response(404)
            self.send_header('Content-Length', '0')
        else:
            data, headers = value
            self.send_response(200)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Last-Modified', 'Tue, 13 Oct 2026 12:00:00 GMT')
            self.send_header('x-amz-meta-sha256', headers['x-amz-meta-sha256'])
        self.end_headers()

    def log_message(self, *args):
        pass


class SdkTransferTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.server.objects, self.server.ports = {}, set()
        self.server.lock = threading.Lock()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = {'AWS_ACCESS_KEY_ID': 'fixture', 'AWS_SECRET_ACCESS_KEY': 'fixture',
                    'AWS_DEFAULT_REGION': 'us-east-1', 'AWS_EC2_METADATA_DISABLED': 'true',
                    'AWS_ENDPOINT_URL_S3': 'http://127.0.0.1:' + str(self.server.server_port)}
        self.enterContext(patch.dict(os.environ, self.env))
        self.s3 = S3('s3://fixture/cases')
        self.s3.enable_transfers(4)
        self.addCleanup(self.s3.client.close)

    def test_put_and_head_keep_distinct_sha_mime_keys_and_reuse_connections(self):
        files = []
        for n in range(16):
            path = self.root / (str(n) + '.png')
            path.write_bytes(('image fixture ' + str(n)).encode())
            files.append(path)
        def transfer(path):
            key = 'a-case/space + ü/' + path.name
            self.s3.upload(path, key)
            self.s3.verify_upload(key, path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest())
            json.dumps(self.s3.head(key))  # HEAD evidence must be safe in the persisted plan.
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(transfer, files))
        self.assertEqual(len(self.server.objects), 16)
        self.assertLessEqual(len(self.server.ports), 4)
        for key, (body, headers) in self.server.objects.items():
            self.assertIn('/fixture/cases/a-case/space%20%2B%20%C3%BC/', key)
            self.assertEqual(headers['x-amz-meta-sha256'], hashlib.sha256(body).hexdigest())
            self.assertEqual(headers['Content-Type'], 'image/png')
        self.assertFalse(self.s3.transfer_config.use_threads)
        self.assertEqual(self.s3.transfer_config.preferred_transfer_client, 'classic')
        self.assertEqual(self.s3.client.meta.config.max_pool_connections, 4)
        self.assertEqual(self.s3.client.meta.config.retries['total_max_attempts'], 3)

    def test_large_file_uses_managed_multipart_with_per_object_metadata(self):
        from botocore.stub import Stubber
        path = self.root / 'large.science'
        path.write_bytes(b'x' * (9 * 1024 * 1024))
        calls = []
        def record(params, model, **kwargs):
            calls.append((model.name, dict(params)))
        self.s3.client.meta.events.register('before-parameter-build.s3', record)
        with Stubber(self.s3.client) as stub:
            stub.add_response('create_multipart_upload', {'UploadId': 'fixture'})
            stub.add_response('upload_part', {'ETag': 'part-1'})
            stub.add_response('upload_part', {'ETag': 'part-2'})
            stub.add_response('complete_multipart_upload', {'ETag': 'complete'})
            self.s3.upload(path, 'a-case/large.science')
            stub.assert_no_pending_responses()
        self.assertEqual([name for name, _ in calls],
                         ['CreateMultipartUpload', 'UploadPart', 'UploadPart', 'CompleteMultipartUpload'])
        self.assertTrue(all(params['Bucket'] == 'fixture' and params['Key'] == 'cases/a-case/large.science'
                            for _, params in calls))
        self.assertEqual(calls[0][1]['Metadata']['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(calls[0][1]['ContentType'], 'application/octet-stream')
        self.assertEqual([calls[1][1]['PartNumber'], calls[2][1]['PartNumber']], [1, 2])

    def test_only_missing_object_is_deduplicated_as_absent(self):
        self.assertIsNone(self.s3.head('missing'))
        with self.assertRaisesRegex(ValueError, '403'):
            self.s3.head('denied')
