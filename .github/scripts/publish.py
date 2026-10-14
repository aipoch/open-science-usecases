#!/usr/bin/env python3
"""Compare the target S3 manifest with a fixed checkout, then publish resources."""
import argparse
import copy
import shutil
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import quote, urlsplit

from check_structure import catalog_errors, read_json, schema_errors, source_errors, selected_cases
from manifest_diff import changed_entries, git
from publication_steps import (build_steps, group_files, write_artifacts, print_plan,
                               Reporter)


KINDS = ('cover', 'case', 'introduction')


def read_manifest(text, source, legacy=True):
    entries = read_json(text, source)
    if not isinstance(entries, list):
        raise ValueError(source + ' must be an array of case objects')
    names = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(source + ': invalid case object')
        errors = schema_errors(entry, legacy=legacy)
        if errors:
            raise ValueError(source + ': ' + '; '.join(errors))
        if entry['name'] in names:
            raise ValueError(source + ': Duplicate case name: ' + entry['name'])
        names.add(entry['name'])
    errors = catalog_errors(entries, legacy=legacy)
    if errors:
        raise ValueError(source + ': ' + '; '.join(errors))
    return entries


def candidate_reasons(previous, current):
    if previous is None:
        return ['new resource'], False
    source_changed = previous.get('release_url', '') != current.get('release_url', '')
    reasons = ['release_url'] if source_changed else []
    for field in ('file_name', 'bytes', 'sha256'):
        old, new = previous[field], current[field]
        if field == 'sha256':
            old, new = old.lower(), new.lower()
        if old != new:
            reasons.append(field)
    return reasons, source_changed


def check_sources(root, entries):
    for entry in entries:
        errors = source_errors(root, entry)
        if errors:
            raise ValueError('; '.join(errors))
    return selected_cases(entries)


def prepare(root, baseline, after, *, check_local=True):
    if git(root, 'rev-parse', 'HEAD').strip() != after:
        raise ValueError('Checkout must match the fixed target commit')
    current_text = git(root, 'show', after + ':manifest.json')
    if (root / 'manifest.json').read_bytes() != current_text.encode('utf-8'):
        raise ValueError('Checkout manifest.json differs from the fixed target commit')
    old = [] if baseline is None else read_manifest(baseline, 'S3 manifest.json')
    new = read_manifest(current_text, 'repository manifest.json', legacy=False)
    changed = changed_entries(old, new)
    cases = check_sources(root, changed) if check_local else selected_cases(changed)
    previous = {entry['name']: entry for entry in old}
    candidates, packages = [], []
    for entry in new:
        for kind in KINDS:
            resource = entry[kind]
            reasons, force = candidate_reasons(previous.get(entry['name'], {}).get(kind), resource)
            if not reasons:
                continue
            candidates.append({'name': entry['name'], 'kind': kind, 'path': resource['path'],
                               'key': entry['name'] + '/' + resource['file_name'],
                               'bytes': resource['bytes'], 'sha256': resource['sha256'].lower(),
                               'release_url': resource['release_url'], 'reasons': reasons,
                               'force_upload': force})
            if kind == 'case':
                packages.append({'name': entry['name'], 'resource': resource})
    files = copy.deepcopy(candidates) + [{'path': 'manifest.json', 'key': 'manifest.json'}]
    return group_files({'after': after, 'baseline': baseline, 'candidates': candidates,
                        'files': files, 'packages': packages, 'cases': cases,
                        'unchanged': [entry['name'] for entry in new if previous.get(entry['name']) == entry],
                        'steps': build_steps(old, new, current_text)})


def matching_head(head, item):
    if not isinstance(head, dict):
        return False
    checksum = head.get('Metadata', {}).get('sha256')
    return (type(head.get('ContentLength')) is int and head['ContentLength'] == item['bytes']
            and isinstance(checksum, str) and checksum.lower() == item['sha256'])


def scope_plan(plan, names):
    """Restrict resource work to coordinator-selected cases, never to plan-supplied scope."""
    result = copy.deepcopy(plan)
    for field in ('candidates', 'packages'):
        result[field] = [item for item in result[field] if item['name'] in names]
    result['files'] = [item for item in result['files']
                       if item['key'] == 'manifest.json' or item['key'].split('/', 1)[0] in names]
    result['cases'] = [item for item in result['cases'] if item['entry']['name'] in names]
    return group_files(result)


