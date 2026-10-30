"""Deterministic, optional ordered replay projection; original exports are never mutated."""
import hashlib
import json
import math
import re

FORMAT = 'open-science-replay'
VERSION = 1


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def matches(value, suffix):
    if not isinstance(value, str):
        return False
    name = value.strip().lower()
    parts = re.split(r'__|\.|/', name)
    return ((len(parts) > 1 and parts[-1] == suffix
             and parts[-2].replace('_', '-') == 'open-science-plan')
            or name in ('open-science-plan_' + suffix, 'open_science_plan_' + suffix))


def timestamp(row):
    value = row.get('createdAt')
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError('Replay requires finite timestamps')
    return value


def build_replay(file, run_document, archive_sha256, session_sha256):
    session = file.get('session')
    if not isinstance(session, dict):
        return {}
    messages = session.get('messages', [])
    graph = session.get('conversationGraph') or {}
    if not isinstance(graph, dict) or not isinstance(messages, list):
        return {}
    activities = graph.get('activities') or []
    if not isinstance(activities, list) or (run_document is not None and not isinstance(run_document, dict)):
        return {}
    if run_document and (not isinstance(run_document.get('runs', []), list)
                         or any(not isinstance(run, dict) for run in run_document.get('runs', []))):
        return {}
    # Legacy/incomplete schemas remain publishable through the original replay reader.
    try:
        if file.get('version') != 2 or not isinstance(session.get('title'), str):
            return {}
        seen = set()
        for row in [*messages, *activities]:
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
                return {}
            timestamp(row)
        for message in messages:
            if message['id'] in seen:
                return {}
            seen.add(message['id'])
    except (ValueError, TypeError, AttributeError):
        return {}
    timeline = [(timestamp(m), 'message', m) for m in messages]
    compact = {}
    for activity in activities:
        sort = activity.get('sortIndex')
        ts = sort if type(sort) in (int, float) and math.isfinite(sort) and sort > 1_000_000_000_000 else timestamp(activity)
        if activity.get('providerToolName') == 'ContextCompaction':
            updated = activity.get('updatedAt')
            updated = updated if type(updated) in (int, float) and math.isfinite(updated) else ts
            old = compact.get(activity['id'])
            if old is None or updated >= old[0]:
                status = activity.get('status')
                if status == 'completed' and str(activity.get('title', '')).strip() == 'Context compaction cancelled':
                    status = 'cancelled'
                # No arbitrary title, errors, payloads or provider metadata leave this boundary.
                safe = {key: activity[key] for key in ('id', 'createdAt', 'providerToolName')}
                safe.update(status=status if status in ('completed', 'in_progress', 'failed', 'cancelled') else 'unknown', sortIndex=ts)
                compact[activity['id']] = (updated, ts, safe)
            continue
        names = (activity.get('providerToolName'), activity.get('title'))
        if any(matches(name, 'update_step_status') for name in names):
            continue
        kind = ('elicitation' if isinstance(activity.get('elicitation'), (dict, list)) or activity.get('elicitation') else
                'plan' if any(matches(name, 'generate_plan') for name in names) else 'activity-group')
        timeline.append((ts, kind, activity))
    # Same stable tie order as Web: messages, noncompact activities, compact insertion order.
    timeline.extend((ts, 'compaction', value) for _, ts, value in compact.values())
    timeline.sort(key=lambda item: item[0])
    blocks = []
    for _, kind, value in timeline:
        if kind == 'activity-group' and blocks and blocks[-1]['kind'] == kind:
            blocks[-1]['activities'].append(value)
        else:
            blocks.append({'seq': len(blocks), 'kind': kind,
                           'messages': [value] if kind == 'message' else [],
                           'activities': [] if kind == 'message' else [value]})
    if len({b['messages'][0]['id'] if b['messages'] else b['activities'][0]['id'] for b in blocks}) != len(blocks):
        return {}
    ordered_messages = [value for _, kind, value in timeline if kind == 'message']
    markers = {m['id']: {'turnFinal': False} for m in messages}
    last = None
    for message in ordered_messages:
        if message.get('role') == 'user':
            if last is not None:
                markers[last]['turnFinal'] = True
            last = None
        else:
            last = message['id']
            target = message.get('responseToMessageId')
            if isinstance(target, str) and target in markers:
                markers[target]['reviewerState'] = 'completed' if message.get('status', 'complete') == 'complete' else 'failed'
    if last is not None:
        markers[last]['turnFinal'] = True
    roots = {key: run_document[key] for key in ('notebookSessionRoot', 'dataRoot', 'workspaceCwd')
             if run_document and key in run_document}
    runs = (run_document or {}).get('runs', [])
    header = {'type': 'header', 'session': {key: session[key] for key in (
        'id', 'projectId', 'revision', 'title', 'description', 'projectName', 'createdAt',
        'updatedAt', 'cwd', 'artifacts') if key in session},
        'runRoots': roots, 'rowMetadata': markers,
        'uploadMessages': [{'uploads': m['uploads']} for m in messages if isinstance(m.get('uploads'), list)]}
    lines = [encoded(header)]
    for block in blocks:
        invocations = {a['executionInvocationId'] for a in block['activities'] if isinstance(a.get('executionInvocationId'), str)}
        block['runs'] = [r for r in runs if isinstance(r.get('executionInvocationId'), str) and r['executionInvocationId'] in invocations]
        block['type'] = 'block'
        lines.append(encoded(block))
    index = {'format': FORMAT, 'version': VERSION, 'archiveSha256': archive_sha256,
             'sessionSha256': session_sha256,
             'lines': [{'bytes': len(line), 'sha256': hashlib.sha256(line).hexdigest()} for line in lines]}
    index_bytes = encoded(index)
    if (len(index_bytes) > 4 * 1024 ** 2 or any(len(line) > 128 * 1024 ** 2 for line in lines)
            or sum(len(line) + 1 for line in lines) > 256 * 1024 ** 2):
        return {}
    return {'index.json': index_bytes, 'blocks.ndjson': b'\n'.join(lines) + b'\n'}
