"""Filesystem AWS boundary with explicit read failures and object metadata."""
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
if args[:2] == ['s3api', 'get-object']:
    assert args[2] == '--bucket' and args[4] == '--key' and len(args) == 7, args
    path = root / args[3] / args[5]
    error = os.environ.get('FAKE_S3_GET_ERROR') or (None if path.is_file() else 'NoSuchKey')
    if error:
        print('An error occurred (' + error + ') when calling the GetObject operation', file=sys.stderr)
        sys.exit(254)
    Path(args[6]).write_bytes(path.read_bytes())
    print('{}')
    sys.exit(0)
if args[:2] == ['s3', 'rm']:
    assert args[3:] == ['--recursive', '--only-show-errors'], args
    assert args[2].endswith('/extracted/'), args
    uri = urlsplit(args[2])
    path = root / uri.netloc / uri.path.lstrip('/')
    if path.exists():
        shutil.rmtree(path)
    sys.exit(0)
assert args[:2] == ['s3', 'cp'] and args[4] == '--only-show-errors', args
uri = urlsplit(args[3])
key = uri.netloc + '/' + uri.path.lstrip('/')
path = root / key
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(Path(args[2]).read_bytes())
metadata_file = root / 'metadata.json'
metadata = json.loads(metadata_file.read_text()) if metadata_file.exists() else {}
metadata[key] = dict([args[6].split('=', 1)]) if args[5:6] == ['--metadata'] else {}
metadata_file.write_text(json.dumps(metadata))
