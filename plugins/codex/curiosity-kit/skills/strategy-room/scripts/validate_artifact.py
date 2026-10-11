#!/usr/bin/env python3
"""Structural checks for three optional Strategy Room JSON artifacts; stdlib only.
Adapted from the original coordinator validators, retaining IDs, choice gates and
non-authorization checks. A pass does not prove evidence, consent or good judgment.
"""
import argparse
from datetime import date
import json
import re
from pathlib import Path
import sys
sys.dont_write_bytecode = True

ROUTES = dict(interview='grill-me', wayfind='decision-wayfinder', challenge='assumption-challenger', explore='multi-direction-explorer', synthesize='decision-synthesizer', register='assumption-register', prioritize='curiosity-compass', match='candidate-matcher-and-brief-builder', productize='proof-to-product-mapper')
STATUSES = ('untested', 'supported', 'weakened', 'falsified', 'expired')
REVERSIBILITY = ('reversible', 'partly-reversible', 'irreversible')

def nonblank(value):
    return isinstance(value, str) and bool(value.strip())

def strings(data, fields, errors, prefix=''):
    for field in fields:
        if not nonblank(data.get(field)):
            errors.append(prefix + field + ' must be a nonblank string')

def string_list(data, field, errors, prefix='', nonempty=False):
    value=data.get(field)
    if not isinstance(value,list) or (nonempty and not value) or (isinstance(value,list) and any(not nonblank(x) for x in value)):
        errors.append(prefix+field+' must be a list of nonblank strings'+(' with at least one entry' if nonempty else ''))
        return []
    return value

def enum(data, field, allowed, errors, prefix=''):
    if data.get(field) not in allowed:
        errors.append(prefix+field+' must be one of '+repr(allowed))

def items(data, field, errors):
    value=data.get(field)
    if not isinstance(value,list) or not value:
        errors.append(field+' must be a nonempty list of objects');return [],set()
    result=[];seen=set()
    for i,item in enumerate(value):
        if not isinstance(item,dict):
            errors.append('%s[%d] must be an object'%(field,i));continue
        result.append(item);identifier=item.get('id')
        if not nonblank(identifier):
            errors.append('%s[%d].id must be a nonblank string'%(field,i))
        elif identifier in seen: errors.append(field+' IDs must be unique')
        else: seen.add(identifier)
    return result,seen

def false_flag(data, errors):
    if data.get('execution_authorized') is not False:
        errors.append('execution_authorized must be the Boolean false')

def validate_router(data, errors):
    allowed={'route','specialist','decision','rationale','execution_authorized'}
    if set(data)-allowed: errors.append('router contains unsupported fields: '+', '.join(sorted(set(data)-allowed)))
    strings(data,['decision','rationale','specialist'],errors);false_flag(data,errors)
    route=data.get('route')
    if not isinstance(route,str) or route not in ROUTES: errors.append('route must name one of the nine routes')
    elif data.get('specialist') != ROUTES[route]: errors.append('specialist must match the selected route')

def validate_synthesis(data, errors):
    strings(data,['decision','decision_owner','horizon','stakes','evidence_sufficiency','recommendation','immediate_next_action','handoff'],errors)
    false_flag(data,errors);enum(data,'reversibility',REVERSIBILITY,errors)
    enum(data,'evidence_state',('recommend','recommend provisionally','decline pending evidence'),errors)
    enum(data,'confidence',('low','medium','high'),errors)
    for field in ['criteria','change_conditions']: string_list(data,field,errors,nonempty=True)
    for field in ['evidence','counterevidence','risks','conditions','missing_evidence']: string_list(data,field,errors)
    options,ids=items(data,'options',errors)
    for i,item in enumerate(options): strings(item,['name','case_for','case_against'],errors,'options[%d].'%i)
    state=data.get('evidence_state');recommended=data.get('recommended_option')
    if state=='decline pending evidence':
        if recommended is not None: errors.append('decline pending evidence requires recommended_option null')
        string_list(data,'missing_evidence',errors,nonempty=True)
    else:
        if not isinstance(recommended,str) or recommended not in ids: errors.append('recommended_option must be an existing option ID')
        string_list(data,'evidence',errors,nonempty=True)
    if state=='recommend provisionally':
        if data.get('reversibility')!='reversible': errors.append('provisional recommendation must be reversible')
        string_list(data,'missing_evidence',errors,nonempty=True);string_list(data,'conditions',errors,nonempty=True)
    gate=data.get('user_choice_gate');record=data.get('final_decision_record')
    if 'final_decision_record' not in data: errors.append('final_decision_record is required')
    if not isinstance(gate,dict): errors.append('user_choice_gate must be an object');return
    enum(gate,'state',('pending','complete'),errors,'user_choice_gate.')
    enum(gate,'authority',('user','delegated'),errors,'user_choice_gate.')
    for field in ['choice','authority_source']:
        if field not in gate: errors.append('user_choice_gate.'+field+' is required')
    if gate.get('state')=='pending':
        if gate.get('choice') is not None or record is not None: errors.append('pending gate requires null choice and final_decision_record')
        if gate.get('authority')=='delegated': errors.append('pending gate cannot assert delegated choice authority')
    elif gate.get('state')=='complete':
        choice=gate.get('choice')
        if not isinstance(choice,str) or choice not in ids: errors.append('completed choice must be an existing option ID')
        if not nonblank(gate.get('authority_source')): errors.append('complete choice needs a traceable authority_source; manually verify actual user authority')
        if not isinstance(record,dict): errors.append('completed gate requires final_decision_record object');return
        strings(record,['selected_option','rationale','review_trigger','immediate_next_action','next_owner'],errors,'final_decision_record.')
        if record.get('selected_option')!=choice: errors.append('final selected_option must equal the actual choice')
        for field in ['accepted_risks','rejected_alternatives','unresolved_evidence']: string_list(record,field,errors,'final_decision_record.')
        for rejected in record.get('rejected_alternatives',[]) if isinstance(record.get('rejected_alternatives'),list) else []:
            if not isinstance(rejected,str) or rejected not in ids or rejected==choice: errors.append('rejected_alternatives must contain other existing option IDs')

