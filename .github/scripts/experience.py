"""Validate and publish a case's optional, Git-backed interactive experience."""
from functools import lru_cache
import hashlib
import re
import subprocess

from manifest_diff import git


def safe_path(path):
    return (isinstance(path, str) and not re.search(r'[\\\x00-\x1f\x7f]', path)
            and all(part not in ('', '.', '..') and not re.match(r'^[A-Za-z]:', part)
                    for part in path.split('/')))


def declaration_errors(entry):
    if 'experience' not in entry:
        return []
    value = entry['experience']
    if not isinstance(value, dict) or set(value) != {'path', 'revision'}:
        return ['experience requires path and revision']
    path = value['path']
    if (not safe_path(path) or path.split('/')[-1] != 'experience'
            or (entry.get('catalog') and path.split('/')[0] != entry['catalog'])):
        return ['experience.path must select a safe experience directory within the case catalog']
    if not isinstance(value['revision'], str) or not re.fullmatch(r'[0-9a-f]{40}', value['revision']):
        return ['experience.revision must be the full Git tree ID']
    return []


@lru_cache(maxsize=1024)
def tree_files(root, commit, path, revision):
    from check_structure import read_json, allowed_release_url
    from extract_science import check_layout
    # Literal paths and NUL delimiters preserve Unicode, whitespace and nested filenames.
    listing = git(root, '--literal-pathspecs', 'ls-tree', '-z', commit, '--', path)
    if listing.partition('\t')[0] != '040000 tree ' + revision:
        raise ValueError(f'{path}: update experience.revision to match the committed directory')
    files, downloads = [], {}
    for line in git(root, 'ls-tree', '-rlz', revision).split('\0'):
        if not line:
            continue
        header, name = line.split('\t', 1)
        mode, kind, blob, size = header.split()
        if mode not in ('100644', '100755') or kind != 'blob' or not safe_path(name):
            raise ValueError(f'{path}: invalid experience file {name!r}')
        if name == '.experience-sources.json':
            downloads = read_json(git(root, 'cat-file', 'blob', blob), path + '/' + name)
            if not isinstance(downloads, dict):
                raise ValueError(f'{path}: .experience-sources.json must map paths to resources')
            for target, resource in downloads.items():
                if (not safe_path(target) or not isinstance(resource, dict)
                        or set(resource) != {'release_url', 'bytes', 'sha256'}
                        or not allowed_release_url(resource['release_url'])
                        or type(resource['bytes']) is not int or resource['bytes'] < 0
                        or not isinstance(resource['sha256'], str)
                        or not re.fullmatch(r'[0-9a-f]{64}', resource['sha256'])):
                    raise ValueError(f'{path}: invalid experience source for {target!r}')
        else:
            files.append((name, blob, int(size)))
    if not any(name == 'index.html' and size > 0 for name, _, size in files):
        raise ValueError(f'{path}: a nonempty index.html is required')
    check_layout([(name, False) for name in
                  ['.experience-sources.json', *(name for name, _, _ in files), *downloads]])
    return files, downloads


@lru_cache(maxsize=4096)
def blob_sha256(root, blob):
    with subprocess.Popen(['git', 'cat-file', 'blob', blob], cwd=root, stdout=subprocess.PIPE) as process:
        checksum = hashlib.file_digest(process.stdout, 'sha256').hexdigest()
        if process.wait():
            raise ValueError('Cannot read experience Git blob ' + blob)
    return checksum


def candidates(root, commit, entry, previous):
    value = entry.get('experience')
    if value is None or value == previous.get('experience'):
        return []
    path, revision = value['path'], value['revision']
    files, downloads = tree_files(root, commit, path, revision)
    if previous.get('experience', {}).get('revision') == revision:
        return []
    name = entry['name']
    resources = {relative: {'sha256': blob_sha256(root, blob), 'bytes': size, 'release_url': ''}
                 for relative, blob, size in files}
    resources.update(downloads)
    return [{'name': name, 'kind': 'experience', 'path': f'{path}/{relative}',
             'key': f'{name}/experience/{revision}/{relative}', **resource,
             'reasons': ['experience revision'], 'force_upload': False}
            for relative, resource in resources.items()]
