"""Synthetic deterministic controls. Acceptance records are fixtures, not model proof."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import planning


def program_fixture(root):
    (root / 'bar').mkdir(exist_ok=True)
    (root / 'bar' / 'reference.txt').write_text('Frozen acceptance reference\n')
    (root / 'bar' / 'questions.json').write_text('["What is supported?"]\n')
    ref = lambda name: {'path': name, 'sha256': hashlib.sha256((root / name).read_bytes()).hexdigest()}
    tasks = []
    for ident, deps in [('A', []), ('B', ['A']), ('C', ['A']), ('D', ['B', 'C'])]:
        tasks.append({'id': ident, 'objective': 'Produce ' + ident,
                      'builder_charter': 'Edit the owned file only', 'critic_charter': 'Inspect actual output',
                      'critic': 'independent reviewer', 'dependencies': deps,
                      'write_targets': ['src/' + ident + '.txt'], 'acceptance_criteria': ['Matches reference'],
                      'evidence_required': ['Actual output'], 'stop_conditions': ['User stop'], 'max_critic_rounds': 2})
    return {'goal': 'Synthetic dependency contract', 'budget': {
        'max_elapsed_minutes': 60, 'max_agent_launches': 20, 'max_concurrency': 2,
        'max_critic_rounds_per_workstream': 2, 'max_cost': 0, 'extension_requires_user_approval': True},
        'verification_panel': ['acceptance/scope', 'evidence/correctness', 'integration/adversarial'],
        'external_bar': [ref('bar/reference.txt')], 'reader_questions': ref('bar/questions.json'),
        'protected_paths': ['bar'], 'workstreams': tasks,
        'integration_waves': [{'id': 'w1', 'workstreams': ['A']},
                              {'id': 'w2', 'workstreams': ['B', 'C']},
                              {'id': 'w3', 'workstreams': ['D']}]}


class PlanningControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='gauntlet-planning-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.program = program_fixture(self.root)
        self.records = {}

    def accept_fixture(self, ident):
        evidence = self.root / ('evidence-' + ident + '.txt')
        evidence.write_text('Synthetic checked output for ' + ident)
        refs = [{'path': evidence.name, 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}]
        self.records[ident] = planning.acceptance_record(self.program, self.records, ident, refs, self.root)

    def test_n8_diamond_readiness(self):
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), ['A'])
        self.accept_fixture('A')
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), ['B', 'C'])
        self.accept_fixture('B')
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), ['C'])
        self.assertFalse(planning.integration_readiness(self.program, self.records, self.root)['ready'])
        self.accept_fixture('C')
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), ['D'])
        self.accept_fixture('D')
        self.assertTrue(planning.integration_readiness(self.program, self.records, self.root)['ready'])
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), [])

    def test_n8_stale_predecessor_blocks_dependents(self):
        for ident in ['A', 'B', 'C', 'D']:
            self.accept_fixture(ident)
        (self.root / 'evidence-A.txt').write_text('changed after acceptance')
        self.assertEqual(planning.accepted_workstreams(self.program, self.records, self.root), [])
        self.assertFalse(planning.integration_readiness(self.program, self.records, self.root)['ready'])

    def test_n4_duplicate_and_out_of_order_waves(self):
        for waves in [[{'id': 'w', 'workstreams': ['A', 'A']}],
                      [{'id': 'w1', 'workstreams': ['B', 'C']}, {'id': 'w2', 'workstreams': ['A']}, {'id': 'w3', 'workstreams': ['D']}],
                      [{'id': 'w1', 'workstreams': ['A']}, {'id': 'w2', 'workstreams': ['A']}, {'id': 'w3', 'workstreams': ['B', 'C']}, {'id': 'w4', 'workstreams': ['D']}]]:
            bad = copy.deepcopy(self.program)
            bad['integration_waves'] = waves
            with self.subTest(waves=waves), self.assertRaises(planning.PlanningError):
                planning.validate_program(bad, self.root)

    def test_cycles_and_unknown_dependencies(self):
        for deps in [['D'], ['missing']]:
            bad = copy.deepcopy(self.program)
            bad['workstreams'][0]['dependencies'] = deps
            with self.subTest(deps=deps), self.assertRaises(planning.PlanningError):
                planning.compile_waves(bad, self.root)

    def test_n6_parallel_overlap_and_aliases(self):
        for left, right in [('src/shared', 'src/shared/child.txt'), ('src/shared.txt', 'src/../src/shared.txt')]:
            bad = copy.deepcopy(self.program)
            bad['workstreams'][1]['write_targets'] = [left]
            bad['workstreams'][2]['write_targets'] = [right]
            with self.subTest(paths=(left, right)), self.assertRaises(planning.PlanningError):
                planning.validate_program(bad, self.root)
            waves = planning.compile_waves(bad, self.root)
            self.assertFalse(any({'B', 'C'} <= set(w['workstreams']) for w in waves))

    def test_n6_symlink_escape_and_protected_bar(self):
        (self.root / 'escape').symlink_to(self.root.parent, target_is_directory=True)
        for target in ['../outside.txt', 'escape/outside.txt', 'bar/reference.txt', '.gauntlet/state.json']:
            bad = copy.deepcopy(self.program)
            bad['workstreams'][0]['write_targets'] = [target]
            with self.subTest(target=target), self.assertRaises(planning.PlanningError):
                planning.validate_program(bad, self.root)

    def test_n1_reader_question_mutation_rejected(self):
        planning.validate_program(self.program, self.root)
        (self.root / 'bar/questions.json').write_text('["An easier question"]')
        with self.assertRaises(planning.PlanningError):
            planning.validate_program(self.program, self.root)

    def test_external_bar_mutation_rejected(self):
        (self.root / 'bar/reference.txt').write_text('weaker replacement')
        with self.assertRaises(planning.PlanningError):
            planning.validate_program(self.program, self.root)

    def test_n7_capped_work_is_not_ready_or_integrated(self):
        self.records['A'] = {'status': 'capped'}
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), [])
        self.assertFalse(planning.integration_readiness(self.program, self.records, self.root)['ready'])

    def test_running_task_consumes_concurrency(self):
        self.accept_fixture('A')
        self.records['B'] = {'status': 'running'}
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), ['C'])
        self.records['C'] = {'status': 'running'}
        self.assertEqual(planning.ready_workstreams(self.program, self.records, self.root), [])

    def test_transitive_invalidation_preserves_history(self):
        for ident in ['A', 'B', 'C', 'D']:
            self.accept_fixture(ident)
        invalid = planning.invalidate_dependents(self.program, self.records, ['A'], self.root)
        self.assertTrue(all(r['status'] == 'invalidated' for r in invalid.values()))
        self.assertTrue(all(r['previous_record']['status'] == 'accepted' for r in invalid.values()))
        self.assertTrue(all(r['status'] == 'accepted' for r in self.records.values()))

    def test_cli_validate_and_reject_exit_codes(self):
        path = self.root / 'program.json'
        path.write_text(json.dumps(self.program))
        argv = [sys.executable, str(SCRIPTS / 'planning.py'), 'validate', '--project-root', str(self.root), '--program', str(path)]
        valid = subprocess.run(argv, capture_output=True, text=True)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        bad = copy.deepcopy(self.program)
        bad['integration_waves'][0]['workstreams'] = ['A', 'A']
        path.write_text(json.dumps(bad))
        denied = subprocess.run(argv, capture_output=True, text=True)
        self.assertEqual(denied.returncode, 2, denied.stdout)
        self.assertIn('error', json.loads(denied.stderr))


if __name__ == '__main__':
    unittest.main()
