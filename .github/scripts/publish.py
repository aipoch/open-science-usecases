#!/usr/bin/env python3
"""Compare the target S3 manifest with a fixed checkout, then publish resources."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

from check_structure import is_image_filename, is_science_url, kebab_case, read_json
from manifest_diff import changed_entries, git, local_resources


def read_manifest(text, source):
    # Reject ambiguous or malformed baselines rather than treating them as empty.
    entries = read_json(text, source)
    if not isinstance(entries, list):
        raise ValueError(source + ' must be an array of case objects')
    names = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(source + ': invalid case object')
        name = entry.get('name')
        extracted_prefix(name)
        if name in names:
            raise ValueError(source + ': Duplicate case name: ' + name)
        names.add(name)
        if not isinstance(entry.get('title'), str) or not entry['title'].strip():
            raise ValueError(source + ': missing case title')
        if not {'cover', 'case'} <= entry.keys():
            raise ValueError(source + ': missing cover or case resource')
        folders = set()
        for kind, extension in (('cover', None), ('case', '.science'), ('introduction', '.md')):
            if kind not in entry:
                continue  # Legacy cases can omit an introduction.
            resource = entry[kind]
            if not isinstance(resource, dict):
                raise ValueError(source + ': invalid ' + kind + ' resource')
            path, filename = resource.get('path'), resource.get('file_name')
            if (not isinstance(path, str) or '\\' in path or '\x00' in path
                    or len(path.split('/')) != 2
                    or any(part in ('', '.', '..') for part in path.split('/'))
                    or PurePosixPath(path).is_absolute()
                    or filename != path.split('/')[-1]
                    or not (is_image_filename(filename) if kind == 'cover' else filename.endswith(extension))):
                raise ValueError(source + ': invalid resource path or file_name')
            folders.add(path.split('/')[0])
            if type(resource.get('bytes')) is not int or resource['bytes'] < 0:
                raise ValueError(source + ': invalid resource byte size')
            sha = resource.get('sha256')
            if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', sha):
                raise ValueError(source + ': resource requires a 64-digit SHA-256')
            if kind == 'case':
                url = resource.get('release_url')
                if url != '' and not is_science_url(url):
                    raise ValueError(source + ': invalid case.release_url')
        if len(folders) != 1:
            raise ValueError(source + ': resources must share one case directory')
    local_resources(entries)  # Also reject colliding upload destinations.
    return entries


def resource_changed(previous, current):
    if previous is None:
        return True
    # Hexadecimal spelling is not a content change; other resource metadata is.
    return ({**previous, 'sha256': previous['sha256'].lower()}
            != {**current, 'sha256': current['sha256'].lower()})


def check_sources(root, entries):
    cases = []
    # Validate every affected case before any package download or extraction.
    for entry in entries:
        directory = entry['cover']['path'].split('/')[0]
        if entry['name'] != kebab_case(directory):
            raise ValueError('Case name must match its directory: ' + directory)
        folder = root / directory
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError('Missing or invalid case directory: ' + directory)
        for kind in ('cover', 'case', 'introduction'):
            if kind not in entry:
                continue
            resource = entry[kind]
            path = root / resource['path']
            if path.is_symlink():
                raise ValueError('Resource source must not be a symlink: ' + resource['path'])
            if kind == 'case' and resource['release_url']:
                if path.exists():
                    raise ValueError('Package requires exactly one source: ' + resource['path'])
            elif not path.is_file():
                raise ValueError('Planned resource source is missing: ' + resource['path'])
        cases.append({'directory': directory, 'name': entry['name'], 'valid': True,
                      'has_local_science': not bool(entry['case']['release_url'])})
    return cases


def prepare(root, baseline, after):
    if git(root, 'rev-parse', 'HEAD').strip() != after:
        raise ValueError('Checkout must match the fixed target commit')
    current_text = git(root, 'show', after + ':manifest.json')
    if (root / 'manifest.json').read_bytes() != current_text.encode('utf-8'):
        raise ValueError('Checkout manifest.json differs from the fixed target commit')
    old = [] if baseline is None else read_manifest(baseline, 'S3 manifest.json')
    new = read_manifest(current_text, 'repository manifest.json')
    cases = check_sources(root, changed_entries(old, new))
    previous, current = local_resources(old), local_resources(new)
    files = [{'path': resource['path'], 'key': key} for key, resource in current.items()
             if resource_changed(previous.get(key), resource)]
    previous_cases = {entry['name']: entry for entry in old}
    packages = [{'name': entry['name'], 'resource': entry['case']} for entry in new
                if resource_changed(previous_cases.get(entry['name'], {}).get('case'), entry['case'])]
    if baseline != current_text:
        files.append({'path': 'manifest.json', 'key': 'manifest.json'})
    return {'after': after, 'files': files, 'packages': packages, 'cases': cases}


def extracted_prefix(name):
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Invalid case name for extracted prefix')
    return name + '/extracted/'


def file_integrity(path):
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


class S3:
    def __init__(self, target):
        uri = urlsplit(target)
        if uri.scheme != 's3' or not uri.netloc or uri.query or uri.fragment:
            raise ValueError('AWS_TARGET_FOLDER must be an s3://bucket[/prefix] URI')
        self.target = target.rstrip('/')
        self.bucket = uri.netloc
        self.manifest_key = uri.path.strip('/') + '/manifest.json' if uri.path.strip('/') else 'manifest.json'

    def read_manifest(self):
        # Only NoSuchKey establishes first publication. Access/network/bucket
        # errors (including ambiguous 404s) must stop without preparing uploads.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'manifest.json'
            result = subprocess.run(['aws', 's3api', 'get-object', '--bucket', self.bucket,
                                     '--key', self.manifest_key, str(path)],
                                    capture_output=True, text=True)
            if result.returncode:
                if re.search(r'\(NoSuchKey\) when calling the GetObject operation', result.stderr):
                    return None
                raise ValueError('Cannot read S3 manifest.json: ' + result.stderr.strip())
            return path.read_bytes().decode('utf-8')

    def upload(self, path, key):
        # Metadata describes uploaded bytes, including unchanged package metadata,
        # and never copies an unverified checksum declaration from the manifest.
        _, checksum = file_integrity(path)
        subprocess.run(['aws', 's3', 'cp', str(path), self.target + '/' + key,
                        '--only-show-errors', '--metadata', 'sha256=' + checksum], check=True)

    def clear_extracted(self, name):
        # Trailing slash prevents deleting similarly named sibling prefixes.
        subprocess.run(['aws', 's3', 'rm', self.target + '/' + extracted_prefix(name),
                        '--recursive', '--only-show-errors'], check=True)


def apply(root, plan, s3):
    if git(root, 'rev-parse', 'HEAD').strip() != plan['after']:
        raise ValueError('Checkout must match the prepared target commit')
    packages = plan.get('packages', [])
    if packages:
        if plan.get('extraction_complete') is not True:
            raise ValueError('All packages must be extracted before publication')
        keys = {item['key'] for item in plan['files']}
        for package in packages:
            for metadata in ('session.json', 'records.json', 'manifest.json'):
                if extracted_prefix(package['name']) + metadata not in keys:
                    raise ValueError('Extracted metadata is missing from the upload plan: ' + metadata)
    # Preflight all files, even plans without packages, before any remote writes.
    prefixes = tuple(extracted_prefix(package['name']) for package in packages)
    for item in plan['files']:
        path = root / item['path']
        if not path.is_file() or path.is_symlink():
            raise ValueError('Planned upload file is missing or invalid: ' + item['path'])
        if item['key'].startswith(prefixes):
            if file_integrity(path) != (item.get('bytes'), item.get('sha256')):
                raise ValueError('Staged extraction size or checksum mismatch: ' + item['key'])
    for package in packages:
        s3.clear_extracted(package['name'])
    # Do not depend on caller ordering to keep the publication index last.
    for item in sorted(plan['files'], key=lambda item: item['key'] == 'manifest.json'):
        s3.upload(root / item['path'], item['key'])
    print('Uploaded {} files.'.format(len(plan['files'])))


def main():
    # Failed-jobs-only reruns could reuse a stale checkout; dispatch a fresh main run.
    if int(os.environ.get('GITHUB_RUN_ATTEMPT', '1')) != 1:
        raise ValueError('Native reruns are disabled; use workflow_dispatch on main')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--after')
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--prepare', type=Path)
    modes.add_argument('--dry-run', action='store_true')
    modes.add_argument('--apply-plan', type=Path)
    args = parser.parse_args()
    root = Path.cwd()
    s3 = S3(os.environ.get('AWS_TARGET_FOLDER', ''))
    if args.apply_plan:
        apply(root, json.loads(args.apply_plan.read_text()), s3)
        return
    plan = prepare(root, s3.read_manifest(), args.after)
    for item in plan['files']:
        print('Upload/replace: ' + json.dumps(item['key'], ensure_ascii=True))
    print('Prepared {} files and {} packages against S3 manifest.json.'.format(
        len(plan['files']), len(plan['packages'])))
    if args.prepare:
        args.prepare.write_text(json.dumps(plan, ensure_ascii=True) + '\n', encoding='utf-8')
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
                stream.write('has_uploads=' + str(bool(plan['files'])).lower() + '\n')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('Publish failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