def validate_register(data,errors):
    strings(data,['decision','decision_ref'],errors)
    assumptions,unused=items(data,'assumptions',errors)
    for i,item in enumerate(assumptions):
        p='assumptions[%d].'%i
        strings(item,['statement','load_bearing','kill_condition'],errors,p)
        enum(item,'kind',('factual','behavioral','capability','timing'),errors,p)
        enum(item,'status',STATUSES,errors,p);enum(item,'confidence',('low','medium','high'),errors,p);enum(item,'reversibility',REVERSIBILITY,errors,p)
        for field in ['owner','test']:
            if field not in item or (item.get(field) is not None and not nonblank(item[field])): errors.append(p+field+' must be nonblank or explicit null')
            if item.get(field) is None and item.get('status')!='untested': errors.append(p+'unknown owner/test requires untested status')
        support=string_list(item,'supporting_evidence',errors,p);against=string_list(item,'contradicting_evidence',errors,p)
        if (item.get('status')=='supported' or item.get('confidence')=='high') and not support: errors.append(p+'supported/high-confidence claim requires supporting evidence')
        if item.get('status') in ('weakened','falsified') and not against: errors.append(p+'weakened/falsified claim requires contradicting evidence')
        history=item.get('history')
        if not isinstance(history,list) or not history: errors.append(p+'history must be a nonempty revision list');continue
        previous=None;last_date=None
        for n,revision in enumerate(history):
            rp=p+'history[%d].'%n
            if not isinstance(revision,dict): errors.append(rp+'must be an object');continue
            strings(revision,['reason'],errors,rp);enum(revision,'to_status',STATUSES,errors,rp)
            ev=string_list(revision,'evidence',errors,rp)
            if revision.get('from_status')!=previous: errors.append(rp+'from_status must match the prior revision (null initially)')
            if 'from_status' not in revision: errors.append(rp+'from_status required')
            if revision.get('to_status') in ('supported','weakened','falsified','expired') and not ev: errors.append(rp+'status change needs dated evidence or expiry basis')
            try:
                value=revision.get('date','')
                if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): raise ValueError('invalid date shape')
                dt=date.fromisoformat(value)
                if last_date and dt<last_date: errors.append(rp+'dates must be nondecreasing')
                last_date=dt
            except (TypeError,ValueError): errors.append(rp+'date must be YYYY-MM-DD')
            previous=revision.get('to_status')
        if previous!=item.get('status'): errors.append(p+'status must match last history revision')

def reject_duplicates(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError('duplicate JSON key: '+key)
        result[key]=value
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=['router','synthesis','register']);parser.add_argument('artifact',type=Path)
    args=parser.parse_args()
    try:
        data=json.loads(args.artifact.read_text(encoding='utf-8'),object_pairs_hook=reject_duplicates,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('invalid JSON constant: '+x)))
    except (OSError,UnicodeError,ValueError) as exc:
        print(json.dumps(dict(valid=False,errors=[str(exc)])));return 2
    errors=[]
    if not isinstance(data,dict): errors.append('artifact must be a JSON object')
    else: {'router':validate_router,'synthesis':validate_synthesis,'register':validate_register}[args.kind](data,errors)
    print(json.dumps(dict(valid=not errors,artifact=args.kind,errors=errors,scope='Structure only; manually verify evidence, judgment and actual authority.'),indent=2))
    return 1 if errors else 0

if __name__=='__main__': raise SystemExit(main())
