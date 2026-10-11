"""Synthetic end-to-end host attestations test plumbing, never model quality/isolation."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import state
import review
import inspection
from test_planning_controls import program_fixture
from test_state_controls import state_fixture


class LifecycleControls(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='gauntlet-lifecycle-test-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.run=self.root/'run';self.config=state_fixture(self.root)
        (self.root/'target').mkdir();self.artifact=self.root/'target/output.txt';self.artifact.write_text('Actual synthetic artifact bytes\n')
        self.inspection=self.root/'inspection.txt';self.inspection.write_text('Observed fixture output; no live reviewer was run.\n')

    def start(self,mode='artifact'):
        self.config['mode']=mode
        if mode=='verification-only':self.config.setdefault('artifact_paths',[str(self.artifact)])
        state.init_run(self.run,self.config);s=state.load_run(self.run)
        state.approve(self.run,{'contract_hash':s['contract_hash'],'host_verified':True,'host':'fixture-host','message_id':'approval-1',
            'actor':'fixture-owner','verified_by':'fixture-coordinator','verified_at':state.now()})

    def dispatch_complete(self,role,ident,extra=None,perspective='acceptance',generation='round1'):
        data={'request_id':ident,'capabilities':self.config['capabilities'],'role':role,'actor':ident+'-author',
            'workstream_id':'piece','action':'read','write_paths':[],'fresh_context':True,'estimated_cost':0,
            'evidence_paths':{'inspection':str(self.inspection)}}
        data.update(extra or {})
        launched=state.launch(self.run,data)
        self.assertTrue(launched['may_launch'])
        receipt={'author_id':data['actor'],'session_id':ident+'-session','host_record':'fixture://'+ident,'role':role,
                 'fresh_context':True,'inherited_turns':0,'forbidden_context_seen':False,'verification_id':generation,
                 'perspectives':[perspective]}
        completed=state.complete(self.run,{'launch_id':launched['launch']['id'],'actual_cost':0,'host_receipt':receipt})
        return completed,receipt

    def round_input(self,index,task_id='piece'):
        s=state.load_run(self.run)
        prepared=review.prepare_blind_pair(self.artifact.read_bytes(),b'A reference fixture artifact\n',
            s['contract'],index)
        packet_hash=review.hash_bytes(review.canonical_bytes(prepared['packet']))
        map_hash=review.hash_bytes(review.canonical_bytes(prepared['sealed_map']))
        e,receipt=self.dispatch_complete('critic','critic'+str(index),{'packet_hash':packet_hash,'sealed_map_hash':map_hash,'workstream_id':task_id},generation='round'+str(index))
        context={'piece_id':task_id,'artifact_hash':state.file_hash(self.artifact),'contract_hash':s['contract_hash'],
            'verification_id':'round'+str(index),'excluded_authors':[],'used_sessions':[],'criteria_ids':['c1'],
            'evidence_manifest':{'inspection':state.file_hash(self.inspection)},'expected_sessions':{receipt['session_id']:receipt},
            'packet_hash':packet_hash,'sealed_map_hash':map_hash}
        verdict={k:context[k] for k in ['piece_id','artifact_hash','contract_hash','verification_id']}
        verdict.update(author_id=receipt['author_id'],session_id=receipt['session_id'],plan_hash_matched=True,
            reason='Synthetic critic compared actual fixture bytes',perspectives=['acceptance'],criteria_checked=['c1'],
            evidence_inspected=[{'id':'inspection','sha256':state.file_hash(self.inspection),'observation':'Actual fixture output inspected'}],
            winner=prepared['sealed_map']['ours_label'],largest_gap='Reference omits a useful concrete fact',gap_is_actionable=True,confidence='high')
        report=self.root/('critic-report-'+str(index)+'.json');report.write_text(json.dumps(verdict))
        return {'evidence_id':'evidence'+str(index),'launch_id':e['id'],'contract_hash':s['contract_hash'],
                'artifact_path':str(self.artifact),'artifact_hash':state.file_hash(self.artifact),'report_path':str(report),
                'verdict':'win','gap':verdict['largest_gap'],'review':dict(prepared,context=context,verdict=verdict),
                'acceptance_evidence':[{'path':str(self.artifact.relative_to(self.root)),'sha256':state.file_hash(self.artifact).split(':',1)[1]}]}

    def final_input(self):
        s=state.load_run(self.run);context={'piece_id':'piece','artifact_hash':state.file_hash(self.artifact),
            'contract_hash':s['contract_hash'],'verification_id':'final1','excluded_authors':[],'used_sessions':[],
            'criteria_ids':self.config['review']['criteria_ids'],
            'required_criteria_ids':self.config['review'].get('required_criteria_ids',self.config['review']['criteria_ids']),
            'required_perspectives':['acceptance','evidence','adversarial'],
            'evidence_manifest':{'inspection':state.file_hash(self.inspection)},'expected_sessions':{},'eligible':True}
        votes=[]
        for role in ['quality','integrity']:
            count=self.config['review']['policy'][role+'_count']
            perspectives=context['required_perspectives'] if count==3 else (['acceptance','evidence'] if role=='quality' else ['adversarial','evidence'])
            for i,perspective in enumerate(perspectives):
                e,r=self.dispatch_complete(role,role+str(i),perspective=perspective,generation='final1')
                context['expected_sessions'][r['session_id']]=r
                vote={k:context[k] for k in ['piece_id','artifact_hash','contract_hash','verification_id']}
                vote.update(author_id=r['author_id'],session_id=r['session_id'],verifier_type=role,result='pass',
                    plan_hash_matched=True,reason='Synthetic independent verdict fixture '+role+str(i),perspectives=[perspective],
                    criteria_checked=list(context['criteria_ids']),criterion_results={c:'pass' for c in context['criteria_ids']},evidence_inspected=[{'id':'inspection','sha256':state.file_hash(self.inspection),'observation':'Fixture evidence checked'}])
                votes.append(vote)
        return {'artifact_path':str(self.artifact),'context':context,'verdicts':votes}

    def test_n3_round_replay_is_idempotent_not_second_win(self):
        self.start();data=self.round_input(1)
        state.record_round(self.run,data);first=state.load_run(self.run)
        again=state.record_round(self.run,data);second=state.load_run(self.run)
        self.assertTrue(again['replayed']);self.assertEqual(first['usage'],second['usage'])
        self.assertEqual(second['pieces']['piece']['consecutive_wins'],1)
        self.assertEqual(second['pieces']['piece']['status'],'looping')
        altered=copy.deepcopy(data);altered['gap']='Changed replay'
        with self.assertRaises(state.StateError):state.record_round(self.run,altered)

    def test_snapshot_changed_between_dispatch_and_record_rejected(self):
        self.start();data=self.round_input(1);self.artifact.write_text('Changed since inspected')
        with self.assertRaises(state.StateError):state.record_round(self.run,data)
        self.assertEqual(state.load_run(self.run)['usage']['iterations'],0)

    def test_happy_artifact_rounds_panel_report_and_replay(self):
        self.start()
        state.record_round(self.run,self.round_input(1));state.record_round(self.run,self.round_input(2))
        self.assertEqual(state.load_run(self.run)['pieces']['piece']['status'],'converged')
        data=self.final_input();result=state.finalize(self.run,data)
        self.assertEqual(result['consensus'],'verified',result['validation_errors'])
        self.assertEqual(state.load_run(self.run)['status'],'verified')
        again=state.finalize(self.run,data)
        self.assertEqual(again['input_hash'],result['input_hash'])
        self.assertEqual(state.load_run(self.run)['usage']['iterations'],2)
        exported=json.loads((self.run/'evidence-report.json').read_text())
        self.assertEqual(exported['status'],'verified')
        self.assertTrue((self.run/'evidence-report.md').is_file());self.assertTrue((self.run/'workbench.html').is_file())

    def test_verification_only_happy_and_artifact_mutation_downgrades(self):
        self.start('verification-only');data=self.final_input()
        result=state.finalize(self.run,data);self.assertEqual(result['consensus'],'verified',result['validation_errors'])
        self.artifact.write_text('Tampered after certification')
        exported=state.report(self.run)
        self.assertEqual(exported['status'],'unverifiable')
        self.assertTrue(json.loads((self.run/'evidence-report.json').read_text())['current_integrity_errors'])

    def test_verification_only_symlink_alias_resolves_to_frozen_identity(self):
        # A path alias (macOS /var vs /private/var, or any symlinked parent) names the same frozen file.
        self.start('verification-only');data=self.final_input()
        alias=self.root/'alias';alias.symlink_to(self.root/'target',target_is_directory=True)
        data['artifact_path']=str(alias/'output.txt')
        result=state.finalize(self.run,data);self.assertEqual(result['consensus'],'verified',result['validation_errors'])

    def builder_request(self,ident):
        return {'request_id':ident,'capabilities':self.config['capabilities'],'role':'builder','actor':ident+'-author',
            'workstream_id':'piece','action':'build','write_paths':[str(self.artifact)],'fresh_context':True,'estimated_cost':0}

    def complete_builder(self,launched):
        return state.complete(self.run,{'launch_id':launched['launch']['id'],'actual_cost':0,'host_receipt':{
            'author_id':launched['launch']['actor'],'session_id':launched['launch']['request_id']+'-session','host_record':'fixture://builder',
            'role':'builder','fresh_context':True,'inherited_turns':0,'forbidden_context_seen':False,
            'write_observations_complete':True,'write_observations':[]}})

    def interrupted_critic(self,ident):
        hashed='sha256:'+'1'*64
        launched=state.launch(self.run,{'request_id':ident,'capabilities':self.config['capabilities'],'role':'critic','actor':ident+'-author',
            'workstream_id':'piece','action':'read','write_paths':[],'fresh_context':True,'estimated_cost':0,
            'evidence_paths':{'inspection':str(self.inspection)},'packet_hash':hashed,'sealed_map_hash':hashed})
        self.assertTrue(launched['may_launch'])
        state.recover(self.run,{'launch_id':launched['launch']['id'],'reason':'Synthetic crash after reservation'})
        state.resume(self.run,{'capabilities':self.config['capabilities']})
        return launched['launch']['id']

    def test_repair_builder_refused_when_its_review_cannot_fit(self):
        # Observed failure: two critic rounds, two consecutive wins needed, one critic interrupted at reservation.
        self.start('artifact')
        self.complete_builder(state.launch(self.run,self.builder_request('initial-builder')))
        lost=self.interrupted_critic('critic-interrupted')
        before=state.load_run(self.run)
        with self.assertRaisesRegex(state.StateError,'Builder refused: workstream piece has 1 critic review'):
            state.launch(self.run,self.builder_request('repair-builder'))
        after=state.load_run(self.run)
        self.assertEqual(after['launches'][lost]['status'],'interrupted')
        self.assertEqual(after['usage'],before['usage']);self.assertEqual(len(after['launches']),len(before['launches']))

    def test_repair_builder_allowed_when_review_capacity_remains(self):
        self.config['budget']['max_critic_rounds_per_workstream']=3;self.config['brief']['budget']=self.config['budget']
        self.start('artifact')
        self.complete_builder(state.launch(self.run,self.builder_request('initial-builder')))
        self.interrupted_critic('critic-interrupted')
        self.assertTrue(state.launch(self.run,self.builder_request('repair-builder'))['may_launch'])

    def test_n2_hash_false_full_lifecycle_cannot_verify(self):
        self.start('verification-only');data=self.final_input();data['verdicts'][0]['plan_hash_matched']=False
        result=state.finalize(self.run,data);self.assertEqual(result['consensus'],'unverifiable')
        self.assertEqual(state.load_run(self.run)['status'],'unverifiable')

    def test_live_inspection_mutation_invalidates_panel(self):
        self.start('verification-only');data=self.final_input();self.inspection.write_text('Evidence changed after reviews')
        result=state.finalize(self.run,data);self.assertEqual(result['consensus'],'unverifiable')

    def test_project_dependency_dispatch_acceptance_integration_final(self):
        program=program_fixture(self.root)
        program['workstreams']=program['workstreams'][:2]
        program['workstreams'][0]['write_targets']=['target/A.txt']
        program['workstreams'][1]['write_targets']=['target/B.txt']
        program['integration_waves']=[{'id':'w1','workstreams':['A']},{'id':'w2','workstreams':['B']}]
        self.config['program']=program;self.config['budget']['max_concurrency']=2
        self.start('project')
        def builder(task):
            return {'request_id':'build-'+task,'capabilities':self.config['capabilities'],'role':'builder','actor':'builder-'+task,
                'workstream_id':task,'action':'build','write_paths':[str(self.root/('target/'+task+'.txt'))],
                'fresh_context':True,'estimated_cost':0}
        with self.assertRaises(state.StateError):state.launch(self.run,builder('B'))
        # Critic fixtures do not launch builders; readiness still enforced when asked to dispatch B.
        self.artifact=self.root/'target/A.txt';self.artifact.write_text('Checked output for A')
        state.record_round(self.run,self.round_input(1,'A'))
        with self.assertRaises(state.StateError):state.launch(self.run,builder('B'))
        state.record_round(self.run,self.round_input(2,'A'))
        launched=state.launch(self.run,builder('B'));self.assertTrue(launched['may_launch'])
        receipt={'author_id':'builder-B','session_id':'builder-B-session','role':'builder','host_record':'fixture://builder-B',
            'fresh_context':True,'inherited_turns':0,'forbidden_context_seen':False,
            'write_observations_complete':True,'write_observations':[]}
        state.complete(self.run,{'launch_id':launched['launch']['id'],'actual_cost':0,'host_receipt':receipt})
        self.artifact=self.root/'target/B.txt';self.artifact.write_text('Checked output for B')
        for index in [3,4]:
            data=self.round_input(index,'B');data['review']['context']['excluded_authors']=['builder-B']
            state.record_round(self.run,data)
        result=inspection.run_check({'authorized':True,'argv':[sys.executable,'-c','print("integration fixture passes")'],
            'cwd':str(self.root),'timeout_seconds':3})
        proof=self.root/'integration.json';proof.write_text(json.dumps(result))
        state.integrate(self.run,{'evidence_path':str(proof),'exit_code':0,'contradictions':[],
            'command':' '.join(result['argv'])})
        data=self.final_input();data['context']['excluded_authors']=['builder-B']
        final=state.finalize(self.run,data)
        self.assertEqual(final['consensus'],'verified',final['validation_errors'])

    def test_knowledge_reader_claims_two_plus_two_final_negative_exports(self):
        self.artifact.write_text('The report claims revenue doubled. It also guarantees next-year profit. The decision is to investigate before investing.')
        original=self.artifact.read_bytes()
        sources=[]
        for index,body in enumerate(['Revenue increased by 10%.','No next-year profit forecast was prepared.','The research budget is provisional.']):
            p=self.root/('knowledge-source-'+str(index)+'.txt');p.write_text(body);sources.append(p)
        questions=['What revenue growth does the memo claim?','What future outcome does it promise?','What action does it recommend?']
        Path(self.config['frozen']['reader_questions']).write_text(json.dumps(questions))
        self.config['source_paths']=[str(p) for p in sources]
        self.config['brief'].update(domain='research',inspection_methods=['reader-proxy','claim-audit'],
            bar_files=[{'path':str(p)} for p in sources])
        self.config['review']['policy'].update(quality_count=2,integrity_count=2)
        self.config['budget']['max_launches']=5
        self.start('verification-only')
        self.dispatch_complete('reader','reader0',perspective='reader-task',generation='reader1')
        raw_reader={'artifact':str(self.artifact),'artifact_sha256':inspection.digest(self.artifact),
            'questions_file':self.config['frozen']['reader_questions'],'questions_sha256':inspection.digest(self.config['frozen']['reader_questions']),
            'questions':questions,'answers':[{'question':q,'answer':a,'guessed':False,'answerable':True,'location':'memo:sentence'+str(i+1)}
                for i,(q,a) in enumerate(zip(questions,['Revenue doubled','Guaranteed next-year profit','Investigate before investing']))]}
        reader_result=inspection.validate_reader(raw_reader)
        checked=[{'path':str(p),'sha256':inspection.digest(p),'quote':p.read_text()} for p in sources]
        raw_claims={'artifact':str(self.artifact),'artifact_sha256':inspection.digest(self.artifact),'claims':[
            {'id':'growth','claim':'Revenue doubled','location':'memo:sentence1','support':'contradicted',
             'reason':'Reviewer fixture:10% growth is not100%','sources_checked':[checked[0]]},
            {'id':'guarantee','claim':'Guaranteed next-year profit','location':'memo:sentence2','support':'unsupported',
             'reason':'Reviewer fixture: none of the three sources provides a profit guarantee','sources_checked':checked}]}
        claim_result=inspection.audit_claims(raw_claims)
        reader_path=self.root/'reader-result.json';reader_path.write_text(json.dumps(reader_result))
        claims_path=self.root/'claim-result.json';claims_path.write_text(json.dumps(claim_result))
        self.inspection=claims_path
        data=self.final_input();data['inspection_reports']={'reader':str(reader_path),'claims':str(claims_path)}
        for vote in data['verdicts']:
            if vote['verifier_type']=='integrity':
                vote['result']='fail';vote['criterion_results']['c1']='fail';vote['reason']='Contradicted growth claim and unsupported guarantee, as recorded in source-checked ledger.'
        result=state.finalize(self.run,data)
        self.assertEqual(result['consensus'],'failed',result['validation_errors'])
        self.assertEqual({c['support'] for c in result['inspections']['claims']['result']['defects']},{'contradicted','unsupported'})
        self.assertEqual(state.load_run(self.run)['usage']['launches'],5)
        self.assertEqual(self.artifact.read_bytes(),original)
        exported=json.loads((self.run/'evidence-report.json').read_text())
        self.assertIn(exported['status'],['failed','unverifiable'])
        self.assertEqual(len(exported['verification']['inspections']['claims']['result']['defects']),2)
        self.assertTrue((self.run/'workbench.html').is_file())

    def rubric_input(self,index,value=4,result='pass'):
        s=state.load_run(self.run)
        e,r=self.dispatch_complete('critic','rubric'+str(index),generation='rubric-round'+str(index))
        context={'piece_id':'piece','artifact_hash':state.file_hash(self.artifact),'contract_hash':s['contract_hash'],
            'verification_id':'rubric-round'+str(index),'excluded_authors':[],'used_sessions':[],'criteria_ids':['c1'],
            'evidence_manifest':{'inspection':state.file_hash(self.inspection)},'expected_sessions':{r['session_id']:r},
            'judging_policy':self.config['review']['judging']}
        verdict={k:context[k] for k in ['piece_id','artifact_hash','contract_hash','verification_id']}
        verdict.update(author_id=r['author_id'],session_id=r['session_id'],plan_hash_matched=True,
            reason='Synthetic rubric judgment on real fixture bytes',perspectives=['acceptance'],criteria_checked=['c1'],
            evidence_inspected=[{'id':'inspection','sha256':state.file_hash(self.inspection),'observation':'Actual fixture inspected'}],
            result=result,confidence='high',largest_gap='Explain the checked evidence more directly',gap_is_actionable=True,
            criterion_observations={'c1':{'value':value,'evidence_ids':['inspection'],'observation':'Synthetic score; no model proof'}})
        report=self.root/('rubric-report-'+str(index)+'.json');report.write_text(json.dumps(verdict))
        return {'evidence_id':'rubric-evidence'+str(index),'launch_id':e['id'],'contract_hash':s['contract_hash'],
                'artifact_path':str(self.artifact),'artifact_hash':state.file_hash(self.artifact),'report_path':str(report),
                'verdict':'win' if result=='pass' else 'blocked' if result=='cannot-verify' else 'revise',
                'gap':verdict['largest_gap'],'review':{'context':context,'verdict':verdict}}

    def test_nonblind_rubric_real_evidence_without_fake_pairing(self):
        self.config['review']['judging']={'mode':'rubric','blind_feasible':False,'reason':'No fair comparator exists',
            'thresholds':{'c1':{'operator':'>=','value':4}}}
        self.start()
        for index in [1,2]:
            data=self.rubric_input(index)
            self.assertNotIn('packet',data['review']);self.assertNotIn('sealed_map',data['review'])
            state.record_round(self.run,data)
        self.assertEqual(state.load_run(self.run)['pieces']['piece']['status'],'converged')
        final=state.finalize(self.run,self.final_input())
        self.assertEqual(final['consensus'],'verified',final['validation_errors'])

    def without_gap(self,data,gap=''):
        data['review']['verdict'].update(largest_gap=gap,gap_is_actionable=False);data['gap']=gap
        Path(data['report_path']).write_text(json.dumps(data['review']['verdict']))
        return data

    def test_no_material_gap_pass_and_blind_win_accepted(self):
        self.config['review']['judging']={'mode':'rubric','blind_feasible':False,'reason':'No fair comparator exists',
            'thresholds':{'c1':{'operator':'>=','value':4}}}
        self.start()
        for index in [1,2]:state.record_round(self.run,self.without_gap(self.rubric_input(index)))
        self.assertEqual(state.load_run(self.run)['pieces']['piece']['status'],'converged')
        blind=LifecycleControls('test_happy_artifact_rounds_panel_report_and_replay');blind.setUp();self.addCleanup(blind.temp.cleanup);blind.start()
        data=blind.without_gap(blind.round_input(1),'No material gap in the preferred artifact')
        prose=dict(data['review']['context'],domain='prose')
        self.assertFalse([e for e in review.validate_critic(data['review']['verdict'],prose) if 'gap' in e])  # no-gap prose win needs no dimension
        state.record_round(blind.run,data)
        self.assertEqual(state.load_run(blind.run)['pieces']['piece']['last_verdict'],'win')

    def test_no_gap_failing_or_losing_verdict_refused(self):
        self.config['review']['judging']={'mode':'rubric','blind_feasible':False,'reason':'No fair comparator exists',
            'thresholds':{'c1':{'operator':'>=','value':4}}}
        self.start()
        with self.assertRaises((state.StateError,review.ReviewError)):
            state.record_round(self.run,self.without_gap(self.rubric_input(1,value=3,result='fail')))
        self.assertEqual(state.load_run(self.run)['usage']['iterations'],0)
        blind=LifecycleControls('test_happy_artifact_rounds_panel_report_and_replay');blind.setUp();self.addCleanup(blind.temp.cleanup);blind.start()
        data=blind.round_input(1);v=data['review']['verdict']
        v['winner']='B' if v['winner']=='A' else 'A';data['verdict']='revise'
        with self.assertRaises((state.StateError,review.ReviewError)):state.record_round(blind.run,blind.without_gap(data))
        self.assertEqual(state.load_run(blind.run)['usage']['iterations'],0)
        prose=dict(data['review']['context'],domain='prose')
        for flag in (0,1):
            v2=dict(data['review']['verdict'],gap_is_actionable=flag,largest_gap='Tighten the argument order')
            self.assertIn('decisive critic verdict must state gap_is_actionable as a boolean',review.validate_critic(v2,prose))
        v3=dict(data['review']['verdict'],gap_is_actionable=True,largest_gap='Tighten the argument order')
        v3.pop('gap_dimension',None)
        self.assertIn('prose gap must improve function, not imitate reference voice',review.validate_critic(v3,prose))
        self.assertNotIn('prose gap must improve function, not imitate reference voice',review.validate_critic(dict(v3,gap_dimension='argument-order'),prose))

    def test_nonblind_claimed_pass_below_frozen_threshold_refused(self):
        self.config['review']['judging']={'mode':'rubric','blind_feasible':False,'reason':'Numeric acceptance threshold',
            'thresholds':{'c1':{'operator':'>=','value':4}}}
        self.start();data=self.rubric_input(1,value=3,result='pass')
        with self.assertRaises((state.StateError,review.ReviewError)):state.record_round(self.run,data)
        self.assertEqual(state.load_run(self.run)['usage']['iterations'],0)
        data['review']['context']['judging_policy']=copy.deepcopy(data['review']['context']['judging_policy'])
        data['review']['context']['judging_policy']['thresholds']['c1']['value']=3
        with self.assertRaises(state.StateError):state.record_round(self.run,data)

    def smoother_request(self,task='piece',path=None):
        return {'request_id':'smooth-'+task,'capabilities':self.config['capabilities'],'role':'smoother','actor':'smoother-author',
            'workstream_id':task,'action':'build','write_paths':[str(path or self.artifact)],'fresh_context':True,'estimated_cost':0}

    def test_smoother_verification_only_forbidden(self):
        self.start('verification-only')
        with self.assertRaises(state.StateError):state.launch(self.run,self.smoother_request())
        self.assertEqual(state.load_run(self.run)['usage']['launches'],0)

    def test_smoother_artifact_resets_wins_and_excluded_from_self_grade(self):
        self.config['budget']['max_critic_rounds_per_workstream']=4
        self.start()
        with self.assertRaises(state.StateError):state.launch(self.run,self.smoother_request())
        state.record_round(self.run,self.round_input(1));state.record_round(self.run,self.round_input(2))
        with self.assertRaises(state.StateError):state.launch(self.run,self.smoother_request(path=self.root/'target/unowned.txt'))
        smooth=state.launch(self.run,self.smoother_request())
        self.assertTrue(smooth['may_launch'])
        s=state.load_run(self.run);self.assertEqual(s['pieces']['piece']['consecutive_wins'],0)
        self.assertEqual(s['pieces']['piece']['status'],'looping');self.assertEqual(s['usage']['launches'],3)
        state.complete(self.run,{'launch_id':smooth['launch']['id'],'actual_cost':0,'host_receipt':{
            'author_id':'smoother-author','session_id':'smoother-session','host_record':'fixture://smoother','role':'smoother',
            'fresh_context':True,'inherited_turns':0,'forbidden_context_seen':False,
            'write_observations_complete':True,'write_observations':[]}})
        for index in [3,4]:
            data=self.round_input(index);data['review']['context']['excluded_authors']=['smoother-author']
            state.record_round(self.run,data)
        data=self.final_input()  # Deliberately omits smoother from excluded authors.
        result=state.finalize(self.run,data)
        self.assertEqual(result['consensus'],'unverifiable')
        self.assertTrue(any('exclusion' in e.lower() for e in result['validation_errors']))

    def test_smoother_project_invalidates_dependents_and_integration(self):
        program=program_fixture(self.root);program['workstreams']=program['workstreams'][:2]
        for task in program['workstreams']:task['write_targets']=['target/'+task['id']+'.txt']
        program['integration_waves']=[{'id':'w1','workstreams':['A']},{'id':'w2','workstreams':['B']}]
        self.config['program']=program;self.config['budget']['max_concurrency']=2
        self.start('project')
        with self.assertRaises(state.StateError):state.launch(self.run,self.smoother_request('A',self.root/'target/A.txt'))
        for index,task in enumerate(['A','B']):
            self.artifact=self.root/('target/'+task+'.txt');self.artifact.write_text('Checked '+task+' output')
            for round_index in [index*2+1,index*2+2]:state.record_round(self.run,self.round_input(round_index,task))
        result=inspection.run_check({'authorized':True,'argv':[sys.executable,'-c','print("integration passes")'],
            'cwd':str(self.root),'timeout_seconds':3})
        proof=self.root/'integration.json';proof.write_text(json.dumps(result))
        integrated={'evidence_path':str(proof),'exit_code':0,'contradictions':[],'command':' '.join(result['argv'])}
        state.integrate(self.run,integrated)
        with self.assertRaises(state.StateError):state.launch(self.run,self.smoother_request('A',self.root/'target/B.txt'))
        smooth=state.launch(self.run,self.smoother_request('A',self.root/'target/A.txt'))
        self.assertTrue(smooth['may_launch']);s=state.load_run(self.run)
        self.assertEqual({k:v['status'] for k,v in s['workstreams'].items()},{'A':'invalidated','B':'invalidated'})
        self.assertIsNone(s['integration']);self.assertTrue(all(p['consecutive_wins']==0 for p in s['pieces'].values()))
        (self.root/'target/A.txt').write_text('Smoothed A output')
        with self.assertRaises(state.StateError):state.integrate(self.run,integrated)
        self.assertNotEqual(state.report(self.run)['status'],'verified')

    def test_finalizer_dissent_state_handoff_report_preserved(self):
        self.config['review']['criteria_ids']=['c1','optional-style']
        self.config['review']['required_criteria_ids']=['c1']
        self.start('verification-only');data=self.final_input()
        data['verdicts'][0]['result']='fail'
        data['verdicts'][0]['criterion_results']['optional-style']='fail'
        data['verdicts'][0]['reason']='Minority quality dissent: supporting detail is too compressed.'
        result=state.finalize(self.run,data)
        self.assertEqual(result['consensus'],'verified-with-dissent',result['validation_errors'])
        self.assertEqual(state.load_run(self.run)['status'],'verified-with-dissent')
        handoff=state.handoff(self.run)
        self.assertEqual(handoff['status'],'verified-with-dissent')
        state.report(self.run)
        exported=json.loads((self.run/'evidence-report.json').read_text())
        self.assertEqual(exported['status'],'verified-with-dissent')
        self.assertEqual(exported['verification']['dissent'][0]['reason'],data['verdicts'][0]['reason'])
        self.assertIn('verified-with-dissent',(self.run/'evidence-report.md').read_text())
        self.artifact.write_text('Changed after dissenting verification')
        self.assertEqual(state.report(self.run)['status'],'unverifiable')

    def cli_operation(self,command,data):
        path=self.root/(command+'-operation.json');path.write_text(json.dumps(data))
        return subprocess.run([sys.executable,str(SCRIPTS/'gauntlet.py'),command,'--run-dir',str(self.run),'--input',str(path)],
                              capture_output=True,text=True)

    def test_cli_verification_target_substitution_rejected(self):
        # Full real lifecycle fixtures, no mocked finalizer or fake consensus function.
        for kind in ['different-bytes','same-bytes-new-path']:
            with self.subTest(kind=kind):
                self.run=self.root/('run-'+kind)
                self.start('verification-only');data=self.final_input()
                substitute=self.root/('substitute-'+kind+'.txt')
                substitute.write_bytes(self.artifact.read_bytes() if kind=='same-bytes-new-path' else b'Unapproved substitute artifact')
                data['artifact_path']=str(substitute)
                data['context']['artifact_hash']=state.file_hash(substitute)
                for vote in data['verdicts']:vote['artifact_hash']=state.file_hash(substitute)
                result=self.cli_operation('finalize',data)
                self.assertEqual(result.returncode,1,result.stdout+result.stderr)
                self.assertNotIn(state.load_run(self.run)['status'],['verified','verified-with-dissent'])

    def test_cli_multiapproved_targets_partial_coverage_rejected(self):
        second=self.root/'target/second.txt';second.write_text('Second approved artifact needing independent coverage')
        self.config['artifact_paths']=[str(self.artifact),str(second)]
        self.start('verification-only');data=self.final_input()
        result=self.cli_operation('finalize',data)
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertNotIn(state.load_run(self.run)['status'],['verified','verified-with-dissent'])

    def test_cli_round_artifact_outside_approved_scope_rejected(self):
        self.start()
        self.artifact=self.root/'outside-write-scope.txt';self.artifact.write_text('Foreign artifact outside approved target tree')
        data=self.round_input(1)
        result=self.cli_operation('round',data)
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertEqual(state.load_run(self.run)['usage']['iterations'],0)

    def test_cli_round_cross_workstream_output_rejected(self):
        program=program_fixture(self.root);program['workstreams']=program['workstreams'][:2]
        for task in program['workstreams']:task['write_targets']=['target/'+task['id']+'.txt']
        program['integration_waves']=[{'id':'w1','workstreams':['A']},{'id':'w2','workstreams':['B']}]
        self.config['program']=program;self.config['budget']['max_concurrency']=2
        self.start('project')
        self.artifact=self.root/'target/B.txt';self.artifact.write_text('B output must not be accepted as A')
        data=self.round_input(1,'A')
        result=self.cli_operation('round',data)
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertEqual(state.load_run(self.run)['usage']['iterations'],0)
        self.assertNotIn('A',state.load_run(self.run)['workstreams'])

    def test_c9_stop_preserves_terminal_verdict_receipts(self):
        for outcome in ['verified','verified-with-dissent','failed','unverifiable']:
            with self.subTest(outcome=outcome):
                self.run=self.root/('terminal-'+outcome)
                self.config['review']['criteria_ids']=['c1','optional-style']
                self.config['review']['required_criteria_ids']=['c1']
                self.start('verification-only');data=self.final_input()
                if outcome=='verified-with-dissent':
                    data['verdicts'][0]['result']='fail';data['verdicts'][0]['criterion_results']['optional-style']='fail'
                elif outcome=='failed':
                    data['verdicts'][3]['result']='fail';data['verdicts'][3]['criterion_results']['c1']='fail'
                elif outcome=='unverifiable':data['verdicts'][0]['plan_hash_matched']=False
                result=state.finalize(self.run,data);self.assertEqual(result['consensus'],outcome,result['validation_errors'])
                before=state.load_run(self.run)
                stopped=self.cli_operation('stop',{'reason':'Late stop must preserve terminal receipt'})
                self.assertIn(stopped.returncode,[0,1],stopped.stdout+stopped.stderr)
                after=state.load_run(self.run)
                self.assertEqual(after['status'],outcome)
                self.assertEqual(after['verification'],before['verification'])

    def test_c14_required_failure_full_finalizer_not_dissent(self):
        self.start('verification-only');data=self.final_input()
        data['verdicts'][0]['result']='fail';data['verdicts'][0]['criterion_results']['c1']='fail'
        result=self.cli_operation('finalize',data)
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertEqual(json.loads(result.stdout)['consensus'],'failed')
        self.assertEqual(state.load_run(self.run)['status'],'failed')

    def test_cli_finalize_success_and_failure_exit_codes(self):
        self.start('verification-only');data=self.final_input();p=self.root/'final.json';p.write_text(json.dumps(data))
        cmd=[sys.executable,str(SCRIPTS/'gauntlet.py'),'finalize','--run-dir',str(self.run),'--input',str(p)]
        result=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(json.loads(result.stdout)['consensus'],'verified')
        data['verdicts'][0]['reason']='Changed immutable final input';p.write_text(json.dumps(data))
        altered=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(altered.returncode,1,altered.stdout)

if __name__=='__main__':unittest.main()
