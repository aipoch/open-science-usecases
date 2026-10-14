"""Compare scheduler limits with fixed fake-S3 latency; this is not an AWS forecast."""
import json
import copy
import time

from test_parallel_publication import ParallelPublicationTests, MemoryS3


def main():
    fixture = ParallelPublicationTests()
    fixture.setUp()
    try:
        plan = fixture.make_plan(count=4, objects=64)
        for cases, files in ((1, 1), (2, 4), (4, 4), (4, 8), (4, 16)):
            store = MemoryS3('[]', latency=.02)
            started = time.monotonic()
            log = fixture.execute(copy.deepcopy(plan), store, case_workers=cases, file_workers=files)
            print(json.dumps({'case_workers': cases, 'file_workers': files,
                              'seconds': round(time.monotonic() - started, 3),
                              'files': len(store.started), 'peak_transfers': store.peak,
                              'console_lines': len(log.splitlines()), 'simulated_latency_ms': 20}))
    finally:
        fixture.doCleanups()

    fixture = ParallelPublicationTests()
    fixture.setUp()
    try:
        # Model the previously omitted CDN wait, including the real coordinator.
        plan = fixture.make_plan(count=12, objects=0)
        for cases in (1, 4):
            store = MemoryS3('[]', latency=0, cdn_latency=.2)
            started = time.monotonic()
            fixture.execute(copy.deepcopy(plan), store, case_workers=cases, file_workers=1)
            print(json.dumps({'scenario': 'cdn-waits', 'case_workers': cases,
                              'seconds': round(time.monotonic() - started, 3),
                              'cases': 12, 'simulated_cdn_latency_ms': 200}))
    finally:
        fixture.doCleanups()


if __name__ == '__main__':
    main()
