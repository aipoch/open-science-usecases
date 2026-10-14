"""Case-sized manifest checkpoints and their reviewable execution evidence."""
import copy
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
import time
import threading

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

    def append(operation, name=None, before=None, after=None):
        # Build primitive operations first. Group only actual catalog dependencies below.
        steps.append({'id': len(steps) + 1, 'operation': operation, 'name': name,
                      'before': copy.deepcopy(before), 'after': copy.deepcopy(after),
                      'manifest': encoded(current), 'files': [], 'packages': []})

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
    steps[-1]['manifest'] = target_text  # Preserve the fixed commit's bytes, even on a no-op run.
    return independent_catalog_steps(old, new, steps, target_text)


def checkpoint_entries(current, step):
    """Apply one operation to the actually accepted entries."""
    operation = step['operation']
    if operation == 'REORDER':
        by_name = {entry['name']: entry for entry in current}
        return [by_name[name] for name in step['after']]
    if operation == 'ADD_CASE':
        return [step['after'], *current]
    if operation == 'UPDATE_CASE':
        return [step['after'] if entry['name'] == step['name'] else entry for entry in current]
    if operation == 'REMOVE_CASE':
        return [entry for entry in current if entry['name'] != step['name']]
    if operation == 'UPDATE_CATALOG':
        replacements = {entry['name']: entry for entry in step['after']}
        names = {entry['name'] for entry in step['before'] + step['after']}
        seen = {entry['name'] for entry in current}
        return ([entry for entry in step['after'] if entry['name'] not in seen] +
                [replacements.get(entry['name'], entry) for entry in current
                 if entry['name'] not in names or entry['name'] in replacements])
    return current


def independent_catalog_steps(old, new, steps, target_text):
    """Coalesce identifier release/reuse dependencies before allowing completion-order commits."""
    old_labels = {e['catalog_name']: e['catalog'] for e in old if e.get('catalog_name')}
    new_labels = {e['catalog_name']: e['catalog'] for e in new if e.get('catalog_name')}
    changed_labels = {key for key in old_labels.keys() & new_labels.keys()
                      if old_labels[key] != new_labels[key]}
    if not changed_labels:
        return steps
    groups = [{i} for i, s in enumerate(steps) if s['operation'] not in ('REORDER', 'FINAL_SYNC')]
    owners = {}
    for i, step in enumerate(steps):
        names = ({e['name'] for e in step['before'] + step['after']}
                 if step['operation'] == 'UPDATE_CATALOG' else {step['name']})
        owners.update({name: i for name in names if name})
    for identifier in changed_labels:
        involved = {owners[e['name']] for e in old + new
                    if e.get('catalog_name') == identifier and e['name'] in owners}
        merged = set().union(*(group for group in groups if group & involved))
        groups = [group for group in groups if not group & involved] + [merged]
    result, current = [], copy.deepcopy(old)
    for group in sorted(groups, key=min):
        if len(group) == 1:
            step = copy.deepcopy(steps[next(iter(group))])
        else:
            names = {name for name, owner in owners.items() if owner in group}
            step = {'operation': 'UPDATE_CATALOG', 'name': None,
                    'before': [e for e in old if e['name'] in names],
                    'after': [e for e in new if e['name'] in names], 'files': [], 'packages': []}
        current = checkpoint_entries(current, step)
        if catalog_errors(current, legacy=True):
            raise ValueError('Cannot build independent catalog checkpoints')
        step.update(id=len(result) + 1, manifest=encoded(current))
        result.append(step)
    for original in steps:
        if original['operation'] in ('REORDER', 'FINAL_SYNC'):
            step = copy.deepcopy(original)
            current = checkpoint_entries(current, step)
            step.update(id=len(result) + 1,
                        manifest=target_text if step['operation'] == 'FINAL_SYNC' else encoded(current))
            result.append(step)
    return result


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
    print('Candidates: {}; packages: {}; unchanged cases: {}'.format(
        len(plan['candidates']), len(plan['packages']), len(plan.get('unchanged', []))), flush=True)
    print('[waiting] Full manifests, decisions and file lists are saved in the publication artifact.', flush=True)


