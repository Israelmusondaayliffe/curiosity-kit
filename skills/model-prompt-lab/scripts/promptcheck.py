#!/usr/bin/env python3
"""Check declared prompt/audit shapes or XML; plain-text lint is advisory.

Usage: promptcheck.py {prompt-package,audit,text,xml} FILE
Reads one UTF-8 file and emits JSON. It never edits input, calls a model,
fetches URLs or validates a provider's current parameter contract. A valid
result establishes only the named local checks. Python 3.9+; stdlib only.
"""
from __future__ import annotations
import argparse
import datetime
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


def parse_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def bad_constant(value):
        raise ValueError('nonfinite JSON number: ' + value)
    data = json.loads(text, object_pairs_hook=pairs, parse_constant=bad_constant)
    def finite(value):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('nonfinite JSON number')
        if isinstance(value, dict):
            for child in value.values(): finite(child)
        elif isinstance(value, list):
            for child in value: finite(child)
    finite(data)
    return data


class NoDTD(ET.TreeBuilder):
    def doctype(self, name, pubid, system):
        raise ValueError('XML document type declarations are unsupported')


def xml_errors(text):
    if not isinstance(text, str) or not text.strip():
        return ['declared XML must be nonempty text']
    # NoDTD rejects real declarations, not a quoted token in a CDATA example.
    try:
        ET.fromstring(text, parser=ET.XMLParser(target=NoDTD()))
        return []
    except ValueError as exc:
        return [str(exc)]
    except ET.ParseError as original:
        # Prompt blocks may be a fragment with multiple sibling elements.
        try:
            ET.fromstring('<prompt_fragment>' + text + '</prompt_fragment>',
                          parser=ET.XMLParser(target=NoDTD()))
            return []
        except (ET.ParseError, ValueError):
            return ['declared XML is malformed: ' + str(original)]


def lint_text(text):
    errors, warnings = [], []
    if not isinstance(text, str) or not text.strip():
        return {'errors':['prompt is empty'], 'warnings':[]}
    seen = {}
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(('```', '~~~')):
            fenced = not fenced
            continue
        if fenced or stripped.startswith('>') or len(stripped) < 40:
            continue
        if stripped in seen:
            warnings.append({'line':number, 'first_line':seen[stripped],
                             'message':'Repeated literal line. Review its role before changing it.'})
        else:
            seen[stripped] = number
    return {'errors':errors, 'warnings':warnings}


def string(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, allow_empty=True):
    return isinstance(value, list) and (allow_empty or bool(value)) and all(string(x) for x in value)


def object_rows(data, key, errors, required_nonempty=False):
    rows = data.get(key)
    if not isinstance(rows, list):
        errors.append(key + ' must be a list'); return []
    if required_nonempty and not rows:
        errors.append(key + ' must not be empty')
    valid = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict): errors.append(f'{key}[{index}] must be an object')
        else: valid.append((index, row))
    return valid


def target_errors(target):
    errors = []
    if not isinstance(target, dict): return ['target must be an object']
    for key in ('provider','model','interface'):
        if not string(target.get(key)): errors.append('target.' + key + ' must be nonempty')
    if target.get('verification') not in ('unverified','documented','executed'):
        errors.append('target.verification must be unverified, documented or executed')
    if not strings(target.get('sources')): errors.append('target.sources must be a string list')
    if target.get('verification') != 'unverified':
        if not strings(target.get('sources'), False): errors.append('documented target needs sources')
        try: datetime.date.fromisoformat(target.get('checked_at',''))
        except (ValueError, TypeError): errors.append('target.checked_at must be an ISO date')
    elif target.get('checked_at') is not None:
        try: datetime.date.fromisoformat(target['checked_at'])
        except (ValueError, TypeError): errors.append('target.checked_at must be an ISO date or null')
    if target.get('verification') == 'executed' and not string(target.get('execution_evidence')):
        errors.append('executed target needs execution_evidence; this checker cannot authenticate it')
    return errors


