"""Filesystem AWS boundary: conditional commits, object checks and CDN failure injection."""
import hashlib
import json
import os
import shutil
from pathlib import Path
import sys
from urllib.parse import urlsplit

args = sys.argv[1:]
root = Path(os.environ['FAKE_S3_ROOT'])
with (root / 'calls.jsonl').open('a') as stream:
    stream.write(json.dumps(args) + '\n')
if os.environ.get('FAKE_S3_FAIL') == args[1]:
    sys.exit(1)

output_format = os.environ.get('AWS_DEFAULT_OUTPUT', 'json')
if '--output' in args:
    index = args.index('--output')
    output_format = args[index + 1]
    del args[index:index + 2]


def emit(value):
    if output_format == 'json':
        print(json.dumps(value))
    elif output_format == 'text':
        # AWS text output is tab-delimited, not a JSON document.
        print('\t'.join(str(item) for item in value.values()))
    else:
        raise AssertionError('Unsupported fixture output format: ' + output_format)


def option(name):
    return args[args.index(name) + 1]


def etag(path):
    return '"' + hashlib.md5(path.read_bytes()).hexdigest() + '"'


def metadata(key, value=None):
    file = root / 'metadata.json'
    values = json.loads(file.read_text()) if file.exists() else {}
    if value is not None:
        values[key] = value
        file.write_text(json.dumps(values))
    return values.get(key, {})


if args[:2] == ['s3api', 'get-object']:
    assert args[2] == '--bucket' and args[4] == '--key' and len(args) == 7, args
    path = root / args[3] / args[5]
    error = os.environ.get('FAKE_S3_GET_ERROR') or (None if path.is_file() else 'NoSuchKey')
    if os.environ.get('FAKE_S3_FAIL_READ_AFTER_PUT') and (root / 'manifests.jsonl').exists():
        error = 'RequestTimeout'
    if error:
        print('An error occurred (' + error + ') when calling the GetObject operation', file=sys.stderr)
        sys.exit(254)
    Path(args[6]).write_bytes(path.read_bytes())
    emit({'ETag': etag(path)})
    sys.exit(0)
if args[:2] == ['s3api', 'head-object']:
    key = option('--bucket') + '/' + option('--key')
    path = root / key
    error = os.environ.get('FAKE_S3_HEAD_ERROR') or (None if path.is_file() else '404')
    if error:
        print('An error occurred (' + error + ') when calling the HeadObject operation', file=sys.stderr)
        sys.exit(254)
    emit({'ContentLength': path.stat().st_size + int(bool(os.environ.get('FAKE_S3_BAD_HEAD'))), 'Metadata': metadata(key)})
    sys.exit(0)
if args[:2] == ['s3api', 'put-object']:
    key = option('--bucket') + '/' + option('--key')
    path = root / key
    if (os.environ.get('FAKE_S3_CONFLICT') or
            ('--if-match' in args and (not path.exists() or option('--if-match') != etag(path))) or
            ('--if-none-match' in args and path.exists())):
        print('PreconditionFailed', file=sys.stderr)
        sys.exit(254)
    history = root / 'manifests.jsonl'
    count = len(history.read_text().splitlines()) if history.exists() else 0
    if os.environ.get('FAKE_S3_FAIL_PUT_NUMBER') == str(count + 1):
        sys.exit(1)
    body = Path(option('--body')).read_bytes()
    fail_case = os.environ.get('FAKE_S3_FAIL_MANIFEST_CASE')
    if fail_case:
        old = {e['name']: e for e in json.loads(path.read_text())} if path.exists() else {}
        new = {e['name']: e for e in json.loads(body)}
        if new.get(fail_case) != old.get(fail_case):
            sys.exit(1)
    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(body)
    metadata(key, dict([option('--metadata').split('=', 1)]))
    with (root / 'manifests.jsonl').open('a') as stream:
        stream.write(json.dumps(json.loads(body)) + '\n')
    emit({'ETag': etag(path)})
    if os.environ.get('FAKE_S3_TIMEOUT_AFTER_PUT'):
        print('Read timeout on endpoint URL', file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
if args[:2] == ['cloudfront', 'create-invalidation']:
    assert option('--paths').startswith('/'), args
    emit({'Invalidation': {'Id': 'fixture-invalidation'}})
    sys.exit(0)
if args[:2] == ['cloudfront', 'wait']:
    assert args[2] == 'invalidation-completed', args
    sys.exit(0)
if args[:2] == ['s3', 'rm']:
    assert args[3:] == ['--recursive', '--only-show-errors'], args
    assert args[2].endswith('/extracted/'), args
    uri = urlsplit(args[2]); path = root / uri.netloc / uri.path.lstrip('/')
    if path.exists():
        shutil.rmtree(path)
    sys.exit(0)
assert args[:2] == ['s3', 'cp'] and args[4] == '--only-show-errors', args
uri = urlsplit(args[3]); key = uri.netloc + '/' + uri.path.lstrip('/')
path = root / key
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(Path(args[2]).read_bytes())
metadata(key, dict([args[6].split('=', 1)]))
