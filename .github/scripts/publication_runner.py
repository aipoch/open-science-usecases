"""Bounded case workers; only the coordinator may commit the shared index."""
import copy
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import subprocess
import threading
import time

from check_structure import source_errors, validate_head_size
from publication_steps import (Reporter, encoded, digest, print_plan, write_artifacts,
                               step_directory, atomic_json, checkpoint_entries)


def step_names(step):
    if step['operation'] == 'UPDATE_CATALOG':
        return {entry['name'] for entry in step['before'] + step['after']}
    return {step['name']} if step['name'] else set()


def next_manifest(baseline, step):
    """Apply only this successful operation, never an earlier failed operation."""
    from publish import read_manifest
    current = read_manifest(baseline, 'accepted checkpoint') if baseline else []
    if step['operation'] == 'FINAL_SYNC':
        return step['manifest']
    text = encoded(checkpoint_entries(current, step))
    read_manifest(text, 'next checkpoint')  # Preserve global catalog and legacy-baseline invariants.
    return text


def upload_files(root, files, s3, step, state, reporter, workers, stop):
    """Bound the pending window too; drain in-flight requests on failure."""
    iterator = iter(files)
    failed = None
    executor = ThreadPoolExecutor(max_workers=workers)
    pending = {}

    def transfer(item, file_state):
        if stop.is_set():
            raise RuntimeError('Publication stopped before upload')
        started = time.monotonic()
        reporter.update(file_state, status='uploading')
        reporter.event(step, 'file', 'uploading', **item)
        try:
            s3.upload(root / item['path'], item['key'])
            s3.verify_upload(item['key'], item['bytes'], item['sha256'])
        except Exception as error:
            reporter.update(file_state, status='failed', error=str(error))
            reporter.event(step, 'file', 'failed', key=item['key'], error=str(error))
            raise
        reporter.update(file_state, status='completed')
        reporter.event(step, 'file', 'completed', key=item['key'],
                       elapsed_seconds=round(time.monotonic() - started, 3))

    def submit():
        item = next(iterator, None)
        if item is not None:
            pending[executor.submit(transfer, *item)] = item

    try:
        for _ in range(workers):
            submit()
        while pending:
            done, _ = wait(pending, timeout=1, return_when=FIRST_COMPLETED)
            reporter.progress()
            for future in done:
                pending.pop(future)
                try:
                    future.result()
                except Exception as error:
                    failed = failed or error
            if failed or stop.is_set():
                for future in pending:
                    future.cancel()
                break
            for _ in done:
                submit()
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
    if failed:
        raise failed
    if stop.is_set():
        raise RuntimeError('Publication stopped during upload')


def resource_step(root, source_plan, step, state, s3, reporter, workers, stop, prepare_cases):
    from publish import scope_plan, prepare_resources, validate_prepared
    from extract_science import expand_plan
    started = time.monotonic()
    phase = 'preparation' if prepare_cases else 'files'
    try:
        if stop.is_set():
            raise RuntimeError('Publication stopped before case preparation')
        reporter.update(state, status='preparing' if prepare_cases else 'uploading')
        reporter.event(step, 'step', state['status'])
        if prepare_cases:
            names = step_names(step)
            scoped = scope_plan(source_plan, names)
            for case in scoped['cases']:
                entry = case['entry']
                errors = source_errors(root, entry)
                for kind in ('cover', 'case', 'introduction'):
                    item = entry[kind]
                    if item['release_url']:
                        validate_head_size(item['release_url'], item['bytes'], entry['name'] + '/' + kind, errors)
                if errors:
                    raise ValueError('; '.join(errors))
            directory = reporter.output.parent / (reporter.output.name + '-staging') / str(step['id'])
            scoped = prepare_resources(root, scoped, s3, directory / 'sources', names=names, check_local=False)
            phase = 'extraction'
            scoped = expand_plan(root, scoped, directory / 'extracted', names=names, check_local=False)
            phase = 'verification'
            validate_prepared(root, scoped, s3, names=names, check_local=False)
            files = [item for item in scoped['files'] if item['key'] != 'manifest.json']
            reporter.ready(step, state, files, scoped['packages'])
            atomic_json(step_directory(reporter.output, step) / 'resource-decisions.json', scoped['decisions'])
        phase = 'files'
        reporter.update(state, status='uploading')
        reporter.event(step, 'files', 'uploading', file_count=len(step['files']),
                       bytes=sum(f['bytes'] for f in step['files']), workers=workers)
        by_case = {}
        for item, file_state in zip(step['files'], state['files']):
            by_case.setdefault(item['key'].split('/', 1)[0], []).append((item, file_state))
        packages = {package['name'] for package in step['packages']}
        # Dependent catalog groups retain case-by-case cleanup and one manifest commit.
        for name, files in by_case.items():
            if stop.is_set():
                raise RuntimeError('Publication stopped before case writes')
            if name in packages:
                reporter.event(step, 'clear_extracted', 'uploading', name=name)
                s3.clear_extracted(name)
                reporter.event(step, 'clear_extracted', 'completed', name=name)
            upload_files(root, files, s3, step, state, reporter, workers, stop)
        reporter.update(state, status='ready')
        reporter.event(step, 'resources', 'completed')
    except Exception as error:
        reporter.update(state, status='failed', failed_phase=phase, error=str(error))
        reporter.event(step, phase, 'failed', error=str(error), detail=getattr(error, 'stderr', None))
        raise
    finally:
        reporter.update(state, elapsed_seconds=round(time.monotonic() - started, 3))


