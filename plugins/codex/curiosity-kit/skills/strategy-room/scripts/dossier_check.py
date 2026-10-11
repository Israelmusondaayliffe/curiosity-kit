#!/usr/bin/env python3
"""Check the optional Markdown researcher handoff, not truth or evidence sufficiency.
Retains the original dossier sections, source table, effort/pace CLI and structured
failure report. No quotas: source independence, coverage and recency are diagnostics.
"""
import argparse
import calendar
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit
sys.dont_write_bytecode = True


def section(text,title):
    match=re.search(r'^##\s+'+re.escape(title)+r'\s*\n(.*?)(?=^##\s|\Z)',text,re.M|re.S|re.I)
    return match.group(1).strip() if match else ''

def field(text,label):
    match=re.search(r'^\s*\*\*'+re.escape(label)+r':\*\*[ \t]*([^\n]*)',text,re.M|re.I)
    return match.group(1).strip() if match else ''

def meaningful(text):
    text=text.strip().lstrip('- ').strip()
    return bool(text) and not text.startswith('[') and text.lower().rstrip('.') not in ('n/a','none','unknown','to be determined')

def source_identity(locator):
    """Source-only URL identity; never apply Markdown exceptions to claim text."""
    locator=locator.strip()
    link=re.fullmatch(r'\[([^\]\n]+)\]\((https?://\S+)\)',locator,re.I)
    if link:
        if not meaningful(link.group(1)): return None
        locator=link.group(2)
    elif not meaningful(locator):
        return None
    if re.match(r'^https?://',locator,re.I):
        try:
            parts=urlsplit(locator)
            if not parts.hostname: return None
            # Scheme/host are case-insensitive; path, query and trailing slash are not.
            return urlunsplit((parts.scheme.lower(),parts.netloc.lower(),parts.path,parts.query,''))
        except ValueError:
            return None
    return locator

def bullets(text):
    return re.findall(r'^\s*-\s+(.+?)\s*$',text,re.M)

def source_refs(text):
    match=re.search(r'\*\*Sources:\*\*(.*?)(?=^\*\*|^###|\Z)',text,re.M|re.S)
    return [re.split(r'[:\s,]',x.strip(),maxsplit=1)[0] for x in bullets(match.group(1))] if match else []

def calendar_cutoff(today,months):
    absolute=today.year*12+today.month-1-months
    year,month=divmod(absolute,12);month+=1
    return date(year,month,min(today.day,calendar.monthrange(year,month)[1]))

