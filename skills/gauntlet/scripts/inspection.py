#!/usr/bin/env python3
"""Observable inspection helpers; no implicit network, model calls or state writes."""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from datetime import datetime, timezone

class InspectionError(ValueError):
    pass

def digest(path):
    p = Path(path).resolve(strict=True)
    if not p.is_file():
        raise InspectionError('evidence must be a regular file')
    return hashlib.sha256(p.read_bytes()).hexdigest()

def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise InspectionError(name + ' must be nonempty text')
    return value

def evidence(path, expected=None):
    actual = digest(path)
    if expected is not None and expected != actual:
        raise InspectionError('evidence hash mismatch: ' + str(path))
    return {'path': str(Path(path).resolve()), 'sha256': actual}

def validate_brief(data):
    fields = ('goal','done_means','domain','execution_shape','out_of_scope','non_negotiables','bar_rationale')
    for name in fields:
        text(data.get(name),name)
    if data['domain'] not in {'code','visual','prose','research','deck','strategy','prompt-system','brand'}:
        raise InspectionError('unsupported domain')
    if data['execution_shape'] not in {'S1','S2','S3'}:
        raise InspectionError('execution_shape must be S1, S2 or S3')
    criteria = data.get('success_criteria')
    if not isinstance(criteria,list) or not criteria or not all(isinstance(c,str) and c.strip() for c in criteria):
        raise InspectionError('independently checkable success_criteria required')
    if len(set(criteria)) != len(criteria):
        raise InspectionError('duplicate success criteria')
    methods = data.get('inspection_methods')
    allowed = {'run','test','measure','render','screenshot','read','reader-proxy','claim-audit','source-reach','red-team'}
    if not isinstance(methods,list) or not methods or any(m not in allowed for m in methods):
        raise InspectionError('declare supported inspection methods')
    bars = data.get('bar_files')
    if not isinstance(bars,list) or not bars:
        raise InspectionError('external bar needs actual inspectable files, not adjectives')
    outputs = [Path(p).resolve() for p in data.get('output_paths',[])]
    refs = []
    for source in bars:
        ref=evidence(source['path'],source.get('sha256'));p=Path(ref['path'])
        if any(p==o or o in p.parents or p in o.parents for o in outputs):
            raise InspectionError('candidate output cannot supply or overwrite its own bar')
        if p.stat().st_size==0: raise InspectionError('bar file is empty')
        refs.append(ref)
    budget = data.get('budget')
    if not isinstance(budget,dict): raise InspectionError('finite runtime budget required')
    for name in ('max_launches','max_iterations','max_concurrency','max_seconds'):
        v=budget.get(name)
        if type(v) not in (int,float) or not math.isfinite(v) or v<=0:
            raise InspectionError('positive finite '+name+' required')
    cost=budget.get('max_cost')
    if type(cost) not in (int,float) or not math.isfinite(cost) or cost<0:
        raise InspectionError('finite nonnegative max_cost required')
    if data['domain'] in {'prose','research','deck','strategy','prompt-system'}:
        if 'reader-proxy' not in methods and 'claim-audit' not in methods:
            raise InspectionError('knowledge work requires reader-proxy or claim-audit, not read alone')
    return {'status':'passed','bar_files':refs,'criteria_count':len(criteria),
            'limit':'Completeness and actual files checked. Coordinator must assess bar fairness and whether criteria are genuinely checkable.'}


def validate_reader(data):
    questions = data.get('questions')
    if not isinstance(questions,list) or not questions or not all(isinstance(q,str) and q.strip() for q in questions):
        raise InspectionError('frozen nonempty question list required')
    if len(set(questions)) != len(questions):
        raise InspectionError('duplicate questions')
    rows = data.get('answers')
    if not isinstance(rows,list) or len(rows)!=len(questions):
        raise InspectionError('one answer for every frozen question required')
    inspected = evidence(data['artifact'],data.get('artifact_sha256'))
    qfile = evidence(data['questions_file'],data.get('questions_sha256'))
    frozen = json.loads(Path(qfile['path']).read_text(encoding='utf-8'))
    if isinstance(frozen,dict): frozen=frozen.get('questions')
    if frozen != questions:
        raise InspectionError('reader questions differ from frozen file')
    gaps=[]
    for q,row in zip(questions,rows):
        if not isinstance(row,dict) or row.get('question')!=q:
            raise InspectionError('reader question identity/order mismatch')
        text(row.get('answer'),'answer')
        if type(row.get('guessed')) is not bool or type(row.get('answerable')) is not bool:
            raise InspectionError('reader must state guessed and answerable')
        text(row.get('location'),'artifact location')
        if row['guessed'] or not row['answerable']:
            gaps.append(row)
    return {'status':'failed' if gaps else 'passed','artifact':inspected,'questions':qfile,'answers':rows,'gaps':gaps,
            'limit':'Structure and hashes checked. Semantic accuracy and actual isolated reader execution require host evidence.'}