def verify_plan(root, plan, *, names=None, check_local=True):
    expected = prepare(root, plan['baseline'], plan['after'], check_local=check_local)
    if names is not None:
        expected = scope_plan(expected, names)
    for field in ('candidates', 'packages', 'cases', 'unchanged'):
        if plan.get(field) != expected[field]:
            raise ValueError('Prepared ' + field + ' differ from the fixed target')
    if len(plan['steps']) != len(expected['steps']):
        raise ValueError('Prepared publication steps differ from the fixed target')
    for actual, wanted in zip(plan['steps'], expected['steps']):
        for field in ('id', 'operation', 'name', 'before', 'after', 'manifest'):
            if actual[field] != wanted[field]:
                raise ValueError('Prepared publication step differs: ' + field)
    grouped = group_files(copy.deepcopy(plan))
    for actual, rebuilt in zip(plan['steps'], grouped['steps']):
        if actual['files'] != rebuilt['files'] or actual['packages'] != rebuilt['packages']:
            raise ValueError('Checkpoint upload lists differ from plan inventory')
    return expected


def prepare_resources(root, plan, s3, output, *, names=None, check_local=True):
    from extract_science import download
    expected = verify_plan(root, plan, names=names, check_local=check_local)
    if plan.get('resources_prepared') or plan['files'] != expected['files']:
        raise ValueError('Resource preparation requires a fresh plan')
    result = copy.deepcopy(plan)
    decisions, files = [], []
    output.mkdir(parents=True, exist_ok=True)
    batch = Path(tempfile.mkdtemp(prefix='sources-', dir=output)).resolve()
    try:
        for item in plan['candidates']:
            # Only selected, non-forced covers/introductions consult target metadata.
            head = s3.head(item['key']) if item['kind'] != 'case' and not item['force_upload'] else None
            skip = item['kind'] != 'case' and not item['force_upload'] and matching_head(head, item)
            decisions.append({'key': item['key'], 'action': 'skip' if skip else 'upload',
                              'head': head, 'reason': 'target SHA and size match' if skip else 'upload required'})
            if skip:
                continue
            target = batch / item['name'] / item['key'].split('/', 1)[1]
            target.parent.mkdir(parents=True, exist_ok=True)
            if item['release_url']:
                download(item['release_url'], target, item)
            else:
                # Bind local input to the fixed Git tree as well as the declared digest.
                listing = git(root, '--literal-pathspecs', 'ls-tree', plan['after'], '--', item['path']).split()
                if not listing or listing[0] not in ('100644', '100755'):
                    raise ValueError('Local source must be a committed regular file: ' + item['path'])
                subprocess.run(['git', '--literal-pathspecs', 'diff', '--quiet', plan['after'], '--', item['path']],
                               cwd=root, check=True)
                shutil.copyfile(root / item['path'], target)
            if file_integrity(target) != (item['bytes'], item['sha256']):
                raise ValueError('Prepared file size or checksum mismatch: ' + item['key'])
            files.append({**item, 'path': str(target)})
    except BaseException:
        shutil.rmtree(batch)
        raise
    result.update(files=files + [{'path': 'manifest.json', 'key': 'manifest.json'}],
                  decisions=decisions, resources_prepared=True)
    return group_files(result)


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
        self.client = None
        self.target = target.rstrip('/')
        self.bucket = uri.netloc
        self.manifest_key = uri.path.strip('/') + '/manifest.json' if uri.path.strip('/') else 'manifest.json'

    def read_manifest(self):
        # Only NoSuchKey establishes first publication. Access/network/bucket
        # errors (including ambiguous 404s) must stop without preparing uploads.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'manifest.json'
            result = subprocess.run(['aws', 's3api', 'get-object', '--bucket', self.bucket,
                                     '--key', self.manifest_key, str(path), '--output', 'json'],
                                    capture_output=True, text=True)
            if result.returncode:
                if re.search(r'\(NoSuchKey\) when calling the GetObject operation', result.stderr):
                    self.etag = None
                    return None
                raise ValueError('Cannot read S3 manifest.json: ' + result.stderr.strip())
            self.etag = json.loads(result.stdout)['ETag']
            return path.read_bytes().decode('utf-8')

    def enable_transfers(self, workers=32):
        # Construct the shared client before starting workers; no default-session races.
        import boto3.session
        from botocore.config import Config
        from boto3.s3.transfer import TransferConfig
        self.client = boto3.session.Session().client('s3', config=Config(
            max_pool_connections=workers, retries={'mode': 'standard', 'total_max_attempts': 3},
            connect_timeout=15, read_timeout=60))
        self.transfer_config = TransferConfig(use_threads=False, preferred_transfer_client='classic')

    def upload(self, path, key):
        _, checksum = file_integrity(path)
        content_type = mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
        self.client.upload_file(str(path), self.bucket, self.object_key(key),
                                ExtraArgs={'Metadata': {'sha256': checksum}, 'ContentType': content_type},
                                Config=self.transfer_config)

    def head(self, key):
        from botocore.exceptions import ClientError
        if self.client is None:
            self.enable_transfers()
        try:
            head = self.client.head_object(Bucket=self.bucket, Key=self.object_key(key))
            # SDK responses also contain datetime objects and transport diagnostics.
            return {'ContentLength': head['ContentLength'], 'Metadata': head.get('Metadata', {})}
        except ClientError as error:
            if error.response.get('Error', {}).get('Code') in ('404', 'NoSuchKey', 'NotFound'):
                return None
            raise ValueError('Cannot HEAD target S3 object: ' + str(error)) from error

    def verify_upload(self, key, size, checksum):
        if not matching_head(self.head(key), {'bytes': size, 'sha256': checksum.lower()}):
            raise ValueError('Uploaded object metadata mismatch: ' + key)

    def object_key(self, key):
        prefix = self.manifest_key.removesuffix('manifest.json')
        return prefix + key

    def commit_manifest(self, path):
        # Compare-and-swap protects the index; resources still require the workflow lock.
        condition = ['--if-match', self.etag] if self.etag is not None else ['--if-none-match', '*']
        subprocess.run(['aws', 's3api', 'put-object', '--bucket', self.bucket,
                        '--key', self.manifest_key, '--body', str(path),
                        '--content-type', 'application/json', '--metadata', 'sha256=' + file_integrity(path)[1],
                        *condition], capture_output=True, text=True, check=True)

    def refresh_cdn(self, case_name=None):
        distribution = os.environ['AWS_DISTRIBUITION_ID']
        # Manifest-only checkpoints keep unrelated resource caches warm.
        paths = [quote('/' + self.manifest_key, safe='/')]
        if case_name:
            paths.append(quote('/' + self.object_key(case_name + '/'), safe='/') + '*')
        print('CDN paths: ' + json.dumps(paths), flush=True)
        result = subprocess.run(['aws', 'cloudfront', 'create-invalidation',
                                 '--distribution-id', distribution, '--output', 'json', '--paths', *paths],
                                capture_output=True, text=True, check=True)
        identifier = json.loads(result.stdout)['Invalidation']['Id']
        print('CDN invalidation submitted: ' + identifier, flush=True)
        subprocess.run(['aws', 'cloudfront', 'wait', 'invalidation-completed',
                        '--distribution-id', distribution, '--id', identifier], check=True)

    def clear_extracted(self, name):
        # Trailing slash prevents deleting similarly named sibling prefixes.
        subprocess.run(['aws', 's3', 'rm', self.target + '/' + extracted_prefix(name),
                        '--recursive', '--only-show-errors'], check=True)


