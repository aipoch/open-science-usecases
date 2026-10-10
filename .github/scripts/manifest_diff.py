"""Git/manifest metadata shared by checking and publication; never hash resource bytes."""
import json
from collections import Counter
import re
import subprocess

SHA = re.compile(r'[0-9a-f]{40}')


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.PIPE).decode('utf-8')


def ancestor(root, older, newer):
    result = subprocess.run(['git', 'merge-base', '--is-ancestor', older, newer], cwd=root,
                            capture_output=True, text=True)
    if result.returncode not in (0, 1):
        raise ValueError('Cannot determine commit ancestry: ' + result.stderr.strip())
    return result.returncode == 0


def commit_exists(root, sha):
    if not isinstance(sha, str) or not SHA.fullmatch(sha) or sha == '0' * 40:
        raise ValueError('A nonzero full commit SHA is required; no full-sync fallback')
    git(root, 'cat-file', '-e', sha + '^{commit}')


def validate_range(root, before, after):
    for sha in (before, after):
        commit_exists(root, sha)
    if git(root, 'rev-parse', 'HEAD').strip() != after:
        raise ValueError('Checkout must match the fixed target commit')
    if not ancestor(root, before, after):
        raise ValueError('Unsupported history: before must be an ancestor of after')


def manifests(root, before, after):
    validate_range(root, before, after)
    # An absent/invalid baseline manifest is an error, never an empty/full-sync baseline.
    old = git(root, 'show', before + ':manifest.json')
    new = git(root, 'show', after + ':manifest.json')
    return json.loads(old), json.loads(new), old != new


def changed_entries(old, new):
    # Ignore formatting/order and removed entries, but detect duplicate-count changes.
    # Canonical JSON also keeps booleans distinct from numeric metadata.
    previous = Counter(json.dumps(entry, sort_keys=True) for entry in old)
    current = Counter(json.dumps(entry, sort_keys=True) for entry in new)
    return [entry for entry in new
            if previous[json.dumps(entry, sort_keys=True)] != current[json.dumps(entry, sort_keys=True)]]


def local_resources(entries):
    resources = {}
    for case in entries:
        for kind in ('cover', 'case', 'introduction'):
            resource = case.get(kind)
            if resource is None:
                # Some untouched legacy cases predate required introductions.
                # Completeness of affected entries belongs to the structure check.
                continue
            if kind == 'case' and resource.get('release_url'):
                continue
            key = case['name'] + '/' + resource['file_name']
            if key in resources:
                raise ValueError('Duplicate upload destination: ' + key)
            resources[key] = resource
    return resources
