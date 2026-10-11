"""Deterministic panel and blind-packet controls; no model judgments are executed."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import review


def panel_fixture():
    h = lambda c: 'sha256:' + c * 64
    context = {'piece_id': 'p', 'artifact_hash': h('a'), 'contract_hash': h('b'),
               'verification_id': 'v1', 'eligible': True, 'excluded_authors': ['builder'],
               'used_sessions': [], 'criteria_ids': ['criterion'],
               'required_perspectives': ['scope', 'evidence', 'integration'],
               'evidence_manifest': {'actual-inspection': h('c')}, 'expected_sessions': {}}
    votes = []
    for role in ['quality', 'integrity']:
        for index, perspective in enumerate(context['required_perspectives']):
            session = role + '-session-' + str(index)
            author = role + '-author-' + str(index)
            context['expected_sessions'][session] = {'author_id': author, 'role': role,
                'verification_id': 'v1', 'fresh_context': True, 'inherited_turns': 0,
                'forbidden_context_seen': False, 'perspectives': [perspective]}
            votes.append({k: context[k] for k in ['piece_id', 'artifact_hash', 'contract_hash', 'verification_id']})
            votes[-1].update(author_id=author, session_id=session, verifier_type=role, result='pass',
                plan_hash_matched=True, reason='Synthetic fixture: explicit evidence observation',
                perspectives=[perspective], criteria_checked=['criterion'],
                evidence_inspected=[{'id': 'actual-inspection', 'sha256': h('c'), 'observation': 'Fixture output recorded'}])
    return context, votes


class ReviewControls(unittest.TestCase):
    def setUp(self):
        self.context, self.votes = panel_fixture()

    def verdict(self):
        return review.compute_consensus(self.votes, self.context)

    def test_consensus_table(self):
        self.context['criteria_ids']=['criterion','optional-style'];self.context['required_criteria_ids']=['criterion']
        for vote in self.votes:
            vote['criteria_checked']=['criterion','optional-style'];vote['criterion_results']={'criterion':'pass','optional-style':'pass'}
        self.assertEqual(self.verdict()['consensus'], 'verified')
        self.votes[0]['result'] = 'fail'
        self.votes[0]['criterion_results']['optional-style']='fail'
        self.votes[0]['reason'] = 'Exact dissent must survive.'
        result = self.verdict()
        self.assertEqual(result['consensus'], 'verified-with-dissent')
        self.assertEqual(result['dissent'][0]['reason'], 'Exact dissent must survive.')
        self.votes[1]['result'] = 'fail'
        self.votes[1]['criterion_results']['optional-style']='fail'
        self.assertEqual(self.verdict()['consensus'], 'failed')
        self.votes[0]['result'] = self.votes[1]['result'] = 'pass'
        self.votes[0]['criterion_results']['optional-style']=self.votes[1]['criterion_results']['optional-style']='pass'
        self.votes[3]['result'] = 'fail'
        self.votes[3]['criterion_results']['criterion']='fail'
        self.assertEqual(self.verdict()['consensus'], 'failed')
        self.votes[3]['result'] = 'cannot-verify'
        self.votes[3]['criterion_results']['criterion']='cannot-verify'
        self.assertEqual(self.verdict()['consensus'], 'unverifiable')

    def test_c14_required_quality_failure_vetoes_majority(self):
        for vote in self.votes:vote['criterion_results']={'criterion':'pass'}
        self.votes[0]['result']='fail';self.votes[0]['criterion_results']['criterion']='fail'
        result=self.verdict()
        self.assertEqual(result['consensus'],'failed',result['validation_errors'])
        self.assertEqual(result['quality_votes']['pass'],2)

    def test_n2_false_plan_hash_never_passes(self):
        self.votes[0]['plan_hash_matched'] = False
        result = self.verdict()
        self.assertEqual(result['consensus'], 'unverifiable')
        self.assertTrue(result['validation_errors'])

    def test_missing_inspection_or_stale_artifact_never_passes(self):
        for key, value in [('evidence_inspected', []), ('artifact_hash', 'sha256:'+'d'*64),
                           ('contract_hash', 'sha256:'+'d'*64)]:
            with self.subTest(key=key):
                self.context, self.votes = panel_fixture()
                self.votes[0][key] = value
                self.assertEqual(self.verdict()['consensus'], 'unverifiable')

    def test_partial_panel_duplicate_session_and_builder_refused(self):
        self.votes.pop()
        self.assertEqual(self.verdict()['consensus'], 'unverifiable')
        self.context, self.votes = panel_fixture()
        self.votes[1] = copy.deepcopy(self.votes[0])
        self.assertEqual(self.verdict()['consensus'], 'unverifiable')
        self.context, self.votes = panel_fixture()
        self.votes[0]['author_id'] = 'builder'
        self.assertEqual(self.verdict()['consensus'], 'unverifiable')

    def test_context_contamination_and_missing_perspectives(self):
        sid = self.votes[0]['session_id']
        for key, value in [('inherited_turns', 1), ('fresh_context', False), ('forbidden_context_seen', True)]:
            with self.subTest(key=key):
                context = copy.deepcopy(self.context)
                context['expected_sessions'][sid][key] = value
                self.assertEqual(review.compute_consensus(self.votes, context)['consensus'], 'unverifiable')
        self.context['required_perspectives'].append('fourth-perspective')
        self.assertEqual(self.verdict()['consensus'], 'unverifiable')

    def test_n7_capped_or_unready_eligibility_cannot_verify(self):
        self.context['eligible'] = False
        self.assertEqual(self.verdict()['consensus'], 'unverifiable')

    def test_four_independent_votes_cover_three_perspectives(self):
        self.votes = [self.votes[i] for i in [0, 1, 3, 5]]
        self.context['expected_sessions'] = {v['session_id']: self.context['expected_sessions'][v['session_id']] for v in self.votes}
        policy = review.default_policy()
        policy.update(quality_count=2, integrity_count=2)
        self.assertEqual(review.compute_consensus(self.votes, self.context, policy)['consensus'], 'verified')
        policy.update(quality_count=1)
        self.assertEqual(review.compute_consensus(self.votes, self.context, policy)['consensus'], 'unverifiable')

    def test_contract_hash_covers_question_set(self):
        contract = {'goal':'Write useful report', 'bar_description':'Frozen reference', 'acceptance_criterion':'Reader can answer',
                    'reader_questions':['Original hard question']}
        first = review.contract_hash(contract)
        contract['reader_questions'] = ['Easier substituted question']
        self.assertNotEqual(review.contract_hash(contract), first)

    def test_cli_panel_exits(self):
        with tempfile.TemporaryDirectory(prefix='gauntlet-review-test-') as tmp:
            path = Path(tmp) / 'input.json'
            argv = [sys.executable, str(SCRIPTS/'review.py'), 'consensus', '--input', str(path)]
            path.write_text(json.dumps({'context': self.context, 'verdicts': self.votes}))
            good = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr + good.stdout)
            self.votes[0]['plan_hash_matched'] = False
            path.write_text(json.dumps({'context': self.context, 'verdicts': self.votes}))
            bad = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1, bad.stdout)
            self.assertEqual(json.loads(bad.stdout)['consensus'], 'unverifiable')

    def test_cli_blind_packet_is_neutral_and_overwrite_refused(self):
        with tempfile.TemporaryDirectory(prefix='gauntlet-blind-test-') as tmp:
            root = Path(tmp)
            (root/'ours.txt').write_text('---\nauthor: candidate\n---\nActual candidate text\n')
            (root/'ref.txt').write_text('Author: comparator\nActual reference text\n')
            (root/'contract.json').write_text(json.dumps({'goal':'Write useful output', 'bar_description':'A real reference', 'acceptance_criterion':'Clear and supported'}))
            argv = [sys.executable,str(SCRIPTS/'review.py'),'blind','--ours',str(root/'ours.txt'),'--reference',str(root/'ref.txt'),
                    '--contract',str(root/'contract.json'),'--seed','7','--packet',str(root/'neutral/packet.json'),'--sealed-map',str(root/'sealed/map.json')]
            first = subprocess.run(argv,capture_output=True,text=True)
            self.assertEqual(first.returncode,0,first.stderr+first.stdout)
            packet=(root/'neutral/packet.json').read_text()
            self.assertNotIn('ours.txt',packet)
            self.assertNotIn('ours_label',packet)
            self.assertNotIn('author: candidate',packet)
            self.assertNotIn('Author: comparator',packet)
            self.assertNotIn(str(root/'sealed'),first.stdout)
            second=subprocess.run(argv,capture_output=True,text=True)
            self.assertEqual(second.returncode,1,second.stdout)


if __name__ == '__main__': unittest.main()