def validate_prepared(root, plan, s3, *, names=None, check_local=True):
    if git(root, 'rev-parse', 'HEAD').strip() != plan['after']:
        raise ValueError('Checkout must match the prepared target commit')
    expected = verify_plan(root, plan, names=names, check_local=check_local)
    candidates = {item['key']: item for item in expected['candidates']}
    if candidates and plan.get('resources_prepared') is not True:
        raise ValueError('All selected resources must be prepared before publication')
    decisions = plan.get('decisions', [])
    if len(decisions) != len(candidates) or {d['key'] for d in decisions} != candidates.keys():
        raise ValueError('Prepared resource decisions are missing or duplicated')
    skipped = set()
    for decision in decisions:
        item = candidates[decision['key']]
        if decision['action'] == 'skip':
            if (item['force_upload'] or item['kind'] == 'case'
                    or not matching_head(decision.get('head'), item)
                    or decision.get('reason') != 'target SHA and size match'):
                raise ValueError('Invalid or forged skip decision: ' + item['key'])
            # Revalidate every skipped object before the first write in the entire batch.
            if not matching_head(s3.head(item['key']), item):
                raise ValueError('Target changed since skip decision: ' + item['key'])
            skipped.add(item['key'])
        elif decision['action'] != 'upload':
            raise ValueError('Invalid resource decision')
    originals = {}
    generated = {}
    seen = set()
    for item in plan['files']:
        key = item['key']
        if key in seen:
            raise ValueError('Duplicate planned upload: ' + key)
        seen.add(key)
        if key == 'manifest.json':
            if item != {'path': 'manifest.json', 'key': 'manifest.json'}:
                raise ValueError('Manifest upload differs from fixed target')
            continue
        path = root / item['path']
        if not path.is_file() or any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('Planned upload file is missing or invalid: ' + item['path'])
        if file_integrity(path) != (item.get('bytes'), item.get('sha256')):
            raise ValueError('Staged file size or checksum mismatch: ' + key)
        if key in candidates:
            if key in skipped or {**item, 'path': candidates[key]['path']} != candidates[key]:
                raise ValueError('Original upload differs from fixed target: ' + key)
            originals[key] = item
        else:
            generated[key] = item
    if originals.keys() != candidates.keys() - skipped or 'manifest.json' not in seen:
        raise ValueError('Original uploads are missing from the plan')
    packages = plan['packages']
    if packages and plan.get('extraction_complete') is not True:
        raise ValueError('All packages must be extracted before publication')
    # Bind the entire extracted upload inventory to verified package bytes, not mutable plan metadata.
    from extract_science import unpack
    expanded = {}
    for package in packages:
        key = package['name'] + '/' + package['resource']['file_name']
        with tempfile.TemporaryDirectory() as temporary:
            inventory = unpack(root / originals[key]['path'], Path(temporary), verify_only=True)
        for item in inventory:
            expanded[extracted_prefix(package['name']) + item['path']] = (item['bytes'], item['sha256'])
    if {key: (item['bytes'], item['sha256']) for key, item in generated.items()} != expanded:
        raise ValueError('Extracted upload inventory differs from verified packages')


