#!/usr/bin/env python3
"""Download changed science packages and prepare their extracted upload files."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unicodedata
from urllib.parse import quote, urlsplit
from urllib.request import urlopen

from manifest_diff import git
from publish import extracted_prefix, file_integrity
from check_structure import read_json


def relative_path(value):
    # Reject ambiguous names on Windows, macOS and Linux without renaming anything.
    if (not isinstance(value, str) or not value or len(value) > 2048
            or re.search(r'[\x00-\x1f\x7f\\:*?"<>|]', value)
            or PurePosixPath(value).is_absolute()):
        raise ValueError('Unsafe package path: ' + repr(value))
    for part in value.split('/'):
        if (part in ('', '.', '..') or part.endswith((' ', '.'))
                or re.fullmatch(r'(?i:con|prn|aux|nul|com[1-9¹²³]|lpt[1-9¹²³])(?:\..*)?', part)):
            raise ValueError('Unsafe package path: ' + repr(value))
    return value


def repository_path(value):
    # Repository filenames are URL components, not portable extraction paths.
    if (not isinstance(value, str) or not value or len(value) > 2048
            or re.search(r'[\x00-\x1f\x7f\\]', value)
            or any(part in ('', '.', '..') for part in value.split('/'))):
        raise ValueError('Unsafe repository path: ' + repr(value))
    return quote(value, safe='/')


def check_layout(entries):
    # Include implicit parents: A/x and a/y collide even when the leaves differ.
    nodes, explicit = {}, set()
    for path, is_directory in entries:
        relative_path(path)
        if path in explicit:
            raise ValueError('Duplicate path: ' + path)
        explicit.add(path)
        parts = path.split('/')
        for length in range(1, len(parts) + 1):
            name = '/'.join(parts[:length])
            directory = length < len(parts) or is_directory
            portable = unicodedata.normalize('NFC', name).casefold()
            previous = nodes.get(portable)
            if previous is not None and previous != (name, directory):
                raise ValueError('Portable path collision or file/directory conflict: ' + path)
            nodes[portable] = (name, directory)


def download(url, target, resource):
    if urlsplit(url).scheme not in ('http', 'https'):
        raise ValueError('Package download requires an HTTP(S) URL')
    expected = resource.get('sha256')
    size = resource.get('bytes')
    if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', expected):
        raise ValueError('Package requires a valid SHA-256 declaration')
    if type(size) is not int or size <= 0:
        raise ValueError('Package requires a positive byte size')
    # Stream large release packages to disk, binding mutable URLs to the declaration.
    digest = hashlib.sha256()
    count = 0
    with urlopen(url, timeout=60) as response, target.open('wb') as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            if count > size:
                raise ValueError('Downloaded package exceeds its declared byte size')
            digest.update(chunk); output.write(chunk)
    if digest.hexdigest() != expected.lower():
        raise ValueError('Downloaded package SHA-256 does not match the manifest')
    if count != size:
        raise ValueError('Downloaded package byte size does not match the manifest')


def unpack(package, output):
    if output.is_symlink() or not output.is_dir() or any(output.iterdir()):
        raise ValueError('Extraction requires an empty, non-symlink output directory')
    with tarfile.open(package, 'r:gz') as archive:
        members = archive.getmembers()
        # tarfile stops at the end-of-archive blocks, before gzip's CRC/size trailer.
        # Consume the tail too so truncated/corrupt compression cannot look complete.
        for chunk in iter(lambda: archive.fileobj.read(1024 * 1024), b''):
            if chunk.strip(b'\x00'):
                raise ValueError('Unexpected content after the tar end marker')
        for member in members:
            if (member.type not in (tarfile.REGTYPE, tarfile.AREGTYPE, tarfile.DIRTYPE)
                    or member.sparse is not None):
                raise ValueError('Link or special archive member: ' + member.name)
        check_layout([(member.name.removesuffix('/') if member.isdir() else member.name,
                       member.isdir()) for member in members])
        by_name = {member.name: member for member in members if member.isfile()}

        def package_json(name):
            if name not in by_name:
                raise ValueError('Missing package JSON: ' + name)
            with archive.extractfile(by_name[name]) as source:
                return read_json(source.read().decode('utf-8'), 'package ' + name)

        manifest = package_json('manifest.json')
        if (not isinstance(manifest, dict) or manifest.get('format') != 'open-science-session'
                or type(manifest.get('schemaVersion')) is not int or manifest['schemaVersion'] != 1
                or not isinstance(manifest.get('inventory'), list)):
            raise ValueError('Unsupported science package format')
        features = manifest.get('requiredFeatures', [])
        if not isinstance(features, list) or any(feature not in ('literature', 'ro-crate', 'content-dedupe')
                                                  for feature in features):
            raise ValueError('Unsupported package features')
        session = package_json('session.json')
        if (not isinstance(session, dict) or session.get('version') != 2
                or not isinstance(session.get('session'), dict)):
            raise ValueError('Unsupported session JSON')
        package_json('records.json')

        destinations = {'manifest.json': [('manifest.json', None)]}
        declared = {}
        for item in manifest['inventory']:
            if not isinstance(item, dict):
                raise ValueError('Invalid inventory entry')
            path = relative_path(item.get('path'))
            if path == 'manifest.json' or path not in by_name:
                raise ValueError('Missing or reserved inventory file: ' + path)
            size, checksum = item.get('sizeBytes'), item.get('checksum')
            if (type(size) is not int or size < 0 or size != by_name[path].size
                    or not isinstance(checksum, str) or not re.fullmatch(r'[a-fA-F0-9]{64}', checksum)):
                raise ValueError('Invalid inventory size or checksum: ' + path)
            key = relative_path(item['storageKey']) if 'storageKey' in item else path
            if key.split('/')[0].casefold() == 'objects':
                raise ValueError('Objects must be restored through storageKey: ' + path)
            if path in ('session.json', 'records.json', 'README.md') and 'storageKey' in item:
                raise ValueError('Package metadata cannot be relocated: ' + path)
            previous = declared.get(path)
            if previous is not None and (
                    'content-dedupe' not in features or 'storageKey' not in previous
                    or 'storageKey' not in item or previous['storageKey'] == key
                    or previous['sizeBytes'] != size or previous['checksum'] != checksum):
                raise ValueError('Invalid duplicate inventory path: ' + path)
            declared[path] = item
            destinations.setdefault(path, []).append((key, (size, checksum.lower())))
        if (not {'session.json', 'records.json', 'README.md'} <= declared.keys()
                or set(by_name) != set(declared) | {'manifest.json'}):
            raise ValueError('Package inventory is incomplete or contains undeclared files')
        check_layout([(key, False) for targets in destinations.values() for key, _ in targets])

        # Stage privately; malformed content never leaves a partial restored tree.
        verified = []
        with tempfile.TemporaryDirectory(prefix='.restore-', dir=output.parent) as temporary:
            staging = Path(temporary) / 'extracted'
            staging.mkdir()
            # Preserve archive order for gzip reads. Dedupe aliases copy the verified first output.
            for member in members:
                first = None
                for key, expected in destinations.get(member.name, []):
                    target = staging / key
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if first is None:
                        digest, count = hashlib.sha256(), 0
                        with archive.extractfile(member) as source, target.open('xb') as destination:
                            for chunk in iter(lambda: source.read(1024 * 1024), b''):
                                digest.update(chunk); count += len(chunk); destination.write(chunk)
                        actual = (count, digest.hexdigest())
                        if count != member.size or (expected is not None and actual != expected):
                            raise ValueError('Inventory content size or checksum mismatch: ' + member.name)
                        first = target
                    else:
                        shutil.copyfile(first, target)
                    # Read back every restored file, including metadata and dedupe aliases.
                    if file_integrity(target) != actual or (expected is not None and actual != expected):
                        raise ValueError('Restored content size or checksum mismatch: ' + key)
                    verified.append({'path': key, 'bytes': actual[0], 'sha256': actual[1]})
            output.rmdir()
            staging.rename(output)
        return verified


def expand_plan(root, plan, output, base_url):
    if git(root, 'rev-parse', 'HEAD').strip() != plan['after']:
        raise ValueError('Checkout must match the prepared target commit')
    if plan.get('extraction_complete'):
        raise ValueError('Extraction requires a fresh, unprepared plan')
    result = copy.deepcopy(plan)
    generated = []
    batch = None
    try:
        for package in plan.get('packages', []):
            prefix = extracted_prefix(package['name'])
            if batch is None:
                output.mkdir(parents=True, exist_ok=True)
                batch = Path(tempfile.mkdtemp(prefix='run-', dir=output))
            resource = package['resource']
            url = resource.get('release_url')
            if not url:
                url = base_url.rstrip('/') + '/' + repository_path(resource['path'])
            directory = batch / package['name']
            directory.mkdir()
            downloaded = directory / 'package.science'
            print('Downloading and extracting: ' + package['name'], flush=True)
            download(url, downloaded, resource)
            extracted = directory / 'extracted'
            extracted.mkdir()
            verified = unpack(downloaded, extracted)
            for item in sorted(verified, key=lambda item: item['path']):
                generated.append({**item, 'path': str((extracted / item['path']).resolve()),
                                  'key': prefix + item['path']})
            downloaded.unlink()
    except BaseException:
        if batch is not None:
            shutil.rmtree(batch)
        raise
    # Publish readiness only after every download and unpack succeeds; manifest stays last.
    result['files'] = ([item for item in plan['files'] if item['key'] != 'manifest.json']
                       + generated
                       + [item for item in plan['files'] if item['key'] == 'manifest.json'])
    result['extraction_complete'] = True
    return result


def main():
    if int(os.environ.get('GITHUB_RUN_ATTEMPT', '1')) != 1:
        raise ValueError('Native reruns are disabled; use workflow_dispatch on main')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    # A retry must never leave a previously ready plan publishable after failing.
    if plan.get('extraction_complete'):
        plan['extraction_complete'] = False
        args.plan.write_text(json.dumps(plan) + '\n', encoding='utf-8')
        raise ValueError('Prepare a fresh plan before retrying extraction')
    result = expand_plan(Path.cwd(), plan, args.output.resolve(), os.environ.get('CASE_FILE_BASE_URL', ''))
    args.plan.write_text(json.dumps(result) + '\n', encoding='utf-8')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, EOFError, tarfile.TarError, subprocess.CalledProcessError) as error:
        print('Extraction failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
