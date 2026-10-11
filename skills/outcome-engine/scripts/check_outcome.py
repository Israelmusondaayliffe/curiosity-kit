#!/usr/bin/env python3
"""Read-only structural checks for explicitly supplied Outcome Engine records."""
import argparse
import hashlib
from datetime import datetime
import json
import os
import re
import stat
import sys

MAX_BYTES = 1024 * 1024
BRIEF = ('Outcome', 'Audience or user', 'Success evidence', 'Constraints', 'Decisions',
         'Requirements', 'Risks and unknowns', 'Blockers', 'Out of scope', 'Next action')
REVIEW = ('System and user', 'Current-state map', 'Diagnosis', 'Friction candidates',
          'Top recommendation', 'Future-state allocation', 'Controls exceptions and recovery',
          'Right-sized pilot', 'Decisions needed', 'Proof after pilot')
PILOT = ('Scope', 'Owner', 'Baseline', 'Success signal', 'Stop', 'Rollback', 'Review date', 'Exclusions')
PRECOMMIT = ('decision', 'owner', 'riskiest_assumption', 'current_evidence', 'prediction',
             'support_rule', 'weakening_rule', 'inconclusive_rule', 'invalidation_rule',
             'method', 'sample', 'selection', 'baseline', 'measure', 'independent_oracle',
             'time_boundary', 'cost_boundary', 'data_boundary', 'permission_boundary',
             'confounders', 'proof_limits', 'raw_evidence_location', 'stop_condition',
             'follow_on_condition')

class SchemaError(ValueError):
    pass


def obj(value, required, optional=(), at='record'):
    if not isinstance(value, dict):
        raise SchemaError(at + ': expected object')
    missing, extra = set(required) - value.keys(), value.keys() - set(required) - set(optional)
    if missing or extra:
        raise SchemaError('%s: missing keys %s; unknown keys %s' % (at, sorted(missing), sorted(extra)))


def string(value, at, nullable=False):
    if nullable and value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise SchemaError(at + ': expected nonempty string' + (' or null' if nullable else ''))


def integer(value, at):
    if type(value) is not int or value < 1:
        raise SchemaError(at + ': expected positive integer')


def enum(value, choices, at):
    if not isinstance(value, str) or value not in choices:
        raise SchemaError(at + ': expected one of ' + ', '.join(choices))