def check_dossier(text,effort=None,pace=None,today=None):
    today=today or date.today();errors=[];warnings=[]
    declared_effort=field(text,'Effort mode').lower()
    declared_pace=field(text,'Subject pace').lower().replace('-moving','')
    for supplied,declared,label,allowed in [(effort,declared_effort,'effort',('light','standard','deep')),(pace,declared_pace,'pace',('fast','standard','slow'))]:
        if declared not in allowed: errors.append('Declare a valid '+label+' in dossier metadata')
        if supplied is not None and supplied!=declared: errors.append('CLI '+label+' contradicts dossier metadata')
    effort=declared_effort;pace=declared_pace
    mode=field(text,'Source mode').lower();assessment=field(text,'Assessment').lower()
    if mode not in ('web','supplied','mixed'):errors.append('Source mode must be web, supplied or mixed')
    if assessment not in ('bounded','incomplete'):errors.append('Assessment must be bounded or incomplete')
    for name in ['Subject Summary','Evidence Sufficiency','Limitations','Open Questions']:
        if not section(text,name): errors.append('Missing '+name+' section (explicit None is allowed where appropriate)')
    for name in ['Subject Summary','Evidence Sufficiency']:
        if not meaningful(section(text,name)): errors.append(name+' must contain nonblank, non-placeholder text')
    if assessment=='incomplete' and not meaningful(section(text,'Limitations')): errors.append('Incomplete evidence must state its limitations')
    sources=[];headers=None
    for line in section(text,'Source List').splitlines():
        if not line.strip().startswith('|'):continue
        cells=[x.strip() for x in line.strip().strip('|').split('|')]
        if cells[0].lower()=='id':headers=[x.lower() for x in cells];continue
        if all(re.fullmatch(r':?-+:?',c) for c in cells):continue
        if not headers or len(cells)!=len(headers):errors.append('Malformed source table row');continue
        sources.append(dict(zip(headers,cells)))
    ids=set();locators=set();origins=[];recent=0;unknown_dates=0;future_dates=0
    for source in sources:
        sid=source.get('id','');locator=source.get('source','')
        if not meaningful(sid) or sid in ids:errors.append('Source IDs must be meaningful and unique')
        else:ids.add(sid)
        # Labels do not create new sources; syndication still uses explicit Origin.
        identity=source_identity(locator)
        if identity is None or identity in locators:errors.append('Source locators must be meaningful and unique')
        locators.add(identity)
        if source.get('tier','').upper() not in ('A','B','C','D'):errors.append('Source '+sid+' needs tier A, B, C or D')
        if source.get('tier','').upper()=='D':warnings.append('Source '+sid+' is low-quality context; manually verify it is not supporting a material claim alone')
        origin=source.get('origin','')
        if meaningful(origin):origins.append(origin.casefold())
        else:warnings.append('Source '+sid+' has unknown origin; independence cannot be inferred from its hostname/title')
        access=source.get('access','')
        if access and access not in ('read','supplied','inaccessible','metadata-only'):errors.append('Source '+sid+' has invalid Access')
        if not access:warnings.append('Source '+sid+' lacks explicit Access; verify actual body access before relying on it')
        if access in ('inaccessible','metadata-only'):warnings.append('Source '+sid+' body unavailable; do not treat it as read')
        if mode=='supplied' and access=='read':errors.append('Supplied-only mode must not claim a web body read')
        for key in ['date published','date accessed','event date','date inspected']:
            value=source.get(key,'').strip()
            if value.lower() in ('','unknown','n/a'):
                if key=='date published':unknown_dates+=1
                continue
            try:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): raise ValueError('invalid date shape')
                parsed=date.fromisoformat(value)
            except ValueError:errors.append('Source '+sid+' '+key+' must be YYYY-MM-DD or unknown');continue
            if parsed>today:
                errors.append('Source '+sid+' '+key+' is future-dated');future_dates+=1;continue
            if key=='date published' and parsed>=calendar_cutoff(today,12 if pace=='fast' else 36 if pace=='standard' else 60):recent+=1
    if not sources and assessment!='incomplete':errors.append('Bounded dossier needs actual sources; otherwise mark incomplete')
    coverage=section(text,'Dimensions Covered')
    covered_match=re.search(r'\*\*Covered:\*\*(.*?)(?=\*\*Skipped:|\Z)',coverage,re.S)
    skipped_match=re.search(r'\*\*Skipped:\*\*(.*)',coverage,re.S)
    covered=bullets(covered_match.group(1)) if covered_match else []
    skipped=bullets(skipped_match.group(1)) if skipped_match else []
    names=[]
    for name in covered:
        if not meaningful(name):errors.append('Covered dimension needs a meaningful name')
        names.append(name.casefold())
    for item in skipped:
        pair=item.split(':',1)
        if len(pair)!=2 or not all(meaningful(x) for x in pair):errors.append('Skipped dimension needs a name and substantive reason')
        names.append(pair[0].casefold().strip())
    if not names:errors.append('Declare covered or justified skipped dimensions')
    if len(set(names))!=len(names):errors.append('Dimension names must be unique across covered/skipped')
    dim_matches=list(re.finditer(r'^###\s+Dimension\s+\d+:\s*([^\n]+)\n(.*?)(?=^###\s+Dimension|^##\s|\Z)',text,re.M|re.S|re.I))
    counts={};finding_ids=set()
    for match in dim_matches:
        name,body=match.group(1).strip(),match.group(2)
        if name.casefold() in (n.casefold() for n in counts):errors.append('Duplicate dimension section '+name)
        disposition=field(body,'Disposition').lower() or 'covered'
        if disposition not in ('covered','no-material-finding','unresolved'):errors.append('Invalid dimension Disposition '+name)
        findings=list(re.finditer(r'^####\s+Finding\s+([^:\n]+):[^\n]*\n(.*?)(?=^####\s|\Z)',body,re.M|re.S|re.I))
        counts[name]=len(findings)
        if not findings and disposition=='covered':errors.append('Covered dimension '+name+' has no findings')
        if disposition in ('no-material-finding','unresolved'):
            if not meaningful(field(body,'Rationale')):errors.append('Explicit no-finding/unresolved dimension needs Rationale')
            if findings:errors.append('No-finding/unresolved dimension must not contain findings')
        if disposition=='unresolved' and assessment!='incomplete':errors.append('Unresolved dimension requires incomplete assessment')
        for finding in findings:
            fid=finding.group(1).strip();fbody=finding.group(2)
            if fid in finding_ids:errors.append('Finding IDs must be unique')
            finding_ids.add(fid)
            if not meaningful(field(fbody,'Claim')):errors.append('Finding '+fid+' has no meaningful Claim')
            refs=source_refs(fbody)
            if not refs or any(ref not in ids for ref in refs):errors.append('Finding '+fid+' must reference existing source IDs')
    if {x.casefold() for x in covered}!={x.casefold() for x in counts}:errors.append('Covered dimensions and actual Dimension sections must agree')
    disagreement=section(text,'Expert Disagreement Map');state=field(disagreement,'State').lower()
    if state not in ('disagreement','consensus','unassessed'):errors.append('Disagreement map needs explicit State: disagreement, consensus or unassessed')
    if not meaningful(field(disagreement,'Scope')):errors.append('Disagreement map needs substantive search/review Scope')
    refs=source_refs(disagreement)
    if (state!='unassessed' and not refs) or any(ref not in ids for ref in refs):errors.append('Disagreement/consensus map must reference existing source IDs')
    if state=='unassessed' and assessment!='incomplete':errors.append('Unassessed disagreement requires incomplete assessment')
    if state=='disagreement':
        entries=list(re.finditer(r'^###\s+Disagreement\s+[^:\n]+:[^\n]*\n(.*?)(?=^###\s|\Z)',disagreement,re.M|re.S|re.I))
        if not entries:errors.append('Disagreement state requires substantive entries')
        for entry in entries:
            body=entry.group(1)
            for label in ['Position 1','Position 2']:
                if not meaningful(field(body,label)):errors.append('Disagreement entry needs '+label)
            if len(re.findall(r'^\s*-\s+Advocates:\s*\S.+$',body,re.M))<2 or len(re.findall(r'^\s*-\s+Reasoning:\s*\S.+$',body,re.M))<2:errors.append('Both positions need advocates and reasoning')
    if unknown_dates:warnings.append('Unknown publication dates count as not known recent, not as recent evidence')
    if pace=='slow':warnings.append('Historical foundational evidence is allowed; assess relevance manually')
    counts_origin=Counter(origins)
    stats=dict(source_count=len(sources),independent_origins=len(counts_origin),largest_origin_share=max(counts_origin.values(),default=0)/len(sources) if sources else 0,recent_fraction=recent/len(sources) if sources else 0,unknown_publication_dates=unknown_dates,future_dates=future_dates,dimensions_covered=len(covered),dimensions_skipped=len(skipped),findings_by_dimension=counts)
    return dict(valid=not errors,passed=not errors,evidence_ready=False if assessment=='incomplete' or errors else None,assessment=assessment,effort=effort,pace=pace,stats=stats,failures=errors,warnings=warnings,scope='Structure only. Evidence readiness requires human/model review; null means not certified, false means incomplete or invalid.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dossier',type=Path);parser.add_argument('--effort',choices=['light','standard','deep']);parser.add_argument('--pace',choices=['fast','standard','slow']);parser.add_argument('--json',action='store_true',help='Retained compatibility flag; output is always structured JSON.');parser.add_argument('--as-of',type=date.fromisoformat,default=date.today())
    args=parser.parse_args()
    try:text=args.dossier.read_text(encoding='utf-8')
    except (OSError,UnicodeError) as exc:
        print(json.dumps(dict(valid=False,passed=False,failures=[str(exc)])));return 2
    result=check_dossier(text,args.effort,args.pace,args.as_of);print(json.dumps(result,indent=2));return 0 if result['valid'] else 1

if __name__=='__main__':raise SystemExit(main())
