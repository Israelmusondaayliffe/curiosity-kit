"""Source-support labels below are fixture reviewer judgments, not automated truth."""
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
import inspection

class InspectionControls(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='gauntlet-inspection-test-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.art=self.root/'memo.txt';self.art.write_text('Revenue doubled. Nobody churned. A forecast is guaranteed.')
        self.source=self.root/'source.txt';self.source.write_text('Revenue increased by 10%. Churn was not measured.')
        self.questions=self.root/'questions.json';self.questions.write_text('["What revenue growth is claimed?", "What is uncertain?"]')
    def source_ref(self,quote='Revenue increased by 10%.'):
        return {'path':str(self.source),'sha256':hashlib.sha256(self.source.read_bytes()).hexdigest(),'quote':quote}
    def claims(self):
        return {'artifact':str(self.art),'artifact_sha256':inspection.digest(self.art),'claims':[
            {'id':'c1','claim':'Revenue doubled','location':'memo.txt:1','support':'contradicted','reason':'Source says 10%, not 100%', 'sources_checked':[self.source_ref()]},
            {'id':'c2','claim':'Nobody churned','location':'memo.txt:1','support':'unsupported','reason':'Source has no churn measurement','sources_checked':[self.source_ref('Churn was not measured.')]}]}
    def reader(self):
        questions=json.loads(self.questions.read_text())
        return {'artifact':str(self.art),'artifact_sha256':inspection.digest(self.art),'questions_file':str(self.questions),
                'questions_sha256':inspection.digest(self.questions),'questions':questions,
                'answers':[{'question':q,'answer':'The memo states a claim','guessed':False,'answerable':True,'location':'memo.txt:1'} for q in questions]}
    def test_contradicted_and_unsupported_both_survive(self):
        result=inspection.audit_claims(self.claims())
        self.assertEqual(result['status'],'failed');self.assertEqual(len(result['defects']),2)
        self.assertEqual({r['support'] for r in result['defects']},{'contradicted','unsupported'})
    def test_false_quote_hash_or_missing_source_refused(self):
        for field,value in [('quote','This quote is fabricated.'),('sha256','a'*64),('path',str(self.root/'missing'))]:
            data=self.claims();data['claims'][0]['sources_checked'][0][field]=value
            with self.subTest(field=field),self.assertRaises((inspection.InspectionError,OSError)):
                inspection.audit_claims(data)
    def test_empty_ledger_cannot_mean_no_defects(self):
        data=self.claims();data['claims']=[]
        with self.assertRaises(inspection.InspectionError): inspection.audit_claims(data)
    def test_unreachable_judgment_is_unverifiable(self):
        data=self.claims();data['claims']=data['claims'][:1];data['claims'][0]['support']='cannot-verify'
        self.assertEqual(inspection.audit_claims(data)['status'],'unverifiable')
    def test_n1_reader_questions_cannot_be_substituted(self):
        data=self.reader();self.assertEqual(inspection.validate_reader(data)['status'],'passed')
        data['questions'][0]='Easier question'
        with self.assertRaises(inspection.InspectionError):inspection.validate_reader(data)
        data=self.reader();self.questions.write_text('["Changed on disk"]')
        with self.assertRaises(inspection.InspectionError):inspection.validate_reader(data)
    def test_reader_guess_is_gap(self):
        data=self.reader();data['answers'][0]['guessed']=True
        result=inspection.validate_reader(data);self.assertEqual(result['status'],'failed');self.assertEqual(len(result['gaps']),1)
    def test_check_requires_authority_and_records_real_exit(self):
        data={'authorized':False,'argv':[sys.executable,'-c','print("fixture output")'],'cwd':str(self.root),'timeout_seconds':2}
        with self.assertRaises(inspection.InspectionError):inspection.run_check(data)
        data['authorized']=True
        result=inspection.run_check(data);self.assertEqual(result['exit_code'],0);self.assertIn('fixture output',result['stdout'])
        data['argv']=[sys.executable,'-c','raise SystemExit(3)']
        result=inspection.run_check(data);self.assertEqual(result['status'],'failed');self.assertEqual(result['exit_code'],3)
    def brief_fixture(self):
        return {'goal':'Publish a checked memo','done_means':'measured threshold','domain':'research','execution_shape':'S1',
            'out_of_scope':'External publishing','non_negotiables':'No unsupported claims','bar_rationale':'Source is independently frozen',
            'success_criteria':['Every claim traced','All reader questions answered','No contradicted claims'],
            'inspection_methods':['reader-proxy','claim-audit'],'bar_files':[self.source_ref()],
            'output_paths':[str(self.art)],'budget':{'max_launches':5,'max_iterations':2,'max_concurrency':2,'max_seconds':60,'max_cost':0}}
    def test_brief_completeness_and_external_bar_controls(self):
        self.assertEqual(inspection.validate_brief(self.brief_fixture())['status'],'passed')
        for mutation in ['goal','bar','adjectives','budget','self-bar','read-only']:
            d=self.brief_fixture()
            if mutation=='goal':d['goal']=''
            elif mutation=='bar':d['bar_files'][0]['path']=str(self.root/'missing')
            elif mutation=='adjectives':d['bar_files']=[];d['bar_rationale']='Excellent polished compelling'
            elif mutation=='budget':d['budget']['max_seconds']=float('inf')
            elif mutation=='self-bar':d['bar_files']=[{'path':str(self.art)}]
            else:d['inspection_methods']=['read']
            with self.subTest(mutation=mutation),self.assertRaises((inspection.InspectionError,OSError)):
                inspection.validate_brief(d)
    def test_cli_brief_success_and_failure(self):
        path=self.root/'brief.json';data=self.brief_fixture();path.write_text(json.dumps(data))
        cmd=[sys.executable,str(SCRIPTS/'inspection.py'),'brief','--input',str(path)]
        good=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(good.returncode,0,good.stdout+good.stderr)
        data['bar_files']=[];path.write_text(json.dumps(data))
        bad=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(bad.returncode,2,bad.stdout)
    def test_cli_claim_failure_exit(self):
        path=self.root/'input.json';path.write_text(json.dumps(self.claims()))
        result=subprocess.run([sys.executable,str(SCRIPTS/'inspection.py'),'claims','--input',str(path)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2,result.stderr);self.assertEqual(json.loads(result.stdout)['status'],'failed')

if __name__=='__main__':unittest.main()
