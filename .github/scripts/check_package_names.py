#!/usr/bin/env python3
"""Enforce whitespace-free .science filenames without changing legacy S3 parsing."""
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
from urllib.parse import unquote, urlsplit


def naming_errors(entries, tracked_paths=()):
    errors = []
    for entry in entries:
        resource = entry.get('case', {})
        label = str(entry.get('name', '<unnamed>'))
        values = [('case.file_name', resource.get('file_name', '')),
                  ('case.path filename', PurePosixPath(resource.get('path', '')).name)]
        url = resource.get('release_url', '')
        if url:
            values.append(('download filename', unquote(urlsplit(url).path.rsplit('/', 1)[-1])))
        for field, filename in values:
            if any(char.isspace() for char in filename):
                errors.append(f'{label}: {field} contains whitespace; replace spaces with hyphens (-): {filename!r}')
    for path in tracked_paths:
        filename = PurePosixPath(path).name
        if filename.lower().endswith('.science') and any(char.isspace() for char in filename):
            errors.append(f'Tracked package filename contains whitespace: {path!r}')
    return errors


def main():
    root = Path.cwd()
    entries = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    errors = naming_errors(entries, tracked)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(entries)} manifest package filenames and all tracked .science filenames contain no whitespace.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
