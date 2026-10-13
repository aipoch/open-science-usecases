"""Case-sized manifest checkpoints and their reviewable execution evidence."""
import copy
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time

from check_structure import catalog_errors


def encoded(value):
    return json.dumps(value, ensure_ascii=True, indent=2) + '\n'


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def build_steps(old, new, target_text):
    """Only case operations change entries; ordering and exact bytes have explicit steps."""
    current = copy.deepcopy(old)
    previous = {entry['name']: entry for entry in old}
    steps = []
    pending = []
    checkpoint = copy.deepcopy(old)

    def append(operation, name=None, before=None, after=None):
        nonlocal checkpoint
        pending.append(name)
        # A shared catalog rename can collide until its last case is updated/removed.
        if catalog_errors(current, legacy=True):
            return
        if len(pending) > 1:
            operation, name = 'UPDATE_CATALOG', None
            before = [entry for entry in checkpoint if entry['name'] in pending]
            after = [entry for entry in current if entry['name'] in pending]
        steps.append({'id': len(steps) + 1, 'operation': operation, 'name': name,
                      'before': copy.deepcopy(before), 'after': copy.deepcopy(after),
                      'manifest': encoded(current), 'files': [], 'packages': []})
        checkpoint = copy.deepcopy(current)
        pending.clear()

    # Reverse insertion retains the repository's relative order within the new head group.
    for entry in reversed([entry for entry in new if entry['name'] not in previous]):
        current.insert(0, copy.deepcopy(entry))
        append('ADD_CASE', entry['name'], after=entry)
    for entry in new:
        name = entry['name']
        if name in previous and entry != previous[name]:
            index = next(i for i, item in enumerate(current) if item['name'] == name)
            current[index] = copy.deepcopy(entry)
            append('UPDATE_CASE', name, previous[name], entry)
    desired = {entry['name'] for entry in new}
    for entry in old:
        if entry['name'] not in desired:
            current = [item for item in current if item['name'] != entry['name']]
            append('REMOVE_CASE', entry['name'], before=entry)
    if [entry['name'] for entry in current] != [entry['name'] for entry in new]:
        before = [entry['name'] for entry in current]
        current = copy.deepcopy(new)
        append('REORDER', before=before, after=[entry['name'] for entry in new])
    append('FINAL_SYNC')
    if pending:
        raise ValueError('Cannot build publication checkpoints with invalid catalogs')
    steps[-1]['manifest'] = target_text  # Preserve the fixed commit's bytes, even on a no-op run.
    return steps


def group_files(plan):
    """Attach originals and expanded archive files to the same case checkpoint."""
    for step in plan['steps']:
        # Rebuild execution lists exclusively from the validated plan inventory.
        step['files'] = []
        step['packages'] = []
        if step['operation'] in ('ADD_CASE', 'UPDATE_CASE', 'UPDATE_CATALOG'):
            names = ({entry['name'] for entry in step['after']} if step['operation'] == 'UPDATE_CATALOG'
                     else {step['name']})
            step['files'] = [item for item in plan['files']
                             if item['key'].split('/', 1)[0] in names]
            step['packages'] = [item for item in plan['packages'] if item['name'] in names]
    return plan


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(encoded(value), encoding='utf-8')
    temporary.replace(path)


def write_artifacts(plan, output):
    output.mkdir(parents=True, exist_ok=True)
    (output / 'baseline-manifest.json').write_text(plan['baseline'] or '[]', encoding='utf-8')
    for step in plan['steps']:
        directory = output / 'steps' / ('%03d-%s' % (step['id'], step['name'] or step['operation'].lower()))
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'manifest.json').write_text(step['manifest'], encoding='utf-8')
        atomic_json(directory / 'files.json', step['files'])
        atomic_json(directory / 'entry-before.json', step['before'])
        atomic_json(directory / 'entry-after.json', step['after'])
    atomic_json(output / 'plan.json', plan)


def print_plan(plan):
    print('Publication target: ' + plan['after'], flush=True)
    print('Step counts: ' + json.dumps(Counter(step['operation'] for step in plan['steps'])), flush=True)
    for item in plan.get('candidates', []):
        print('Candidate: ' + json.dumps(item, ensure_ascii=True), flush=True)
    for decision in plan.get('decisions', []):
        print('Target decision: ' + json.dumps(decision, ensure_ascii=True), flush=True)
    for name in plan.get('unchanged', []):
        print('[skipped] ' + name + ': declaration matches S3', flush=True)
    print('Extraction ready: ' + str(plan.get('extraction_complete', not plan['packages'])), flush=True)
    for step in plan['steps']:
        print('::group::Step {id} {operation} {name}'.format(**step), flush=True)
        print('[waiting] manifest sha256=' + digest(step['manifest']), flush=True)
        print('Before: ' + encoded(step['before']), flush=True)
        print('After: ' + encoded(step['after']), flush=True)
        if not step['files']:
            print('No resource uploads in this step.', flush=True)
        for item in step['files']:
            print('Upload: ' + json.dumps(item, ensure_ascii=True), flush=True)
        for package in step['packages']:
            print('Replace extracted prefix: ' + package['name'] + '/extracted/', flush=True)
        print('::endgroup::', flush=True)


class Reporter:
    """Durable statuses distinguish a committed manifest from a failed CDN refresh."""
    def __init__(self, plan, output):
        self.output = output
        self.started = time.monotonic()
        self.state = {'after': plan['after'], 'steps': [
            {'id': s['id'], 'operation': s['operation'], 'name': s['name'], 'status': 'waiting',
             'manifest_committed': False, 'manifest_verified': False, 'cdn': 'waiting',
             'files': [{'key': f['key'], 'status': 'waiting'} for f in s['files']]}
            for s in plan['steps']]}
        atomic_json(output / 'status.json', self.state)
        (output / 'events.jsonl').write_text('', encoding='utf-8')

    def event(self, step, phase, status, **details):
        record = {'time': datetime.now(timezone.utc).isoformat(), 'step': step['id'],
                  'phase': phase, 'status': status, **details}
        print(json.dumps(record, ensure_ascii=True), flush=True)
        with (self.output / 'events.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(record, ensure_ascii=True) + '\n')
        atomic_json(self.output / 'status.json', self.state)

    def summary(self):
        rows = ['### Case publication', '', '| Step | Operation | Case | Status | Manifest accepted | Read-back verified | CDN |',
                '| --- | --- | --- | --- | --- | --- | --- |']
        for s in self.state['steps']:
            rows.append('| {id} | {operation} | {name} | {status} | {manifest_committed} | {manifest_verified} | {cdn} |'.format(**s))
        rows.extend(['', 'Elapsed: %.1fs' % (time.monotonic() - self.started), ''])
        text = '\n'.join(rows)
        (self.output / 'summary.md').write_text(text, encoding='utf-8')
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as stream:
                stream.write(text)
