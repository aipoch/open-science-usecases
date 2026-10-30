import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ordered_replay import build_replay


class OrderedReplayTests(unittest.TestCase):
    def test_complete_ordered_groups_and_safe_compaction(self):
        session = {'version': 2, 'session': {'id': 's', 'projectId': 'p', 'title': 'Replay',
            'createdAt': 1, 'messages': [
                {'id': 'last', 'role': 'assistant', 'content': 'complete ```code```', 'createdAt': 50},
                {'id': 'first', 'role': 'user', 'content': 'question', 'createdAt': 10}],
            'conversationGraph': {'activities': [
                {'id': 'b', 'createdAt': 30, 'title': 'tool'},
                {'id': 'a', 'createdAt': 20, 'title': 'tool'},
                {'id': 'c', 'createdAt': 40, 'updatedAt': 40, 'providerToolName': 'ContextCompaction',
                 'status': 'in_progress', 'rawOutput': 'SECRET'},
                {'id': 'c', 'createdAt': 40, 'updatedAt': 41, 'providerToolName': 'ContextCompaction',
                 'status': 'completed', 'rawInput': 'SECRET', 'title': 'SECRET'}]}}}
        original = copy.deepcopy(session)
        files = build_replay(session, None, 'a' * 64, 'b' * 64)
        index = json.loads(files['index.json'])
        lines = files['blocks.ndjson'].splitlines()
        records = list(map(json.loads, lines))
        self.assertEqual(len(records), 5)
        self.assertEqual(records[1]['messages'][0]['id'], 'first')
        self.assertEqual([a['id'] for a in records[2]['activities']], ['a', 'b'])
        self.assertEqual(records[3]['activities'][0]['status'], 'completed')
        self.assertNotIn(b'SECRET', files['blocks.ndjson'])
        self.assertEqual(records[0]['rowMetadata']['last']['turnFinal'], True)
        self.assertEqual([r['seq'] for r in records[1:]], list(range(4)))
        for line, entry in zip(lines, index['lines']):
            self.assertEqual(entry, {'bytes': len(line), 'sha256': hashlib.sha256(line).hexdigest()})
        self.assertEqual(session, original)
        self.assertEqual(files, build_replay(session, None, 'a' * 64, 'b' * 64))

    def test_cross_repository_golden_contract(self):
        fixture = json.loads(Path(__file__).with_name('ordered-replay.json').read_text())
        source = fixture['source'].encode()
        files = build_replay(json.loads(source), None, 'a' * 64, hashlib.sha256(source).hexdigest())
        self.assertEqual(json.loads(files['index.json']), fixture['index'])
        self.assertEqual(files['blocks.ndjson'].decode(), fixture['stream'])

    def test_nullable_graph_and_empty_elicitation_match_web_semantics(self):
        source = {'version': 2, 'session': {'title': 'Nullable', 'messages': [], 'conversationGraph': None}}
        files = build_replay(source, None, 'a'*64, 'b'*64)
        self.assertEqual(len(files['blocks.ndjson'].splitlines()), 1)
        source['session']['conversationGraph'] = {'activities': [{'id':'ask','createdAt':1,'elicitation':{}}]}
        files = build_replay(source, None, 'a'*64, 'b'*64)
        self.assertEqual(json.loads(files['blocks.ndjson'].splitlines()[1])['kind'], 'elicitation')

    def test_nonstring_optional_linkage_is_ignored_like_web(self):
        source = {'version': 2, 'session': {'title': 'Optional IDs', 'messages': [
            {'id':'m', 'createdAt':1, 'responseToMessageId':{}}],
            'conversationGraph': {'activities': [{'id':'a','createdAt':2,'executionInvocationId':{}}]}}}
        files = build_replay(source, {'runs':[{'executionInvocationId':{}}]}, 'a'*64, 'b'*64)
        self.assertEqual(len(files['blocks.ndjson'].splitlines()), 3)

    def test_notebook_dependencies_and_tool_boundaries(self):
        session = {'version': 2, 'session': {'title': 'Runs', 'messages': [],
            'conversationGraph': {'activities': [
                {'id': 'later', 'createdAt': 3, 'title': 'tool', 'executionInvocationId': 'run-b'},
                {'id': 'plan', 'createdAt': 2, 'providerToolName': 'mcp.open_science_plan.generate_plan'},
                {'id': 'earlier', 'createdAt': 1, 'title': 'tool', 'executionInvocationId': 'run-a'},
                {'id': 'update', 'createdAt': 4, 'providerToolName': 'open-science-plan/update_step_status'}]}}}
        runs = {'workspaceCwd': '/example', 'runs': [
            {'executionInvocationId': 'run-b', 'outputs': ['complete B']},
            {'executionInvocationId': 'run-a', 'outputs': ['complete A']}]}
        records = list(map(json.loads, build_replay(session, runs, 'a'*64, 'b'*64)['blocks.ndjson'].splitlines()))
        self.assertEqual([r['kind'] for r in records[1:]], ['activity-group','plan','activity-group'])
        self.assertEqual(records[1]['runs'], [runs['runs'][1]])
        self.assertEqual(records[3]['runs'], [runs['runs'][0]])
        self.assertEqual(records[0]['runRoots'], {'workspaceCwd': '/example'})

    def test_extraction_and_verify_only_regenerate_identical_sidecars_after_integrity_checks(self):
        import tempfile
        from test_unpack import archive_bytes, declaration
        from extract_science import unpack
        fixture = json.loads(Path(__file__).with_name('ordered-replay.json').read_text())
        files = {'session.json': fixture['source'].encode(), 'records.json': b'{"tables":{}}', 'README.md': b'# Original'}
        inventory = [declaration(name, data) for name, data in files.items()]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / 'case.science'
            package.write_bytes(archive_bytes(files, inventory))
            original = package.read_bytes()
            extracted = root / 'extracted'; extracted.mkdir()
            actual = unpack(package, extracted)
            empty = root / 'verify'; empty.mkdir()
            expected = unpack(package, empty, verify_only=True)
            self.assertEqual(actual, expected)
            derived = [entry for entry in actual if entry['path'].startswith('replay-v1/')]
            self.assertEqual(len(derived), 2)
            self.assertEqual((extracted / 'session.json').read_bytes(), files['session.json'])
            self.assertEqual(package.read_bytes(), original)
            index = next(entry for entry in derived if entry['path'].endswith('index.json'))
            self.assertEqual(json.loads((extracted/index['path']).read_bytes())['archiveSha256'], hashlib.sha256(original).hexdigest())
            inventory[0]['checksum'] = '0' * 64
            package.write_bytes(archive_bytes(files, inventory))
            broken = root/'broken'; broken.mkdir()
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                unpack(package, broken)
            self.assertEqual(list(broken.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