def array(value, at, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise SchemaError(at + ': expected ' + ('nonempty ' if nonempty else '') + 'array')


def strings(value, at, nonempty=False):
    array(value, at, nonempty)
    for v in value:
        string(v, at)
    if len(set(value)) != len(value):
        raise SchemaError(at + ': duplicate entries')


def records(value, at):
    array(value, at)
    found = {}
    for row in value:
        if not isinstance(row, dict):
            raise SchemaError(at + ': expected object entries')
        string(row.get('id'), at + '.id')
        if row['id'] in found:
            raise SchemaError(at + ': duplicate id ' + row['id'])
        found[row['id']] = row
    return found


def version(value):
    if type(value) is not int or value != 1:
        raise SchemaError('version: expected integer 1')


def validate_markdown(text, mode):
    """Return structural findings for the supported canonical ATX format."""
    required = BRIEF if mode == 'brief' else REVIEW
    headings, lines, fence = [], text.splitlines(), None
    visible = []
    for i, line in enumerate(lines):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = (marker[1][0], len(marker[1]))
            continue
        visible.append((i, line))
        h = re.match(r'^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$', line)
        if h:
            headings.append((i, len(h[1]), h[2].strip()))
    findings = []
    for name in required:
        matches = [(i, level) for i, level, title in headings if title.casefold() == name.casefold()]
        if len(matches) != 1:
            findings.append('%s: expected one canonical heading, found %d' % (name, len(matches)))
            continue
        start, level = matches[0]
        end = next((i for i, lev, _ in headings if i > start and lev <= level), len(lines))
        body = '\n'.join(line for i, line in visible if start < i < end)
        substantive = re.sub(r'^ {0,3}#{1,6}\s+.*$', '', body, flags=re.M)
        substantive = re.sub(r'<!--.*?-->', '', substantive, flags=re.S).strip()
        if not substantive:
            findings.append(name + ': empty section')
        # Slot keywords are uppercase so ordinary prose such as "[Enter via the side door]" passes.
        if re.search(r'\[(?:TODO|TBD|FILL(?: IN)?|INSERT|REPLACE|DESCRIBE|ENTER)(?:\b[^\]]*)\](?!\()', body) or re.search(r'\{\{[^}]+\}\}|<INSERT\b[^>]*>', body, re.I):
            findings.append(name + ': unresolved instructional slot')
        if mode == 'review' and name == 'Right-sized pilot':
            for label in PILOT:
                # Canonical labeled lines or nested ATX headings, not incidental prose. A labeled line needs an
                # actual value after any closing bold markup: "**Rollback:**" alone is empty.
                values = re.findall(r'^\s*(?:[-*]\s+)?(?:\*\*)?' + re.escape(label) + r'(?:\*\*)?[ \t]*:(.*)$', body, re.I | re.M)
                heading = re.search(r'^\s*#{1,6}\s+' + re.escape(label) + r'\s*$', body, re.I | re.M)
                if any(re.sub(r'^\*\*', '', v.strip()).strip() for v in values):
                    continue
                if heading:
                    section = re.split(r'^\s*#{1,6}\s', body[heading.end():], maxsplit=1, flags=re.M)[0]
                    if section.strip():
                        continue
                findings.append('Right-sized pilot: ' + ('empty ' if values or heading else 'missing labeled ') + label)
    return findings


def validate_plan(data):
    """Return (findings, dependency_ready_ids, blocked_reasons). No work is run."""
    obj(data, ('version', 'brief', 'requirements', 'slices'), ('controls',))
    version(data['version'])
    brief = data['brief']
    obj(brief, ('source', 'revision', 'status', 'approval_source'), at='brief')
    for key in ('source', 'revision'):
        string(brief[key], 'brief.' + key)
    enum(brief['status'], ('proposed', 'accepted'), 'brief.status')
    string(brief['approval_source'], 'brief.approval_source', True)
    reqs, slices = records(data['requirements'], 'requirements'), records(data['slices'], 'slices')
    if not reqs or not slices:
        raise SchemaError('requirements and slices must be nonempty')
    for row in reqs.values():
        obj(row, ('id', 'text'), at='requirement')
        string(row['text'], 'requirement.text')
    controls = data.get('controls', dict(assets=[], decisions=[], approvals=[], risks=[]))
    obj(controls, ('assets', 'decisions', 'approvals', 'risks'), at='controls')
    assets, decisions, approvals, risks = [records(controls[k], k) for k in ('assets', 'decisions', 'approvals', 'risks')]
    for row in decisions.values():
        obj(row, ('id', 'status', 'value', 'source'), at='decision')
        enum(row['status'], ('proposed', 'accepted', 'deferred', 'rejected'), 'decision.status')
        for key in ('value', 'source'):
            string(row[key], 'decision.' + key)
    for row in risks.values():
        obj(row, ('id', 'description', 'owner', 'recovery'), at='risk')
        for key in ('description', 'owner', 'recovery'):
            string(row[key], 'risk.' + key)
    for row in approvals.values():
        obj(row, ('id', 'asset', 'version', 'scope', 'owner', 'status', 'evidence'), at='approval')
        integer(row['version'], 'approval.version')
        enum(row['status'], ('pending', 'approved', 'rejected'), 'approval.status')
        for key in ('asset', 'scope', 'owner'):
            string(row[key], 'approval.' + key)
        string(row['evidence'], 'approval.evidence', True)
    for row in assets.values():
        obj(row, ('id', 'title', 'owner', 'version', 'state', 'location', 'decision_ids', 'risk_ids', 'production_slices', 'verification_slices', 'approval_ids', 'delivery_authority', 'delivery_evidence'), at='asset')
        integer(row['version'], 'asset.version')
        enum(row['state'], ('planned', 'draft', 'verified', 'approved', 'delivered'), 'asset.state')
        for key in ('title', 'owner'):
            string(row[key], 'asset.' + key)
        for key in ('location', 'delivery_authority', 'delivery_evidence'):
            string(row[key], 'asset.' + key, True)
        for key in ('decision_ids', 'risk_ids', 'production_slices', 'verification_slices', 'approval_ids'):
            strings(row[key], 'asset.' + key, key in ('production_slices', 'verification_slices'))
    for row in slices.values():
        obj(row, ('id', 'title', 'outcome', 'proof', 'checks', 'dependencies', 'blockers', 'owner', 'action_scope', 'boundaries', 'state', 'output_version', 'evidence', 'asset_ids', 'approval_ids', 'authority'), at='slice')
        for key in ('title', 'outcome', 'proof', 'owner', 'action_scope'):
            string(row[key], 'slice.' + key)
        integer(row['output_version'], 'slice.output_version')
        enum(row['state'], ('planned', 'active', 'blocked', 'verified'), 'slice.state')
        string(row['authority'], 'slice.authority', True)
        for key in ('boundaries', 'asset_ids', 'approval_ids'):
            strings(row[key], 'slice.' + key, key == 'boundaries')
        checks = records(row['checks'], 'slice.checks')
        if not checks:
            raise SchemaError('slice.checks: must be nonempty')
        for check in checks.values():
            obj(check, ('id', 'requirement_ids', 'description'), at='check')
            strings(check['requirement_ids'], 'check.requirement_ids', True)
            string(check['description'], 'check.description')
        array(row['dependencies'], 'slice.dependencies')
        seen = set()
        for dep in row['dependencies']:
            obj(dep, ('slice', 'output_version'), at='dependency')
            string(dep['slice'], 'dependency.slice')
            integer(dep['output_version'], 'dependency.output_version')
            if dep['slice'] in seen:
                raise SchemaError('duplicate dependency ' + dep['slice'])
            seen.add(dep['slice'])
        array(row['blockers'], 'slice.blockers')
        for b in row['blockers']:
            obj(b, ('description', 'cleared', 'evidence'), at='blocker')
            string(b['description'], 'blocker.description')
            if type(b['cleared']) is not bool:
                raise SchemaError('blocker.cleared: expected boolean')
            string(b['evidence'], 'blocker.evidence', True)
        array(row['evidence'], 'slice.evidence')
        seen = set()
        for e in row['evidence']:
            obj(e, ('check', 'output_version', 'source', 'result'), at='evidence')
            string(e['check'], 'evidence.check')
            string(e['source'], 'evidence.source')
            integer(e['output_version'], 'evidence.output_version')
            enum(e['result'], ('pass', 'fail'), 'evidence.result')
            if (e['check'], e['output_version']) in seen:
                raise SchemaError('duplicate evidence check/version')
            seen.add((e['check'], e['output_version']))
    findings, gates, covered = [], {}, set()
    def refs(ids, domain, context):
        for ident in ids:
            if ident not in domain:
                findings.append(context + ': unknown reference ' + ident)
    if brief['status'] == 'accepted' and not brief['approval_source']:
        findings.append('accepted brief needs approval_source')
    for aid, a in approvals.items():
        refs([a['asset']], assets, aid)
        if a['status'] == 'approved' and not a['evidence']:
            findings.append(aid + ': approved record lacks evidence')
    def approval_gate(ident, asset_ids=None, scope=None):
        a = approvals.get(ident)
        if not a:
            return 'unknown approval ' + ident
        asset = assets.get(a['asset'])
        if not asset:
            return ident + ': unknown asset'
        if asset_ids is not None and a['asset'] not in asset_ids:
            return ident + ': approval asset outside slice associations'
        if a['version'] != asset['version']:
            return ident + ': stale asset version'
        if scope is not None and a['scope'] != scope:
            return ident + ': scope mismatch'
        if a['status'] != 'approved' or not a['evidence']:
            return ident + ': approval not recorded with evidence'
        return None
    for sid, s in slices.items():
        reasons = []
        refs(s['asset_ids'], assets, sid)
        if brief['status'] != 'accepted' or not brief['approval_source']:
            reasons.append('brief acceptance not recorded')
        for dep in s['dependencies']:
            target = slices.get(dep['slice'])
            if target is None:
                findings.append(sid + ': unknown dependency ' + dep['slice'])
                reasons.append('unknown dependency ' + dep['slice'])
            elif target['state'] != 'verified' or target['output_version'] != dep['output_version']:
                reasons.append('dependency %s needs verified output version %s' % (dep['slice'], dep['output_version']))
        for b in s['blockers']:
            if not b['cleared']:
                reasons.append('blocker: ' + b['description'])
            elif not b['evidence']:
                findings.append(sid + ': cleared blocker lacks evidence')
                reasons.append('blocker clearance lacks evidence')
        for ident in s['approval_ids']:
            problem = approval_gate(ident, s['asset_ids'], s['action_scope'])
            if problem:
                reasons.append(problem)
            if ident not in approvals:
                findings.append(sid + ': unknown approval ' + ident)
        checks = {c['id']: c for c in s['checks']}
        for c in checks.values():
            refs(c['requirement_ids'], reqs, sid + '/' + c['id'])
            covered.update(c['requirement_ids'])
        current_pass = set()
        for e in s['evidence']:
            if e['check'] not in checks:
                findings.append(sid + ': evidence for unknown check ' + e['check'])
            if e['output_version'] != s['output_version']:
                findings.append(sid + ': evidence output version differs from current slice')
            if e['result'] == 'pass' and e['output_version'] == s['output_version']:
                current_pass.add(e['check'])
        if s['state'] == 'verified':
            if current_pass != set(checks):
                findings.append(sid + ': verified needs current passing evidence for every check')
            if reasons:
                findings.append(sid + ': verified with unmet gates: ' + '; '.join(reasons))
        if s['state'] == 'active' and reasons:
            findings.append(sid + ': active with unmet gates: ' + '; '.join(reasons))
        if s['state'] == 'blocked' and not reasons:
            findings.append(sid + ': blocked without a declared unmet gate')
        gates[sid] = reasons
    for rid in reqs.keys() - covered:
        findings.append('uncovered requirement ' + rid)
    # Iterative depth-first cycle detection avoids recursion limits on bounded but large inputs.
    colors = {}
    for root in slices:
        stack = [(root, False)]
        while stack:
            sid, leaving = stack.pop()
            if leaving:
                colors[sid] = 2
                continue
            if colors.get(sid) == 1:
                findings.append('slice dependency cycle includes ' + sid)
                continue
            if colors.get(sid) == 2:
                continue
            colors[sid] = 1
            stack.append((sid, True))
            for dep in slices[sid]['dependencies']:
                if dep['slice'] in slices:
                    stack.append((dep['slice'], False))
    for aid, a in assets.items():
        for key, domain in (('decision_ids', decisions), ('risk_ids', risks), ('production_slices', slices), ('verification_slices', slices), ('approval_ids', approvals)):
            refs(a[key], domain, aid)
        for sid in a['production_slices'] + a['verification_slices']:
            if sid in slices and aid not in slices[sid]['asset_ids']:
                findings.append(aid + ': slice does not reference asset ' + sid)
        if a['state'] != 'planned' and not a['location']:
            findings.append(aid + ': produced asset needs location')
        if a['state'] in ('verified', 'approved', 'delivered'):
            for sid in a['production_slices'] + a['verification_slices']:
                if sid in slices and (slices[sid]['state'] != 'verified' or slices[sid]['output_version'] != a['version']):
                    findings.append(aid + ': requires verified current-version production/verification slice ' + sid)
            for did in a['decision_ids']:
                if did in decisions and decisions[did]['status'] != 'accepted':
                    findings.append(aid + ': governing decision is not accepted: ' + did)
        if a['state'] in ('approved', 'delivered'):
            if not a['approval_ids']:
                findings.append(aid + ': approved/delivered needs scoped current approval')
            for ident in a['approval_ids']:
                problem = approval_gate(ident, [aid])
                if problem:
                    findings.append(aid + ': ' + problem)
        if a['state'] == 'delivered' and (not a['delivery_authority'] or not a['delivery_evidence']):
            findings.append(aid + ': delivered needs recorded action authority and delivery evidence')
        if a['state'] != 'delivered' and (a['delivery_authority'] or a['delivery_evidence']):
            findings.append(aid + ': delivery fields only belong to delivered state')
    # Findings in purported verified producers must not create a trustworthy-looking frontier.
    ready = [] if findings else [sid for sid, s in slices.items() if s['state'] in ('planned', 'active') and not gates[sid]]
    return findings, ready, {sid: why for sid, why in gates.items() if why}


def experiment_schema(data):
    obj(data, ('version', 'test_id', 'record_id', 'record_version', 'recorded_at', 'predecessor', 'execution_state', 'precommit', 'observations', 'interpretation', 'classification', 'invalidation_reason', 'next_action', 'next_owner'))
    version(data['version'])
    integer(data['record_version'], 'record_version')
    for key in ('test_id', 'record_id', 'recorded_at', 'next_action', 'next_owner'):
        string(data[key], key)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', data['recorded_at']):
        raise SchemaError('recorded_at: expected ISO timestamp with seconds, at most 6 fractional digits and timezone')
    try:   # pad the fraction to 6 digits: Python 3.9 parses only 3 or 6, later versions any count
        datetime.fromisoformat(re.sub(r'\.(\d+)', lambda m: '.' + m[1].ljust(6, '0'), data['recorded_at'].replace('Z', '+00:00')))
    except ValueError:
        raise SchemaError('recorded_at: invalid calendar date or time')
    enum(data['execution_state'], ('planned', 'completed'), 'execution_state')
    enum(data['classification'], ('not-run', 'supports', 'weakens', 'inconclusive', 'invalid'), 'classification')
    for key in ('interpretation', 'invalidation_reason'):
        string(data[key], key, True)
    obj(data['precommit'], PRECOMMIT, at='precommit')
    for key in PRECOMMIT:
        string(data['precommit'][key], 'precommit.' + key)
    obs = records(data['observations'], 'observations')
    for row in obs.values():
        obj(row, ('id', 'description', 'source'), at='observation')
        for key in ('description', 'source'):
            string(row[key], 'observation.' + key)
    if data['predecessor'] is not None:
        obj(data['predecessor'], ('record_id', 'sha256'), at='predecessor')
        string(data['predecessor']['record_id'], 'predecessor.record_id')
        if not isinstance(data['predecessor']['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', data['predecessor']['sha256']):
            raise SchemaError('predecessor.sha256: expected lowercase SHA-256 hex')


def experiment_state(data):
    findings = []
    if data['record_version'] == 1 and (data['predecessor'] is not None or data['execution_state'] != 'planned'):
        findings.append('initial record must be planned with null predecessor')
    if data['record_version'] > 1 and data['predecessor'] is None:
        findings.append('later record must identify its predecessor')
    if data['execution_state'] == 'planned':
        if data['classification'] != 'not-run' or data['observations'] or data['interpretation'] is not None or data['invalidation_reason'] is not None:
            findings.append('planned record must be not-run with no actual observations, interpretation or invalidation reason')
    else:
        if data['classification'] == 'not-run' or not data['observations'] or not data['interpretation']:
            findings.append('completed record needs observations, interpretation and a result classification')
        if data['classification'] == 'invalid' and not data['invalidation_reason']:
            findings.append('invalid result needs an exact invalidation reason')
        if data['classification'] != 'invalid' and data['invalidation_reason'] is not None:
            findings.append('invalidation reason conflicts with non-invalid classification')
    return findings


def validate_experiment(data, prior=None, prior_sha256=None):
    """Check explicit record pair. Hash refers to the prior file's exact bytes."""
    experiment_schema(data)
    findings = experiment_state(data)
    if data['record_version'] == 1:
        if data['predecessor'] is not None or prior is not None:
            findings.append('initial record must have null predecessor and no --prior')
        return findings
    if not data['predecessor'] or prior is None:
        findings.append('later record requires predecessor identity/hash and explicit --prior')
        return findings
    experiment_schema(prior)
    findings.extend('prior: ' + item for item in experiment_state(prior))
    if prior['test_id'] != data['test_id'] or prior['record_version'] + 1 != data['record_version']:
        findings.append('prior must have same test_id and exactly preceding record_version')
    if prior['record_id'] == data['record_id']:
        findings.append('successor must have a new record_id')
    if data['predecessor']['record_id'] != prior['record_id'] or data['predecessor']['sha256'] != prior_sha256:
        findings.append('predecessor identity/hash mismatch')
    if data['precommit'] != prior['precommit']:
        findings.append('precommit changed; start a new planned test lineage')
    if prior['execution_state'] == 'completed':
        if data['execution_state'] != 'completed' or data['observations'] != prior['observations']:
            findings.append('interpretation correction must retain completed raw observations and state')
        if prior['classification'] == 'invalid' and data['classification'] != 'invalid':
            findings.append('invalid completed evidence cannot be upgraded within the same lineage')
    return findings


def load_file(path):
    """Read only the explicitly supplied path; never open recorded pointers."""
    absolute = os.path.abspath(path)
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0)
    fd = os.open(absolute, flags)
    with os.fdopen(fd, 'rb') as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode):
            raise SchemaError('input must be a regular file')
        if info.st_size > MAX_BYTES:
            raise SchemaError('input exceeds 1 MiB')
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise SchemaError('input exceeds 1 MiB')
    return raw.decode('utf-8'), hashlib.sha256(raw).hexdigest()