def audit_claims(data):
    """Validate explicit claim-to-source judgments and quotes, not semantic truth by regex."""
    artifact = evidence(data['artifact'],data.get('artifact_sha256'))
    rows=data.get('claims')
    if not isinstance(rows,list) or not rows:
        raise InspectionError('nonempty claim ledger required; absence is not zero defects')
    seen=set(); defects=[]; unknown=[]; citations=set(); output=[]
    for row in rows:
        if not isinstance(row,dict): raise InspectionError('claim must be object')
        cid=text(row.get('id'),'claim id')
        if cid in seen: raise InspectionError('duplicate claim id')
        seen.add(cid)
        text(row.get('claim'),'claim'); text(row.get('location'),'artifact location')
        status=row.get('support')
        if status not in {'supported','contradicted','unsupported','cannot-verify'}:
            raise InspectionError('support must be explicit semantic judgment')
        text(row.get('reason'),'reason')
        checked=row.get('sources_checked')
        if not isinstance(checked,list) or not checked:
            raise InspectionError('even unsupported claims require the sources actually checked')
        normalized=[]
        for source in checked:
            if not isinstance(source,dict): raise InspectionError('source object required')
            item=evidence(source['path'],source.get('sha256'))
            quote=source.get('quote','')
            if not isinstance(quote,str): raise InspectionError('quote must be text')
            if quote and quote not in Path(item['path']).read_text(encoding='utf-8'):
                raise InspectionError('quote absent from cited source for '+cid)
            item['quote']=quote;normalized.append(item);citations.add(item['sha256'])
        if status in {'supported','contradicted'} and not any(s['quote'].strip() for s in normalized):
            raise InspectionError('supported/contradicted needs actual source excerpt')
        entry=dict(row,sources_checked=normalized);output.append(entry)
        if status in {'contradicted','unsupported'}: defects.append(entry)
        if status=='cannot-verify': unknown.append(entry)
    return {'status':'failed' if defects else 'unverifiable' if unknown else 'passed',
            'artifact':artifact,'claims':output,'claim_count':len(rows),'defects':defects,'unknown':unknown,
            'unique_source_count':len(citations),'supported_ratio':sum(r['support']=='supported' for r in rows)/len(rows),
            'limit':'Script validates ledger, source bytes, quote presence and counts. A fresh integrity judge must verify semantic support and completeness; no automatic web reachability claim.'}

def run_check(data):
    """Run an explicitly authorized local argv check and capture actual output."""
    if data.get('authorized') is not True:
        raise InspectionError('record actual task authorization before executing')
    argv=data.get('argv')
    if not isinstance(argv,list) or not argv or not all(isinstance(a,str) and a for a in argv):
        raise InspectionError('argv must be nonempty strings, no shell parsing')
    cwd=Path(data['cwd']).resolve(strict=True)
    seconds=data.get('timeout_seconds')
    if isinstance(seconds,bool) or not isinstance(seconds,(int,float)) or not math.isfinite(seconds) or seconds<=0:
        raise InspectionError('finite positive timeout required')
    start=datetime.now(timezone.utc).isoformat()
    try:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=seconds,shell=False)
        code=p.returncode; stdout=p.stdout;stderr=p.stderr;timed_out=False
    except subprocess.TimeoutExpired as e:
        code=None; stdout=(e.stdout or b'');stderr=(e.stderr or b'');timed_out=True
        if isinstance(stdout,bytes): stdout=stdout.decode('utf-8','replace')
        if isinstance(stderr,bytes): stderr=stderr.decode('utf-8','replace')
    outputs=[evidence(p) for p in data.get('artifacts',[])]
    return {'status':'passed' if code==0 and not timed_out else 'failed','argv':argv,'cwd':str(cwd),
            'exit_code':code,'stdout':stdout,'stderr':stderr,'timed_out':timed_out,'started_at':start,
            'finished_at':datetime.now(timezone.utc).isoformat(),'artifacts':outputs,
            'limit':'Local process is not sandboxed. Caller must authorize its actions and inspect side effects; timeout is not a process-tree containment guarantee.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['brief','reader','claims','check'])
    p.add_argument('--input',required=True)
    a=p.parse_args()
    try:
        data=json.loads(Path(a.input).read_text(encoding='utf-8'))
        result={'brief':validate_brief,'reader':validate_reader,'claims':audit_claims,'check':run_check}[a.command](data)
        print(json.dumps(result,sort_keys=True,indent=2,allow_nan=False))
        return 0 if result['status'] in {'clear','full','degraded','passed'} else 2
    except (InspectionError,ValueError,OSError,KeyError,TypeError) as e:
        print(json.dumps({'status':'invalid','error':str(e)}));return 2
if __name__=='__main__': raise SystemExit(main())
