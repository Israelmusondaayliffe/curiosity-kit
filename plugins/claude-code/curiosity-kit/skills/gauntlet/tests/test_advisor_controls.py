"""Pure local packet tests. Synthetic host records attest nothing about live models."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import advisor


def context_fixture():
    plan={'version':1,'sha256':'a'*64}
    limits={'launches':4,'concurrency':2,'minutes':60,'cost':0,'rounds':2}
    return {'host':'codex','invocations':{'gauntlet':True,'advisor':True},'run_id':'fixture-run','plan':plan,
        'approval':{'approved':True,'run_id':'fixture-run','plan':copy.deepcopy(plan)},
        'owners':copy.deepcopy(advisor.OWNERS),'perspectives':sorted(advisor.PERSPECTIVES),'remaining':limits,
        'tasks':[{'task_id':'a','objective':'Produce test artifact','model':'gpt-6-luna','dependencies':[],
                  'write_roots':['out'],'outputs':['out/a.txt'],'criteria':['C1'],'evidence_commands':['check'],
                  'limits':copy.deepcopy(limits)}]}


def runtime_fixture():
    c=context_fixture();c.update(advisor_available=True,task_status={'a':'authorized'},host_records={})
    c['tasks'][0].update(worker_record='worker',reviewer_record='reviewer')
    for role in ['worker','reviewer']:
        c['host_records'][role]={'run_id':c['run_id'],'task_id':'a','role':role,'plan':copy.deepcopy(c['plan']),
            'fresh':True,'forked':False,'host_id':'fixture-host','session_id':role+'-session','request_id':role+'-request',
            'request_sha256':'b'*64,'response_sha256':'c'*64,'successful':True,'read_only':role=='reviewer','model':'gpt-6-luna'}
    packet=advisor.build_task_packet(c,'a')
    blobs={'out/a.txt':b'actual result','evidence/check.txt':b'check output'}
    ref=lambda path:{'path':path,'sha256':hashlib.sha256(blobs[path]).hexdigest()}
    returned={'packet_type':'ReturnPacket','run_id':c['run_id'],'plan':copy.deepcopy(c['plan']),'task_id':'a',
        'task_packet_sha256':advisor.digest(packet),'status':'succeeded','actual_write_paths':['out/a.txt'],
        'artifacts':[ref('out/a.txt')],'evidence':[ref('evidence/check.txt')],
        'usage':{'launches':1,'concurrency':1,'minutes':1,'cost':0,'rounds':1},
        'commands':[{'command':'check','exit_code':0,'evidence_path':'evidence/check.txt'}],
        'criterion_to_evidence':{'C1':['evidence/check.txt']}}
    reviewed={'packet_type':'ReviewPacket','run_id':c['run_id'],'plan':copy.deepcopy(c['plan']),'task_id':'a',
        'reviewer':copy.deepcopy(c['host_records']['reviewer']),'task_packet_sha256':advisor.digest(packet),
        'return_packet_sha256':advisor.digest(returned),'artifacts':copy.deepcopy(returned['artifacts']),'verdict':'accepted'}
    return c,packet,returned,blobs,reviewed


class AdvisorControls(unittest.TestCase):
    def test_d5_arbitrary_explicit_model_locally_valid(self):
        c=context_fixture();packet=advisor.build_composition_packet(c)
        result=advisor.validate_composition(packet,c)
        self.assertTrue(result['valid']);self.assertFalse(result['dispatch_authorized'])
        c['tasks'][0]['model']='unlisted-capable-model-selected-by-user'
        self.assertTrue(advisor.validate_composition(advisor.build_composition_packet(c),c)['valid'])

    def test_d5_competing_authority_approval_and_perspective_failures(self):
        for mutation in ['owner','approval','perspectives','stale']:
            c=context_fixture()
            if mutation=='owner':c['owners']['terminal_verdict']='advisor'
            elif mutation=='approval':c['approval']['approved']=False
            elif mutation=='perspectives':c['perspectives']=c['perspectives'][:2]
            else:c['approval']['plan']['sha256']='d'*64
            with self.subTest(mutation=mutation),self.assertRaises(advisor.AdvisorError):advisor.build_composition_packet(c)

    def test_d5_cycle_and_unordered_overlap(self):
        for cyclic in [True,False]:
            c=context_fixture();second=copy.deepcopy(c['tasks'][0]);second['task_id']='b'
            c['tasks'].append(second)
            if cyclic:c['tasks'][0]['dependencies']=['b'];second['dependencies']=['a']
            with self.subTest(cyclic=cyclic),self.assertRaises(advisor.AdvisorError):advisor.build_composition_packet(c)
        c=context_fixture();second=copy.deepcopy(c['tasks'][0]);second.update(task_id='b',dependencies=['a']);c['tasks'].append(second)
        self.assertTrue(advisor.validate_composition(advisor.build_composition_packet(c),c)['valid'])

    def test_absent_advisor_does_not_break_static_validation_but_blocks_dispatch(self):
        c=context_fixture();self.assertTrue(advisor.validate_composition(advisor.build_composition_packet(c),c)['valid'])
        with self.assertRaises(advisor.AdvisorError):advisor.build_task_packet(c,'a')

    def test_bound_synthetic_return_requires_canonical_registration(self):
        c,p,r,b,v=runtime_fixture();result=advisor.validate_return_packet(c,p,r,b,v)
        self.assertTrue(result['valid']);self.assertTrue(result['requires_gauntlet_registration']);self.assertIsNone(result['terminal_verdict'])

    def test_return_tamper_scope_and_self_review_refused(self):
        for mutation in ['bytes','scope','reviewer','plan','failed-command']:
            c,p,r,b,v=runtime_fixture()
            if mutation=='bytes':b['out/a.txt']=b'altered artifact'
            elif mutation=='scope':r['actual_write_paths']=['../outside']
            elif mutation=='reviewer':c['host_records']['reviewer']['session_id']=c['host_records']['worker']['session_id'];v['reviewer']=copy.deepcopy(c['host_records']['reviewer'])
            elif mutation=='plan':r['plan']['sha256']='d'*64
            else:r['commands'][0]['exit_code']=1
            with self.subTest(mutation=mutation),self.assertRaises(advisor.AdvisorError):advisor.validate_return_packet(c,p,r,b,v)

    def test_cli_advisor_validate_exit_codes(self):
        with tempfile.TemporaryDirectory(prefix='gauntlet-advisor-test-') as tmp:
            root=Path(tmp);c=context_fixture();p=advisor.build_composition_packet(c)
            (root/'context.json').write_text(json.dumps(c));(root/'packet.json').write_text(json.dumps(p))
            argv=[sys.executable,str(SCRIPTS/'gauntlet.py'),'advisor-validate','--context',str(root/'context.json'),'--packet',str(root/'packet.json')]
            good=subprocess.run(argv,capture_output=True,text=True)
            self.assertEqual(good.returncode,0,good.stdout+good.stderr)
            p['owners']['approval']='advisor';(root/'packet.json').write_text(json.dumps(p))
            bad=subprocess.run(argv,capture_output=True,text=True)
            self.assertNotEqual(bad.returncode,0,bad.stdout)

if __name__=='__main__':unittest.main()