def decode_json(text):
    def pairs(entries):
        result = {}
        for key, value in entries:
            if key in result:
                raise SchemaError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise SchemaError('nonfinite JSON value: ' + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='mode', required=True)
    for mode in ('brief', 'review', 'plan', 'experiment'):
        sub = subs.add_parser(mode)
        sub.add_argument('file')
        if mode == 'experiment':
            sub.add_argument('--prior')
    args = parser.parse_args(argv)
    try:
        text, _ = load_file(args.file)
        if args.mode in ('brief', 'review'):
            findings = validate_markdown(text, args.mode)
        elif args.mode == 'plan':
            plan = decode_json(text)
            findings, ready, blocked = validate_plan(plan)
            print('Dependency-ready from declared state: ' + (', '.join(ready) or '(none)'))
            active = [s['id'] for s in plan['slices'] if s['id'] in ready and s['state'] == 'active']
            if active:
                print('Already active among these IDs (not new dispatch): ' + ', '.join(active))
            if findings:
                print('Frontier withheld because structural findings exist.')
            for sid, reasons in blocked.items():
                print('Blocked %s: %s' % (sid, '; '.join(reasons)))
        else:
            prior, digest = None, None
            if args.prior:
                prior_text, digest = load_file(args.prior)
                prior = decode_json(prior_text)
            findings = validate_experiment(decode_json(text), prior, digest)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print('Invalid input/schema: ' + str(exc), file=sys.stderr)
        return 2
    for finding in findings:
        print('Finding: ' + finding)
    print('Structural findings.' if findings else 'Structurally consistent.')
    print('Limits: declared records only; not source truth, actual approval, authorization, execution or semantic completion.')
    return 1 if findings else 0

if __name__ == '__main__':
    sys.exit(main())