def step_directory(output, step):
    return output / 'steps' / ('%03d-%s' % (step['id'], step['name'] or step['operation'].lower()))


class Reporter:
    """Serialize evidence writes; file events are journaled, snapshots are rate limited."""
    def __init__(self, plan, output):
        self.output = output
        self.started = time.monotonic()
        self.last_snapshot = self.last_progress = self.started
        self.lock = threading.RLock()
        self.state = {'after': plan['after'], 'steps': [
            {'id': s['id'], 'operation': s['operation'], 'name': s['name'], 'status': 'waiting',
             'manifest_committed': False, 'manifest_verified': False, 'cdn': 'waiting',
             'files': [{'key': f['key'], 'status': 'waiting', 'bytes': f.get('bytes', 0)} for f in s['files']]}
            for s in plan['steps']]}
        atomic_json(output / 'status.json', self.state)
        (output / 'events.jsonl').write_text('', encoding='utf-8')

    def update(self, state, **fields):
        with self.lock:
            state.update(fields)

    def event(self, step, phase, status, **details):
        record = {'time': datetime.now(timezone.utc).isoformat(), 'step': step['id'],
                  'phase': phase, 'status': status, **details}
        with self.lock:
            with (self.output / 'events.jsonl').open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(record, ensure_ascii=True) + '\n')
            if phase != 'file' or status == 'failed':
                label = step['name'] or step['operation']
                detail = json.dumps(details.get('error', ''), ensure_ascii=True) if status == 'failed' else ''
                if phase == 'files' and status == 'uploading':
                    detail = '{} files, {} bytes, {} file workers'.format(
                        details['file_count'], details['bytes'], details['workers'])
                # JSON escaping keeps untrusted error text from injecting Actions commands.
                print('[{}] {}: {} (step {}){}'.format(label, phase, status, step['id'],
                      ' — ' + detail if detail else ''), flush=True)
            now = time.monotonic()
            if phase != 'file' or status == 'failed' or now - self.last_snapshot >= 5:
                atomic_json(self.output / 'status.json', self.state)
                self.last_snapshot = now

    def ready(self, step, state, files, packages):
        with self.lock:
            step['files'], step['packages'] = files, packages
            state['files'] = [{'key': item['key'], 'status': 'waiting', 'bytes': item['bytes']} for item in files]
            atomic_json(step_directory(self.output, step) / 'files.json', files)

    def progress(self):
        with self.lock:
            now = time.monotonic()
            if now - self.last_progress < 10:
                return
            self.last_progress = now
            for state in self.state['steps']:
                if state['status'] in ('preparing', 'uploading', 'ready'):
                    done = sum(f['status'] == 'completed' for f in state['files'])
                    print('[progress] {}: {} {}/{} files'.format(
                        state['name'] or state['operation'], state['status'], done, len(state['files'])), flush=True)
            atomic_json(self.output / 'status.json', self.state)

    def summary(self):
        with self.lock:
            atomic_json(self.output / 'status.json', self.state)
            rows = ['### Case publication', '',
                    '| Step | Case / operation | Status | Files verified | Bytes verified | Seconds | Manifest accepted / verified | CDN |',
                    '| --- | --- | --- | --- | --- | --- | --- | --- |']
            for s in self.state['steps']:
                done = [f for f in s['files'] if f['status'] == 'completed']
                rows.append('| {} | {} | {} | {}/{} | {} | {} | {} / {} | {} |'.format(
                    s['id'], s['name'] or s['operation'], s['status'], len(done), len(s['files']),
                    sum(f.get('bytes', 0) for f in done), s.get('elapsed_seconds', ''),
                    s['manifest_committed'], s['manifest_verified'], s['cdn']))
            rows.extend(['', 'Results: ' + str(dict(Counter(s['status'] for s in self.state['steps']))),
                         '', 'Elapsed: %.1fs' % (time.monotonic() - self.started),
                         '', 'See the publication artifact for per-file events and failure details.', ''])
            text = '\n'.join(rows)
            (self.output / 'summary.md').write_text(text, encoding='utf-8')
            if os.environ.get('GITHUB_STEP_SUMMARY'):
                with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as stream:
                    stream.write(text)
