"""Ledger controls with synthetic receipts. No helper/model invocation occurs."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import datetime
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import state
import review


def state_fixture(root):
    frozen={}
    for name in ['plan','bar','criteria','reader_questions']:
        p=root/(name+'.txt');p.write_text('Frozen '+name+' content\n');frozen[name]=str(p)
    source=root/'source.txt';source.write_text('Actual external source evidence\n')
    config = {'explicit_invocation':True,'capabilities':{'fresh_context':True,'artifact_inspection':True,'parallel_helpers':True},
        'mode':'artifact','task':'Build one checked synthetic artifact','budget':{'max_launches':20,'max_iterations':10,
        'max_concurrency':3,'max_critic_rounds_per_workstream':2,'max_seconds':3600,'max_cost':0},
        'scope':{'write_roots':[str(root/'target')],'allowed_actions':['read','build']},'frozen':frozen,'source_paths':[str(source)],
        'project_root':str(root),'review':{'policy':review.default_policy(),'criteria_ids':['c1'],'required_perspectives':['acceptance','evidence','adversarial']}}
    config['brief']={'goal':config['task'],'done_means':'blind win','domain':'code','execution_shape':'S1',
        'out_of_scope':'External network and publishing','non_negotiables':'Keep reference unchanged','bar_rationale':'Independent frozen reference',
        'success_criteria':['Output matches reference','Actual inspection runs','Independent review agrees'],
        'inspection_methods':['test'],'bar_files':[{'path':str(source)}],'output_paths':[str(root/'target')],'budget':config['budget']}
    return config



def fable_run(run_dir,log,manifest=None):
    """A Fable Advisor run directory in the source shape: status-free manifest plus run-log.jsonl records."""
    run_dir=Path(run_dir);run_dir.mkdir(parents=True,exist_ok=True)
    m=run_dir/'run-manifest.json'
    m.write_text(manifest if isinstance(manifest,str) else json.dumps(dict({'packet_type':'RunManifest','run_id':run_dir.name,'plan':{'status':'approved'}},**(manifest or {}))))
    if log is not None:(run_dir/'run-log.jsonl').write_text(''.join((r if isinstance(r,str) else json.dumps(r))+'\n' for r in log))
    return m

class StateControls(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='gauntlet-state-test-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.run=self.root/'run';self.config=state_fixture(self.root)

    def initialize(self,approve=True):
        state.init_run(self.run,self.config)
        if approve:
            s=state.load_run(self.run)
            state.approve(self.run,{'contract_hash':s['contract_hash'],'host_verified':True,'host':'synthetic-host',
                'message_id':'fixture-approval','actor':'fixture-owner','verified_by':'fixture-coordinator','verified_at':state.now()})
        return state.load_run(self.run)

    def launch_data(self,rid='request-1',path=None):
        return {'request_id':rid,'capabilities':self.config['capabilities'],'role':'builder','actor':'fixture-builder-'+rid,
                'workstream_id':rid,'action':'build','write_paths':[str(path or self.root/'target'/rid)],
                'fresh_context':True,'estimated_cost':0}

    def test_approval_required_before_launch(self):
        self.initialize(False)
        with self.assertRaises(state.StateError):state.launch(self.run,self.launch_data())
        self.assertEqual(state.load_run(self.run)['usage']['launches'],0)

    def test_d5_peer_absent_active_both_named_before_state(self):
        absent=copy.deepcopy(self.config);absent['peer_probe']=str(self.root/'missing-manifest.json')
        self.assertTrue(state.precheck(absent)['peer_absent'])
        for kind in ['active','both']:
            bad=copy.deepcopy(self.config)
            if kind=='active':
                p=fable_run(self.root/'peer-active',[{'event':'collected','task_id':'T1'}]);bad['peer_probe']=str(p)
            else:bad['fable_requested']=True
            with self.subTest(kind=kind),self.assertRaises(state.StateError):state.init_run(self.run,bad)
            self.assertFalse(self.run.exists())
        terminal=fable_run(self.root/'peer-done',[{'event':'terminal','state':'accepted-and-synthesized'}])
        good=copy.deepcopy(self.config);good['peer_probe']=str(terminal)
        self.assertIn(state.precheck(good)['status'],['supported','full'])

    def test_d5_peer_terminal_read_from_run_log_not_manifest(self):
        # Source manifests carry no run status; only the final run-log record decides, and anything else blocks.
        blocked={
            'manifest status only':fable_run(self.root/'m',None,{'status':'accepted-and-synthesized'}),
            'nonterminal last record':fable_run(self.root/'n',[{'event':'collected','task_id':'T1'}]),
            'reopened after terminal':fable_run(self.root/'r',[{'event':'terminal','state':'failed'},{'event':'dispatched','task_id':'T2'}]),
            'unknown terminal label':fable_run(self.root/'u',[{'event':'terminal','state':'done'}]),
            'malformed last record':fable_run(self.root/'x',['{not json']),
            'malformed manifest':fable_run(self.root/'y',[{'event':'terminal','state':'failed'}],'{not json'),
        }
        for kind,manifest in blocked.items():
            bad=copy.deepcopy(self.config);bad['peer_probe']=str(manifest)
            with self.subTest(kind=kind),self.assertRaises(state.StateError):state.precheck(bad)
        for record in ({'event':'run_closed','terminal_state':'accepted-and-synthesized'},{'event':'terminal','state':'budget-exhausted'}):
            good=copy.deepcopy(self.config);good['peer_probe']=str(fable_run(self.root/record['event'],[record]))
            with self.subTest(record=record):self.assertIn(state.precheck(good)['status'],['supported','degraded'])

    def test_explicit_invocation_gate(self):
        self.config['explicit_invocation']=False
        with self.assertRaises(state.StateError):state.init_run(self.run,self.config)
        self.assertFalse(self.run.exists())

    def test_d7_degraded_recorded_and_unsupported_refused(self):
        self.config['capabilities']['parallel_helpers']=False
        state.init_run(self.run,self.config)
        s=state.load_run(self.run);self.assertEqual(s['surface']['status'],'degraded')
        self.assertIn('parallel_helpers',s['surface']['missing'])
        unsupported=copy.deepcopy(self.config);unsupported['capabilities']['fresh_context']=False
        other=self.root/'unsupported'
        with self.assertRaises(state.StateError):state.init_run(other,unsupported)
        self.assertFalse(other.exists())

    def test_d7_capability_drift_blocks_before_dispatch(self):
        self.initialize();data=self.launch_data();data['capabilities']=dict(data['capabilities'],parallel_helpers=False)
        result=state.launch(self.run,data)
        self.assertFalse(result['may_launch']);s=state.load_run(self.run)
        self.assertEqual(s['usage']['launches'],0);self.assertEqual(s['status'],'blocked')

    def test_n1_frozen_question_change_detected(self):
        self.initialize();Path(self.config['frozen']['reader_questions']).write_text('Easier questions')
        with self.assertRaises(state.StateError):state.verify(self.run)
        with self.assertRaises(state.StateError):state.launch(self.run,self.launch_data())

    def test_launch_replay_does_not_spend_or_relaunch(self):
        self.initialize();data=self.launch_data();first=state.launch(self.run,data);second=state.launch(self.run,data)
        self.assertTrue(first['may_launch']);self.assertFalse(second['may_launch']);self.assertTrue(second['replayed'])
        self.assertEqual(state.load_run(self.run)['usage']['launches'],1)
        changed=copy.deepcopy(data);changed['actor']='different'
        with self.assertRaises(state.StateError):state.launch(self.run,changed)

    def test_n5_counters_cannot_decrease(self):
        self.initialize();state.launch(self.run,self.launch_data())
        state.usage(self.run,{'elapsed_seconds':10})
        for key,value in [('launches',0),('elapsed_seconds',9),('cost',-1),('iterations',float('nan'))]:
            with self.subTest(key=key),self.assertRaises(state.StateError):state.usage(self.run,{key:value})
        self.assertEqual(state.load_run(self.run)['usage']['launches'],1)

    def test_n6_parallel_nested_write_overlap_refused(self):
        self.initialize();state.launch(self.run,self.launch_data('a',self.root/'target/shared'))
        with self.assertRaises(state.StateError):state.launch(self.run,self.launch_data('b',self.root/'target/shared/child.txt'))
        self.assertEqual(state.load_run(self.run)['usage']['launches'],1)

    def test_scope_escape_refused(self):
        self.initialize()
        with self.assertRaises(state.StateError):state.launch(self.run,self.launch_data('a',self.root/'outside.txt'))

    def test_n7_exhaustion_never_certifies(self):
        self.config['budget']['max_launches']=1;self.initialize()
        state.launch(self.run,self.launch_data('a'))
        result=state.launch(self.run,self.launch_data('b'))
        self.assertFalse(result['may_launch']);self.assertEqual(state.load_run(self.run)['status'],'exhausted')
        report=state.report(self.run);self.assertEqual(report['status'],'exhausted')
        self.assertEqual(json.loads((self.run/'evidence-report.json').read_text())['status'],'exhausted')

    def test_recovery_preserves_reservation_accounting_and_disk_resume(self):
        self.initialize();r=state.launch(self.run,self.launch_data());lid=r['launch']['id']
        with self.assertRaises(state.StateError):state.resume(self.run,{'capabilities':self.config['capabilities']})
        state.recover(self.run,{'launch_id':lid,'reason':'Synthetic interrupted process'})
        again=state.recover(self.run,{'launch_id':lid,'reason':'Synthetic interrupted process'})
        self.assertEqual(again['status'],'interrupted')
        state.resume(self.run,{'capabilities':self.config['capabilities']})
        self.assertEqual(state.load_run(self.run)['usage']['launches'],1)
        self.assertEqual(state.load_run(self.run)['status'],'ready')

    def test_handoff_and_report_derive_from_state(self):
        self.initialize();state.launch(self.run,self.launch_data())
        handoff=state.handoff(self.run);disk=state.load_run(self.run)
        self.assertEqual(handoff['usage'],disk['usage']);self.assertEqual(handoff['contract_hash'],disk['contract_hash'])
        self.assertEqual(len(handoff['pending_launches']),1)
        state.report(self.run)
        exported=json.loads((self.run/'evidence-report.json').read_text())
        self.assertEqual(exported['usage'],disk['usage']);self.assertTrue((self.run/'workbench.html').is_file())

    def test_cli_init_approval_gate_and_immutable_failure(self):
        p=self.root/'input.json';p.write_text(json.dumps(self.config))
        argv=[sys.executable,str(SCRIPTS/'gauntlet.py'),'init','--run-dir',str(self.run),'--input',str(p)]
        good=subprocess.run(argv,capture_output=True,text=True);self.assertEqual(good.returncode,0,good.stdout+good.stderr)
        p.write_text(json.dumps(self.launch_data()))
        argv[2]='launch'
        bad=subprocess.run(argv,capture_output=True,text=True);self.assertEqual(bad.returncode,1,bad.stdout)
        self.assertIn('error',json.loads(bad.stdout))

    def test_c12_target_peer_autoprobe_before_state_creation(self):
        peer=self.root/'.fable-advisor/runs/peer-live/run-manifest.json';peer.parent.mkdir(parents=True)
        fable_run(peer.parent,[{'event':'collected','task_id':'T1'}])
        self.assertNotIn('peer_probe',self.config)
        p=self.root/'config.json';p.write_text(json.dumps(self.config))
        result=subprocess.run([sys.executable,str(SCRIPTS/'gauntlet.py'),'init','--run-dir',str(self.run),'--input',str(p)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertFalse(self.run.exists())
        fable_run(peer.parent,[{'event':'collected','task_id':'T1'},{'event':'run_closed','terminal_state':'accepted-and-synthesized'}])
        state.init_run(self.run,self.config)
        self.assertEqual(state.load_run(self.run)['status'],'awaiting_approval')

    def complete_writer(self,reservation,observations,complete=True):
        return state.complete(self.run,{'launch_id':reservation['launch']['id'],'actual_cost':0,'host_receipt':{
            'author_id':reservation['launch']['actor'],'role':'builder','session_id':reservation['launch']['request_id']+'-session',
            'host_record':'fixture://observed-write-receipt','fresh_context':True,'inherited_turns':0,'forbidden_context_seen':False,
            'write_observations_complete':complete,'write_observations':observations}})

    def test_c5_observed_declared_write_hashes_complete(self):
        target=self.root/'target/owned.txt';target.parent.mkdir();target.write_text('Before')
        before=state.file_hash(target)
        self.initialize();reserved=state.launch(self.run,self.launch_data('actual-build',target))
        target.write_text('After observed build')
        observed=[{'path':str(target),'before_sha256':before,'after_sha256':state.file_hash(target)}]
        completed=self.complete_writer(reserved,observed)
        self.assertEqual(completed['status'],'completed')
        self.assertEqual(completed['host_receipt']['write_observations'],observed)

    def test_c5_missing_or_forged_writeset_evidence_rejected(self):
        target=self.root/'target/owned.txt';target.parent.mkdir();target.write_text('Before')
        before=state.file_hash(target)
        self.initialize();reserved=state.launch(self.run,self.launch_data('actual-build',target))
        target.write_text('Actual changed bytes')
        for observed,complete in [([],False),([],True),([{'path':str(target),'before_sha256':before,'after_sha256':'sha256:'+'f'*64}],True)]:
            with self.subTest(observed=observed),self.assertRaises(state.StateError):self.complete_writer(reserved,observed,complete)
        self.assertEqual(state.load_run(self.run)['launches'][reserved['launch']['id']]['status'],'reserved')

    def test_c5_undeclared_write_or_deletion_rejected(self):
        target=self.root/'target/owned.txt';target.parent.mkdir();target.write_text('Owned baseline')
        foreign=self.root/'target/unowned.txt';foreign.write_text('Do not delete')
        self.initialize();reserved=state.launch(self.run,self.launch_data('actual-build',target))
        old=state.file_hash(foreign);foreign.unlink()
        with self.assertRaises(state.StateError):self.complete_writer(reserved,[{'path':str(foreign),'before_sha256':old,'after_sha256':None}])
        foreign.write_text('Do not delete')
        new=self.root/'target/undeclared.txt';new.write_text('Unexpected output')
        with self.assertRaises(state.StateError):self.complete_writer(reserved,[{'path':str(new),'before_sha256':None,'after_sha256':state.file_hash(new)}])
        with self.assertRaises(state.StateError):self.complete_writer(reserved,[])

    def test_c2_approval_and_paused_idle_excluded_active_usage_monotonic(self):
        # Only the wall clock is controlled; all state transitions and persistence are real.
        original=datetime.datetime
        class Clock(original):
            current=original(2026,10,5,12,tzinfo=datetime.timezone.utc)
            @classmethod
            def now(cls,tz=None):return cls.current if tz else cls.current.replace(tzinfo=None)
        self.config['budget']['max_seconds']=30
        with mock.patch.object(state.dt,'datetime',Clock):
            state.init_run(self.run,self.config)
            Clock.current+=datetime.timedelta(days=2)
            s=state.load_run(self.run)
            state.approve(self.run,{'contract_hash':s['contract_hash'],'host_verified':True,'host':'fixture-host',
                'message_id':'timed-approval','actor':'fixture-owner','verified_by':'fixture-coordinator','verified_at':state.now()})
            self.assertIsNone(state.limit(state.load_run(self.run)))
            self.assertEqual(state.load_run(self.run)['usage']['elapsed_seconds'],0)
            first_launch=state.launch(self.run,self.launch_data('timed-first'))
            Clock.current+=datetime.timedelta(seconds=10)
            self.complete_writer(first_launch,[])
            state.pause(self.run,{'reason':'Pause after real active work'})
            first=state.load_run(self.run)
            self.assertEqual(first['session']['elapsed_seconds'],10)
            self.assertEqual(first['usage']['elapsed_seconds'],10)
            Clock.current+=datetime.timedelta(days=3)
            self.assertEqual(state.load_run(self.run)['usage']['elapsed_seconds'],10)
            state.resume(self.run,{'capabilities':self.config['capabilities']})
            resumed=state.load_run(self.run)
            self.assertEqual(resumed['session']['elapsed_seconds'],0)
            self.assertEqual(resumed['usage']['elapsed_seconds'],10)
            second_launch=state.launch(self.run,self.launch_data('timed-second'))
            Clock.current+=datetime.timedelta(seconds=7)
            self.complete_writer(second_launch,[])
            state.pause(self.run,{'reason':'Second active interval'})
            last=state.load_run(self.run)
            self.assertEqual(last['session']['elapsed_seconds'],7)
            self.assertEqual(last['usage']['elapsed_seconds'],17)
            self.assertGreater(last['session']['index'],first['session']['index'])
            with self.assertRaises(state.StateError):state.usage(self.run,{'elapsed_seconds':10})

    def test_c8_new_approved_successor_preserves_exhausted_history(self):
        self.config['budget']['max_launches']=1;self.initialize()
        state.launch(self.run,self.launch_data('spent'))
        state.launch(self.run,self.launch_data('over-cap'))
        old_run=self.run;old_bytes=(old_run/'state.json').read_bytes()
        with self.assertRaises(state.StateError):state.resume(old_run,{'capabilities':self.config['capabilities']})
        self.run=self.root/'explicit-successor';self.config['budget']['max_launches']=2
        self.initialize(False)
        with self.assertRaises(state.StateError):state.launch(self.run,self.launch_data('new-work'))
        s=state.load_run(self.run)
        state.approve(self.run,{'contract_hash':s['contract_hash'],'host_verified':True,'host':'fixture-host',
            'message_id':'separate-successor-approval','actor':'fixture-owner','verified_by':'fixture-coordinator','verified_at':state.now()})
        self.assertTrue(state.launch(self.run,self.launch_data('new-work'))['may_launch'])
        self.assertEqual((old_run/'state.json').read_bytes(),old_bytes)
        self.assertEqual(state.load_run(old_run)['usage']['launches'],1)
        self.assertEqual(state.load_run(old_run)['status'],'exhausted')

    def test_c5_own_run_ledger_excluded_from_output_snapshot(self):
        target=self.root/'target/owned.txt';target.parent.mkdir();target.write_text('Before')
        before=state.file_hash(target)
        self.run=self.root/'target/canonical-run'
        self.initialize();reserved=state.launch(self.run,self.launch_data('own-run-safe',target))
        state.report(self.run)  # Normal generated canonical views must not count as helper edits.
        target.write_text('After legitimate writer')
        completed=self.complete_writer(reserved,[{'path':str(target),'before_sha256':before,'after_sha256':state.file_hash(target)}])
        self.assertEqual(completed['status'],'completed')
        self.assertIn(str(self.run.resolve()),completed['observed_writes']['snapshot_exclusions'])
        self.assertEqual(completed['observed_writes']['changed'],[str(target.resolve())])

    def test_c5_legitimate_parallel_writer_changes_are_separated(self):
        a=self.root/'target/a.txt';a.parent.mkdir();a.write_text('A before')
        b=self.root/'target/b.txt';b.write_text('B before')
        before_a,before_b=state.file_hash(a),state.file_hash(b)
        self.initialize()
        reserved_a=state.launch(self.run,self.launch_data('writer-a',a))
        reserved_b=state.launch(self.run,self.launch_data('writer-b',b))
        a.write_text('A after');b.write_text('B after')
        done_b=self.complete_writer(reserved_b,[{'path':str(b),'before_sha256':before_b,'after_sha256':state.file_hash(b)}])
        done_a=self.complete_writer(reserved_a,[{'path':str(a),'before_sha256':before_a,'after_sha256':state.file_hash(a)}])
        self.assertEqual(done_a['status'],'completed');self.assertEqual(done_b['status'],'completed')
        self.assertEqual(done_a['observed_writes']['changed'],[str(a.resolve())])
        self.assertEqual(done_b['observed_writes']['changed'],[str(b.resolve())])
        self.assertIn(str(b.resolve()),done_a['observed_writes']['concurrent_lane_changes'])
        self.assertIn(str(a.resolve()),done_b['observed_writes']['concurrent_lane_changes'])

    def test_duplicate_json_keys_rejected(self):
        p=self.root/'dup.json';p.write_text('{"a":1,"a":2}')
        with self.assertRaises(state.StateError):state.read_json(p)

    def test_lock_serializes_subprocess_writers(self):
        self.initialize()
        # The subprocess tries an exclusive lock while this process owns it.
        marker=self.root/'lock-entered'
        code='import sys;sys.path.insert(0,sys.argv[1]);import state;from pathlib import Path\nwith state.lock(sys.argv[2]): Path(sys.argv[3]).write_text("entered")'
        with state.lock(self.run):
            p=subprocess.Popen([sys.executable,'-c',code,str(SCRIPTS),str(self.run),str(marker)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            try:
                p.wait(timeout=.15)
                self.fail('Child acquired or exited before parent released lock')
            except subprocess.TimeoutExpired:pass
            self.assertFalse(marker.exists())
        out,err=p.communicate(timeout=5)
        self.assertEqual(p.returncode,0,err);self.assertTrue(marker.exists())

if __name__=='__main__':unittest.main()