def apply(root, plan, s3, output=None, *, case_workers=4, file_workers=8, prepare_cases=False):
    from publication_runner import run
    return run(root, plan, s3, output or root / '.publication',
               case_workers=case_workers, file_workers=file_workers, prepare_cases=prepare_cases)



def main():
    # Failed-jobs-only reruns could reuse a stale checkout; dispatch a fresh main run.
    if int(os.environ.get('GITHUB_RUN_ATTEMPT', '1')) != 1:
        raise ValueError('Native reruns are disabled; use workflow_dispatch on main')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--after')
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--prepare', type=Path)
    modes.add_argument('--dry-run', action='store_true')
    modes.add_argument('--prepare-resources', type=Path)
    parser.add_argument('--output', type=Path)
    modes.add_argument('--apply-plan', type=Path)
    modes.add_argument('--publish-plan', type=Path)
    parser.add_argument('--case-workers', type=int, default=int(os.environ.get('CASE_UPLOAD_WORKERS', '4')))
    parser.add_argument('--file-workers', type=int, default=int(os.environ.get('FILE_UPLOAD_WORKERS', '8')))
    args = parser.parse_args()
    if not (1 <= args.case_workers <= 16 and 1 <= args.file_workers <= 32
            and args.case_workers * args.file_workers <= 64):
        raise ValueError('Workers require 1..16 cases, 1..32 files and at most 64 total transfers')
    root = Path.cwd()
    s3 = S3(os.environ.get('AWS_TARGET_FOLDER', ''))
    if args.prepare_resources:
        if args.output is None:
            raise ValueError('--output is required for resource preparation')
        plan = json.loads(args.prepare_resources.read_text())
        plan = prepare_resources(root, plan, s3, args.output)
        write_artifacts(plan, args.prepare_resources.with_suffix(''))
        args.prepare_resources.write_text(json.dumps(plan) + '\n', encoding='utf-8')
        return
    if args.apply_plan or args.publish_plan:
        if not os.environ.get('AWS_DISTRIBUITION_ID', '').strip():
            raise ValueError('AWS_DISTRIBUITION_ID is required for every publication step')
        path = args.apply_plan or args.publish_plan
        s3.enable_transfers(args.case_workers * args.file_workers)
        apply(root, json.loads(path.read_text()), s3, path.with_suffix(''),
              case_workers=args.case_workers, file_workers=args.file_workers,
              prepare_cases=bool(args.publish_plan))
        return
    plan = prepare(root, s3.read_manifest(), args.after, check_local=False)
    print_plan(plan)
    print('Prepared {} files and {} packages against S3 manifest.json.'.format(
        len(plan['files']), len(plan['packages'])))
    if args.prepare:
        args.prepare.parent.mkdir(parents=True, exist_ok=True)
        write_artifacts(plan, args.prepare.with_suffix(''))
        Reporter(plan, args.prepare.with_suffix(''))
        args.prepare.write_text(json.dumps(plan, ensure_ascii=True) + '\n', encoding='utf-8')
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
                for key, value in {'has_checks': bool(plan['cases']), 'has_uploads': bool(plan['candidates']),
                                   'has_packages': bool(plan['packages']), 'has_manifest': True}.items():
                    stream.write(key + '=' + str(value).lower() + '\n')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('Publish failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