def check_package(data):
    if not isinstance(data, dict): return ['prompt package must be an object']
    errors = []
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        errors.append('schema_version must be integer 1')
    if data.get('operation') not in ('create','migrate','diagnose'):
        errors.append('operation must be create, migrate or diagnose')
    errors.extend(target_errors(data.get('target')))
    if not string(data.get('prompt')): errors.append('prompt must be nonempty text')
    if data.get('format') not in ('plain','xml'): errors.append('format must be plain or xml')
    if data.get('format') == 'xml': errors.extend(xml_errors(data.get('prompt')))
    if not strings(data.get('limitations')): errors.append('limitations must be a string list')
    if isinstance(data.get('target'),dict) and data['target'].get('verification')=='unverified':
        if not strings(data.get('limitations'),False): errors.append('unverified target needs a stated limitation')
    ids = set()
    for i, row in object_rows(data,'requirements',errors,True):
        rid = row.get('id')
        if not string(rid) or rid in ids: errors.append(f'requirements[{i}].id must be a unique string')
        else: ids.add(rid)
        if not string(row.get('text')): errors.append(f'requirements[{i}].text must be nonempty')
        if row.get('kind') not in ('task','facts','output','policy','tool','verification'):
            errors.append(f'requirements[{i}].kind is unsupported')
    check_ids = set()
    for i, row in object_rows(data,'checks',errors,True):
        cid = row.get('id')
        if not string(cid) or cid in check_ids: errors.append(f'checks[{i}].id must be a unique string')
        else: check_ids.add(cid)
        refs = row.get('requirement_ids')
        if not strings(refs,False): errors.append(f'checks[{i}].requirement_ids must be a nonempty string list')
        elif any(r not in ids for r in refs): errors.append(f'checks[{i}] references unknown requirement')
        if not string(row.get('method')): errors.append(f'checks[{i}].method must be nonempty')
        if row.get('status') not in ('planned','passed','failed','blocked'):
            errors.append(f'checks[{i}].status is unsupported')
        if row.get('status') in ('passed','failed') and not string(row.get('evidence')):
            errors.append(f'checks[{i}].evidence is required for claimed execution')
    for i, row in object_rows(data,'native_configurations',errors):
        if not string(row.get('label')): errors.append(f'native_configurations[{i}].label must be nonempty')
        if row.get('scope') not in ('target','source_example'):
            errors.append(f'native_configurations[{i}].scope is unsupported')
        if not isinstance(row.get('values'),dict): errors.append(f'native_configurations[{i}].values must be an object')
        if not strings(row.get('sources')): errors.append(f'native_configurations[{i}].sources must be a string list')
        elif row.get('scope') == 'target' and row.get('values') and not row['sources']:
            errors.append(f'native_configurations[{i}].sources required for active native settings')
    return errors


def check_audit(data):
    if not isinstance(data,dict): return ['audit must be an object']
    errors = []
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        errors.append('schema_version must be integer 1')
    source = data.get('source')
    if not isinstance(source,dict): errors.append('source must be an object')
    else:
        for key in ('model','interface'):
            if not string(source.get(key)): errors.append('source.'+key+' must be nonempty')
        digest=source.get('prompt_sha256')
        if not isinstance(digest,str) or not re.fullmatch('[0-9a-f]{64}',digest):
            errors.append('source.prompt_sha256 must be a lowercase SHA-256 identity')
    errors.extend(target_errors(data.get('target')))
    ids=set()
    for i,row in object_rows(data,'findings',errors):
        rid=row.get('id')
        if not string(rid) or rid in ids: errors.append(f'findings[{i}].id must be a unique string')
        else: ids.add(rid)
        for key in ('location','evidence','consequence','action'):
            if not string(row.get(key)): errors.append(f'findings[{i}].{key} must be nonempty')
        if row.get('severity') not in ('critical','major','minor','suggestion'):
            errors.append(f'findings[{i}].severity is unsupported')
        if row.get('certainty') not in ('observed','inferred','unknown'):
            errors.append(f'findings[{i}].certainty is unsupported')
    for i,row in object_rows(data,'unsupported_parameters',errors):
        for key in ('name','scope','evidence','action'):
            if not string(row.get(key)): errors.append(f'unsupported_parameters[{i}].{key} must be nonempty')
    coverage=data.get('coverage')
    if not isinstance(coverage,dict): errors.append('coverage must be an object')
    else:
        if coverage.get('status') not in ('complete','partial','blocked'):
            errors.append('coverage.status is unsupported')
        if not strings(coverage.get('inspected'),False): errors.append('coverage.inspected must be a nonempty string list')
        if not strings(coverage.get('missing')): errors.append('coverage.missing must be a string list')
        if coverage.get('status') in ('partial','blocked') and not coverage.get('missing'):
            errors.append('partial/blocked coverage must name missing evidence')
        if coverage.get('status') == 'complete' and coverage.get('missing'):
            errors.append('complete coverage cannot have missing evidence')
    if type(data.get('verification_required')) is not bool:
        errors.append('verification_required must be boolean')
    return errors


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('prompt-package','audit','text','xml'))
    parser.add_argument('file',type=Path)
    args=parser.parse_args(argv)
    warnings=[]
    try:
        text=args.file.read_text(encoding='utf-8')
        if args.mode in ('prompt-package','audit'):
            data=parse_json(text)
            errors=check_package(data) if args.mode=='prompt-package' else check_audit(data)
            if args.mode=='prompt-package' and isinstance(data,dict) and string(data.get('prompt')):
                warnings=lint_text(data['prompt'])['warnings']
        elif args.mode=='xml': errors=xml_errors(text)
        else:
            result=lint_text(text);errors=result['errors'];warnings=result['warnings']
    except (OSError,ValueError,UnicodeError) as exc:
        errors=[str(exc)]
    result={'valid':not errors,'check':args.mode,'errors':errors,'warnings':warnings,
            'provider_compatibility':'not_checked','runtime_verified':False,
            'claims_authenticated':False,
            'limits':'Shape/XML/literal-line checks only; not source truth, permission, grade validity or model behavior.'}
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    return 0 if not errors else 2

if __name__=='__main__': sys.exit(main())