def commit_step(step, state, baseline, s3, reporter):
    if s3.read_manifest() != baseline:
        raise ValueError('S3 manifest changed since preparation; dispatch a fresh run')
    text = next_manifest(baseline, step)
    path = step_directory(reporter.output, step) / 'applied-manifest.json'
    path.write_text(text, encoding='utf-8')
    reporter.event(step, 'manifest', 'uploading', sha256=digest(text))
    try:
        s3.commit_manifest(path)
        reporter.update(state, manifest_committed=True)
        reporter.event(step, 'manifest', 'accepted')
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or '').lower()
        if not any(message in detail for message in (
                'timeout', 'timed out', 'connection was closed', 'connection reset', 'connection aborted')):
            raise
        reporter.update(state, manifest_committed=None)
        reporter.event(step, 'manifest', 'unknown')
        if s3.read_manifest() != text:
            raise
        reporter.update(state, manifest_committed=True)
        reporter.event(step, 'manifest', 'accepted')
    if s3.read_manifest() != text:
        raise ValueError('Published manifest read-back mismatch')
    reporter.update(state, manifest_verified=True)
    reporter.event(step, 'manifest', 'completed')
    return text


def finish_step(step, state, baseline, s3, reporter, failures):
    started = time.monotonic()
    # A shared-index error is fatal, unlike a case-local resource/CDN error.
    try:
        baseline = commit_step(step, state, baseline, s3, reporter)
    except Exception as error:
        reporter.update(state, status='failed', failed_phase='manifest', error=str(error))
        reporter.event(step, 'manifest', 'failed', error=str(error), detail=getattr(error, 'stderr', None))
        raise
    reporter.update(state, cdn='uploading')
    reporter.event(step, 'cdn', 'uploading')
    cdn_errors = []
    for name in sorted({item['key'].split('/', 1)[0] for item in step['files']}) or [None]:
        try:
            s3.refresh_cdn(name)
        except Exception as error:
            cdn_errors.append(error)
            reporter.event(step, 'cdn', 'failed', name=name, error=str(error))
    reporter.update(state, elapsed_seconds=round(state.get('elapsed_seconds', 0) + time.monotonic() - started, 3))
    if cdn_errors:
        reporter.update(state, status='failed', cdn='failed', failed_phase='cdn', error=str(cdn_errors[0]))
        failures.extend(cdn_errors)
    else:
        reporter.update(state, status='completed', cdn='completed')
        reporter.event(step, 'step', 'completed')
    return baseline


def run(root, plan, s3, output, *, case_workers=4, file_workers=8, prepare_cases=False):
    from publish import verify_plan, validate_prepared
    if not (1 <= case_workers <= 16 and 1 <= file_workers <= 32 and case_workers * file_workers <= 64):
        raise ValueError('Invalid publication concurrency; maximum total is 64')
    expected = verify_plan(root, plan, check_local=not prepare_cases)
    if prepare_cases:
        if plan['files'] != expected['files'] or plan.get('resources_prepared'):
            raise ValueError('Case preparation requires a fresh plan')
    else:
        validate_prepared(root, plan, s3)
    if s3.read_manifest() != plan['baseline']:
        raise ValueError('S3 manifest changed since preparation; dispatch a fresh run')
    source_plan = copy.deepcopy(plan)
    write_artifacts(plan, output)
    reporter = Reporter(plan, output)
    print_plan(plan)
    print('Concurrency: {} cases x {} files = {} transfers maximum'.format(
        case_workers, file_workers, case_workers * file_workers), flush=True)
    pairs = list(zip(plan['steps'], reporter.state['steps']))
    resource_steps = iter((step, state) for step, state in pairs if step['operation'] not in ('REORDER', 'FINAL_SYNC'))
    baseline, failures = plan['baseline'], []
    stop = threading.Event()
    executor = ThreadPoolExecutor(max_workers=case_workers)
    pending = {}

    def submit():
        pair = next(resource_steps, None)
        if pair is not None:
            future = executor.submit(resource_step, root, source_plan, *pair, s3, reporter,
                                     file_workers, stop, prepare_cases)
            pending[future] = pair

    try:
        for _ in range(case_workers):
            submit()
        while pending:
            done, _ = wait(pending, timeout=1, return_when=FIRST_COMPLETED)
            reporter.progress()
            for future in sorted(done, key=lambda f: pending[f][0]['id']):
                step, state = pending.pop(future)
                try:
                    future.result()
                except Exception as error:
                    failures.append(error)
                else:
                    baseline = finish_step(step, state, baseline, s3, reporter, failures)
                submit()
        complete_index = all(state['manifest_verified'] for step, state in pairs
                             if step['operation'] not in ('REORDER', 'FINAL_SYNC'))
        for step, state in pairs:
            if step['operation'] in ('REORDER', 'FINAL_SYNC'):
                if not complete_index:
                    reporter.update(state, status='skipped')
                    reporter.event(step, 'step', 'skipped', reason='Failed cases are excluded from the index')
                    continue
                reporter.update(state, status='uploading')
                baseline = finish_step(step, state, baseline, s3, reporter, failures)
        if failures:
            raise failures[0]
    finally:
        stop.set()
        executor.shutdown(wait=True, cancel_futures=True)
        reporter.summary()
