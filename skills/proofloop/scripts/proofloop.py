#!/usr/bin/env python3
"""ProofLoop: bounded local evidence and quarantined advisory records. Python 3.9+."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import tempfile
import time

MAX_BYTES = 2 * 1024 * 1024
MAX_DEPTH = 24
MAX_INT = 9007199254740991
HIGH = {'medical', 'legal', 'financial', 'employment', 'identity', 'security-policy', 'permission'}
HIGH_ALIASES = {'health': 'medical', 'healthcare': 'medical', 'medicine': 'medical', 'law': 'legal', 'finance': 'financial', 'investment': 'financial', 'hiring': 'employment', 'recruitment': 'employment', 'identity-management': 'identity', 'security': 'security-policy', 'permissions': 'permission', 'authorization': 'permission'}

def high_domain(value):
    normalized = value.strip().lower().replace('_', '-').replace(' ', '-')
    return HIGH_ALIASES.get(normalized, normalized) in HIGH

DEFAULT_BUDGET = dict(drafts=3, executions=2, verifiers=2, tool_calls=20, minutes=30, learning_records=2, candidates=1, policy_promotions=0)
TERMINALS = {'completed_verified', 'completed_unverified', 'blocked', 'budget_exhausted', 'policy_denied', 'capability_missing', 'security_quarantine', 'cancelled'}
STATUSES = {'observation': {'recorded', 'locally_excluded'}, 'experience': {'recorded', 'locally_excluded'}, 'candidate_lesson': {'candidate', 'rejected', 'expired', 'superseded', 'locally_excluded'}, 'approved_advisory': {'approved_advisory', 'expired', 'superseded', 'locally_excluded'}, 'user_preference': {'recorded', 'superseded', 'locally_excluded'}}

class Fault(Exception):
    pass

def need(ok, message):
    if not ok:
        raise Fault(message)

def obj(v, required, optional=()):
    need(type(v) is dict and set(required) <= set(v) and set(v) <= set(required) | set(optional), 'invalid object fields')

def integer(v, minimum=0, maximum=MAX_INT):
    need(type(v) is int and minimum <= v <= maximum, 'invalid integer')

def string(v):
    need(type(v) is str and 0 < len(v) <= 16384 and '\x00' not in v, 'invalid string')

def strings(v, nonempty=False):
    need(type(v) is list and len(v) <= 1024 and (v or not nonempty), 'invalid string list')
    for s in v:
        string(s)

def digest(v):
    need(type(v) is str and re.fullmatch('[0-9a-f]{64}', v), 'invalid digest')

def typed(v, depth=0):
    need(depth <= MAX_DEPTH, 'JSON nesting limit')
    if type(v) is dict:
        need(len(v) <= 4096, 'JSON object limit')
        for k, x in v.items():
            string(k); typed(x, depth + 1)
    elif type(v) is list:
        need(len(v) <= 10000, 'JSON array limit')
        for x in v:
            typed(x, depth + 1)
    elif type(v) is int:
        integer(v, -MAX_INT)
    elif type(v) is str:
        need(len(v) <= 65536 and '\x00' not in v, 'JSON string limit')
    else:
        need(v is None or type(v) is bool, 'unsupported JSON value; use decimal strings')

def pairs(items):
    d = {}
    for k, v in items:
        need(k not in d, 'duplicate JSON key')
        d[k] = v
    return d

def parse(raw):
    need(len(raw) <= MAX_BYTES, 'JSON byte limit')
    try:
        value = json.loads(raw, object_pairs_hook=pairs)
    except (ValueError, UnicodeError, RecursionError):
        raise Fault('invalid JSON')
    typed(value)
    return value

def canon(value):
    typed(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')

def sha(value):
    return hashlib.sha256(canon(value)).hexdigest()

def now():
    return int(time.time() * 1000)

def file_sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def within(workspace, path, exists=True):
    string(workspace); string(path)
    root = Path(workspace).resolve(strict=True)
    need(root.is_dir(), 'workspace must exist')
    p = Path(path)
    if not p.is_absolute():
        p = root / p
    need(p.name != '..', 'path outside selected workspace')
    # Ordinary parent aliases are resolved; a selected leaf symlink is never followed.
    need(not p.is_symlink(), 'selected file symlink denied')
    parent = p.parent.resolve(strict=True)
    resolved = parent / p.name
    need(resolved == root or root in resolved.parents, 'path outside selected workspace')
    if exists:
        need(resolved.exists(), 'selected path missing')
    return resolved

def pin(v):
    obj(v, ['path', 'sha256']); string(v['path']); digest(v['sha256'])

def identities(c):
    out = {}
    for item in c['sources'] + c['dependencies']:
        p = within(c['workspace'], item['path'])
        out[str(p)] = file_sha(p)
    for v in c['verifiers']:
        out[v['argv'][0]] = file_sha(v['argv'][0])
        for item in v['pins']:
            p = within(c['workspace'], item['path'])
            out[str(p)] = file_sha(p)
    return out

def artifact_id(c):
    return {a: file_sha(within(c['workspace'], a)) if within(c['workspace'], a, False).is_file() else None for a in c['deliverables']}

def validate_contract(c):
    obj(c, ['version', 'run_id', 'project', 'task_id', 'goal', 'family', 'privacy_class', 'workspace', 'deliverables', 'sources', 'dependencies', 'prohibited_actions', 'allowed_actions', 'learning', 'learning_eligibility', 'storage', 'criteria', 'verifiers', 'budgets', 'deadline_ms', 'budget_scope', 'verification_plan', 'best_effort'])
    need(c['version'] == 2 and type(c['version']) is int, 'unsupported contract version')
    for k in ['run_id', 'project', 'task_id', 'goal', 'family', 'workspace']:
        string(c[k])
    assert_no_credentials(c)
    need(c['privacy_class'] in ['public', 'internal', 'confidential', 'restricted'], 'invalid privacy class')
    strings(c['deliverables'], True); strings(c['prohibited_actions']); strings(c['allowed_actions'])
    allowed = {'draft', 'execute', 'verify', 'record_observation', 'create_lesson', 'curate', 'retrieve', 'transfer'}
    need(set(c['allowed_actions']) <= allowed, 'unknown action')
    need(not set(c['allowed_actions']) & set(c['prohibited_actions']), 'action both allowed and prohibited')
    need(c['learning'] in ['none', 'ephemeral', 'workspace_ledger'], 'unsupported learning retention')
    le = c['learning_eligibility']; obj(le, ['eligible', 'excluded_domains', 'classification_ref'])
    need(type(le['eligible']) is bool, 'invalid learning eligibility'); strings(le['excluded_domains']); string(le['classification_ref'])
    need(not le['eligible'] or not le['excluded_domains'], 'contradictory learning eligibility')
    need((le['eligible'] and not le['excluded_domains'] and not high_domain(c['family'])) or c['learning'] == 'none', 'ineligible learning must be none')
    need(c['storage'] in ['transient', 'task_local'], 'unsupported storage adapter')
    need(c['learning'] != 'workspace_ledger' or c['storage'] == 'task_local', 'ledger requires local storage')
    need(c['budget_scope'] in ['adapter_only', 'global'], 'invalid budget scope')
    need(type(c['best_effort']) is bool, 'invalid best effort')
    for name in ['sources', 'dependencies', 'criteria', 'verifiers']:
        need(type(c[name]) is list and len(c[name]) <= 128, 'invalid contract list')
    for item in c['sources'] + c['dependencies']:
        pin(item)
    obj(c['budgets'], DEFAULT_BUDGET)
    for k, v in c['budgets'].items():
        integer(v, 0, 100000)
    need(c['budgets']['minutes'] > 0 and c['budgets']['policy_promotions'] == 0, 'invalid time or promotion budget')
    need(c['budgets']['candidates'] <= 1, 'at most one candidate lesson')
    integer(c['deadline_ms'], 1)
    ids = set()
    for cr in c['criteria']:
        obj(cr, ['id', 'description', 'required', 'method', 'verifier', 'predicate'])
        string(cr['id']); string(cr['description'])
        need(cr['id'] not in ids, 'duplicate criterion'); ids.add(cr['id'])
        need(type(cr['required']) is bool and cr['method'] in ['E2', 'E3', 'E4'], 'invalid criterion method')
        if cr['method'] == 'E2':
            need(cr['verifier'] is None and cr['predicate'] is None, 'E2 cannot use deterministic substitute')
        elif cr['method'] == 'E4':
            need(cr['verifier'] is None, 'E4 uses composed evidence')
            ep = cr['predicate']; obj(ep, ['components', 'held_out', 'provenance_groups', 'independence_ref'])
            strings(ep['components'], True); strings(ep['held_out'], True); string(ep['independence_ref'])
            need(len(ep['components']) >= 2 and len(set(ep['components'])) == len(ep['components']) and set(ep['held_out']) < set(ep['components']), 'E4 needs distinct repeated and held-out evidence')
            obj(ep['provenance_groups'], ep['components'])
            for group in ep['provenance_groups'].values():
                string(group)
            need(len(set(ep['provenance_groups'].values())) >= 2, 'E4 needs independent provenance groups')
        else:
            string(cr['verifier'])
            obj(cr['predicate'], ['exit_code'], ['stdout_sha256'])
            integer(cr['predicate']['exit_code'], 0, 255)
            if 'stdout_sha256' in cr['predicate']:
                digest(cr['predicate']['stdout_sha256'])
    need(any(x['required'] for x in c['criteria']), 'required criteria cannot be empty')
    by_id = {x['id']: x for x in c['criteria']}
    for cr in c['criteria']:
        if cr['method'] == 'E4':
            need(all(x in by_id and by_id[x]['method'] in ['E2', 'E3'] for x in cr['predicate']['components']), 'E4 component missing or recursive')
    vids = set()
    for v in c['verifiers']:
        obj(v, ['id', 'argv', 'executable_sha256', 'cwd', 'env', 'pins', 'configuration', 'test_data', 'timeout_ms', 'output_cap_bytes', 'containment', 'concurrent_mutation'])
        string(v['id']); need(v['id'] not in vids, 'duplicate verifier'); vids.add(v['id'])
        strings(v['argv'], True); need(os.path.isabs(v['argv'][0]), 'executable must be absolute'); digest(v['executable_sha256'])
        string(v['cwd']); obj(v['env'], [], v['env'].keys() if type(v['env']) is dict else [])
        for k, value in v['env'].items():
            string(k); need(type(value) is str, 'invalid environment')
        need(type(v['pins']) is list and len(v['pins']) > 0, 'verifier must pin local inputs')
        for p in v['pins']:
            pin(p)
        for k in ['configuration', 'test_data']:
            digest(v[k])
        integer(v['timeout_ms'], 1, 1800000); integer(v['output_cap_bytes'], 1, 1048576)
        need(v['containment'] == 'process_group' and v['concurrent_mutation'] == 'host_exclusive', 'unsupported verifier isolation requirement')
    need(all(x['method'] != 'E3' or x['verifier'] in vids for x in c['criteria']), 'missing required verifier')
    obj(c['verification_plan'], ['initial_invocations', 'repair_invocations', 'final_invocations'])
    for v in c['verification_plan'].values():
        integer(v, 0, 100000)
    n = sum(c['verification_plan'].values())
    needed = {x['id'] for x in c['criteria'] if x['required']}
    for x in c['criteria']:
        if x['required'] and x['method'] == 'E4':
            needed.update(x['predicate']['components'])
    required_v = {x['verifier'] for x in c['criteria'] if x['id'] in needed and x['method'] == 'E3'}
    need(n >= len(required_v) and n <= c['budgets']['verifiers'] and n <= c['budgets']['tool_calls'], 'infeasible verification plan')
    return c

def check_action(c, action):
    validate_contract(c); string(action)
    known = {'draft', 'execute', 'verify', 'record_observation', 'create_lesson', 'curate', 'retrieve', 'transfer'}
    need(action in known, 'unknown action denied')
    need(action in c['allowed_actions'] and action not in c['prohibited_actions'], 'policy_denied')
    need(action not in {'create_lesson', 'curate', 'retrieve', 'transfer'} or c['learning'] != 'none', 'ineligible_learning_disabled')
    return {'eligible': True, 'human_authorization': 'host_must_check_current_request'}

def assert_pins(c, actual):
    for p in c['sources'] + c['dependencies']:
        need(actual[str(within(c['workspace'], p['path']))] == p['sha256'], 'source or dependency changed')
    for v in c['verifiers']:
        need(actual[v['argv'][0]] == v['executable_sha256'], 'verifier executable changed')
        for p in v['pins']:
            need(actual[str(within(c['workspace'], p['path']))] == p['sha256'], 'verifier input changed')
    return actual

def fresh_pins(c):
    return assert_pins(c, identities(c))

def input_snapshot(c):
    # Settlement/report must remain available after dispatched inputs drift or disappear.
    actual = {}
    try:
        actual = identities(c)
        assert_pins(c, actual)
        return actual, True
    except (Fault, OSError):
        return actual, False

def state_digest(s):
    return sha({k: v for k, v in s.items() if k != 'digest'})

def seal(s):
    s['digest'] = state_digest(s)
    return s

def validate_state(s):
    obj(s, ['version', 'generation', 'digest', 'contract', 'contract_digest', 'started_ms', 'last_ms', 'deadline_ms', 'revision', 'spent', 'operations', 'observations', 'lessons', 'history', 'derivatives'])
    need(s['version'] == 2, 'unsupported state version'); integer(s['generation'], 1); digest(s['digest'])
    need(state_digest(s) == s['digest'], 'state digest mismatch')
    validate_contract(s['contract']); need(sha(s['contract']) == s['contract_digest'], 'contract changed')
    need(type(s['operations']) is list and type(s['observations']) is list and type(s['lessons']) is list, 'invalid state collections')
    for k in ['started_ms', 'last_ms', 'deadline_ms', 'revision']:
        integer(s[k])
    obj(s['spent'], ['drafts', 'executions', 'verifiers', 'tool_calls', 'learning_records', 'candidates', 'policy_promotions'])
    for v in s['spent'].values():
        integer(v)
    need(s['contract']['learning'] == 'workspace_ledger' or not s['lessons'], 'learning retention mismatch')
    for key, value in s['spent'].items():
        need(value <= s['contract']['budgets'][key], 'stored budget exceeded')
    for r in s['lessons']:
        validate_record(r)
    return s

class Store:
    def __init__(self, envelope, create=False):
        self.e = envelope; self.create = create; self.path = None; self.lock = None; self.fd = None
        self.state = None
    def __enter__(self):
        try:
            return self.enter()
        except BaseException:
            self.__exit__()
            raise
    def enter(self):
        e = self.e
        integer(e['expected_generation']); need(e['expected_digest'] is None or type(e['expected_digest']) is str, 'invalid expected digest')
        if 'store' in e:
            self.path = within(e['workspace'], e['store'], not self.create)
            need(not self.create or not self.path.exists(), 'store already exists')
            need(os.name == 'posix', 'capability_missing: local ledger requires POSIX atomic replace and directory fsync')
            self.lock = Path(str(self.path) + '.lock')
            try:
                self.fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                raise Fault('writer lock exists; explicit operator recovery required')
            os.write(self.fd, b'ProofLoop exclusive writer; do not break automatically\n'); os.fsync(self.fd)
            if not self.create:
                self.state = validate_state(parse(self.path.read_bytes()))
        elif not self.create:
            self.state = validate_state(copy.deepcopy(e['state']))
        if self.state is not None:
            need(self.state['generation'] == e['expected_generation'] and self.state['digest'] == e['expected_digest'], 'stale generation or digest')
            need(Path(self.state['contract']['workspace']).resolve() == Path(e['workspace']).resolve(), 'workspace mismatch')
        else:
            need(e['expected_generation'] == 0 and e['expected_digest'] is None, 'init expected generation must be zero')
        return self
    def commit(self, s, event):
        s['last_ms'] = max(s['last_ms'], now())
        s['generation'] += 1
        s['history'].append({'generation': s['generation'], 'event': event, 'at_ms': now()})
        seal(s); raw = canon(s); need(len(raw) <= MAX_BYTES, 'state capacity reached')
        if self.path is not None:
            fd, name = tempfile.mkstemp(prefix='.' + self.path.name + '.', dir=str(self.path.parent))
            try:
                with os.fdopen(fd, 'wb') as f:
                    f.write(raw); f.flush(); os.fsync(f.fileno())
                os.replace(name, self.path)
                d = os.open(self.path.parent, os.O_RDONLY)
                try:
                    os.fsync(d)
                finally:
                    os.close(d)
            finally:
                if os.path.exists(name):
                    os.unlink(name)
        self.state = s
        return s
    def __exit__(self, *args):
        if self.fd is not None:
            os.close(self.fd)
            os.unlink(self.lock)

def load_state(e):
    if 'store' in e:
        s = validate_state(parse(within(e['workspace'], e['store']).read_bytes()))
    else:
        s = validate_state(e['state'])
    need(Path(e['workspace']).resolve() == Path(s['contract']['workspace']).resolve(), 'workspace mismatch')
    return s

def init(e):
    c = validate_contract(e['payload']); need(c['workspace'] == e['workspace'], 'workspace mismatch')
    need((c['storage'] == 'task_local') == ('store' in e), 'storage selection mismatch')
    fresh_pins(c)
    t = now(); need(c['deadline_ms'] > t, 'deadline expired')
    s = dict(version=2, generation=0, digest='', contract=c, contract_digest=sha(c), started_ms=t, last_ms=t, deadline_ms=min(c['deadline_ms'], t + c['budgets']['minutes'] * 60000), revision=0, spent={k: 0 for k in DEFAULT_BUDGET if k != 'minutes'}, operations=[], observations=[], lessons=[], history=[], derivatives=[])
    with Store(e, True) as st:
        return st.commit(s, 'init')

def clock_check(s):
    t = now()
    need(t >= s['last_ms'], 'clock rollback blocks dispatch')
    need(t < s['deadline_ms'], 'budget_exhausted: deadline')
    need(s['contract']['budget_scope'] == 'adapter_only', 'capability_missing: global calls cannot be observed')
    s['last_ms'] = t


def reserve(s, p, internal=False):
    obj(p, ['operation_id', 'run_id', 'kind', 'revision'], ['verifier'])
    string(p['operation_id']); integer(p['revision'], 1)
    need(p['run_id'] == s['contract']['run_id'], 'wrong run receipt')
    need(not any(o['operation_id'] == p['operation_id'] for o in s['operations']), 'reused operation id')
    need(p['kind'] in ['draft', 'execute', 'verify', 'observe'], 'unknown operation')
    need(p['kind'] != 'verify' or internal, 'verifier reservations are owned by verify')
    check_action(s['contract'], {'observe': 'record_observation'}.get(p['kind'], p['kind']))
    fresh_pins(s['contract'])
    clock_check(s)
    if p['kind'] == 'draft':
        need(p['revision'] == s['revision'] + 1, 'draft revision must increase by one')
    else:
        need(p['revision'] == s['revision'] and s['revision'] > 0, 'candidate revision mismatch')
    charges = {'tool_calls': 1}
    key = {'draft': 'drafts', 'execute': 'executions', 'verify': 'verifiers'}.get(p['kind'])
    if key:
        charges[key] = 1
    for key, n in charges.items():
        need(s['spent'][key] + n <= s['contract']['budgets'][key], 'budget_exhausted: ' + key)
    if p['kind'] == 'execute' and s['spent']['drafts'] >= s['contract']['budgets']['drafts']:
        gates = [x for x in aggregate(s)['criteria'] if x['method'] == 'E3' and x['required']]
        need(s['contract']['best_effort'] and gates and all(x['passed'] for x in gates), 'capped draft requires best effort and complete deterministic gate')
    for key, n in charges.items():
        s['spent'][key] += n
    if p['kind'] == 'draft':
        s['revision'] = p['revision']
    op = dict(p, status='pending', reserved_ms=now(), charges=charges, artifacts=artifact_id(s['contract']), inputs=identities(s['contract']))
    s['operations'].append(op)
    return op

def record_step(s, p):
    obj(p, ['run_id', 'operation_id', 'revision', 'outcome', 'observations'])
    need(p['run_id'] == s['contract']['run_id'], 'wrong run or revision receipt')
    # A reservation stays settleable after a later draft; its observations keep the reserved revision.
    op = next((x for x in s['operations'] if x['operation_id'] == p['operation_id']), None)
    need(op is not None and op['revision'] == p['revision'] and op['status'] == 'pending' and op['kind'] != 'verify', 'missing or reused receipt')
    need(p['outcome'] in ['completed', 'failed', 'interrupted', 'unknown'], 'invalid outcome')
    need(type(p['observations']) is list, 'invalid observations')
    current_inputs, pins_match = input_snapshot(s['contract'])
    for o in p['observations']:
        obj(o, ['criterion', 'passed', 'method', 'decision_ref', 'limits'])
        cr = next((x for x in s['contract']['criteria'] if x['id'] == o['criterion']), None)
        need(cr is not None and type(o['passed']) is bool, 'unknown criterion or invalid result')
        need(o['method'] in ['E0', 'E1', 'E2', 'E3', 'E4'], 'invalid evidence kind')
        strings(o['limits']); string(o['decision_ref'])
        o = copy.deepcopy(o)
        if not pins_match:
            o['limits'].append('Frozen input identities changed or unavailable; observation cannot certify this contract.')
        s['observations'].append(dict(o, contract_pins_match=pins_match, provenance='host_declared' if o['method'] == 'E2' else 'imported_unverified', revision=op['revision'], operation_id=op['operation_id'], artifacts=artifact_id(s['contract']), inputs=current_inputs))
    op['status'] = p['outcome']; op['recorded_ms'] = now()


def capture(c, v, remaining):
    need(os.name == 'posix' and hasattr(os, 'killpg'), 'capability_missing: process-group termination')
    before = fresh_pins(c); arts = artifact_id(c)
    cwd = within(c['workspace'], v['cwd']); need(cwd.is_dir(), 'verifier cwd missing')
    start = time.monotonic(); cap = v['output_cap_bytes']; buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    timed_out = False; truncated = False
    proc = subprocess.Popen(v['argv'], cwd=str(cwd), env=v['env'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, start_new_session=True)
    sel = selectors.DefaultSelector()
    for key, f in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
        os.set_blocking(f.fileno(), False); sel.register(f, selectors.EVENT_READ, key)
    duration = min(v['timeout_ms'], remaining) / 1000
    try:
        while sel.get_map():
            if time.monotonic() - start >= duration:
                timed_out = True; break
            for key, _ in sel.select(min(0.05, max(0, duration - (time.monotonic() - start)))):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    sel.unregister(key.fileobj); continue
                available = cap - sum(len(b) for b in buffers.values())
                buffers[key.data].extend(chunk[:available])
                if len(chunk) > available:
                    truncated = True; break
            if truncated:
                break
        if not timed_out and not truncated:
            try:
                proc.wait(timeout=max(0.001, duration - (time.monotonic() - start)))
            except subprocess.TimeoutExpired:
                timed_out = True
    finally:
        # Kill the owned group even when the leader exited: inherited pipes/children may remain.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait(); sel.close(); proc.stdout.close(); proc.stderr.close()
    after = identities(c)
    stable = before == after and arts == artifact_id(c)
    return dict(exit_code=proc.returncode, signal=-proc.returncode if proc.returncode < 0 else None, elapsed_ms=int((time.monotonic() - start) * 1000), timed_out=timed_out, truncated=truncated, stdout_sha256=hashlib.sha256(buffers['stdout']).hexdigest(), stderr_sha256=hashlib.sha256(buffers['stderr']).hexdigest(), captured_bytes=sum(len(b) for b in buffers.values()), inputs=before, end_inputs=after, artifacts=arts, stable=stable, raw_output_retained=False, boundary='before/after equality; host-exclusive inputs required; no OS sandbox or change-and-revert proof')

def verify(e):
    need('store' in e, 'blocked: capture requires authorized task-local evidence storage')
    with Store(e) as st:
        s = st.state; p = e['payload']; obj(p, ['operation_id', 'run_id', 'revision', 'verifier'])
        v = next((x for x in s['contract']['verifiers'] if x['id'] == p['verifier']), None)
        need(v is not None, 'unknown verifier'); fresh_pins(s['contract'])
        need(within(s['contract']['workspace'], v['cwd']).is_dir(), 'verifier cwd missing')
        need(os.name == 'posix' and hasattr(os, 'killpg'), 'capability_missing')
        op = reserve(s, dict(p, kind='verify'), True)
        st.commit(s, 'reserve verifier')
        try:
            result = capture(s['contract'], v, s['deadline_ms'] - now())
        except (OSError, Fault):
            op['status'] = 'unknown'; st.commit(s, 'verifier failed to capture'); raise Fault('verifier capture unavailable; reservation consumed')
        op['capture'] = result; op['status'] = 'completed'
        for cr in s['contract']['criteria']:
            if cr['method'] != 'E3' or cr['verifier'] != v['id']:
                continue
            pred = cr['predicate']
            passed = result['stable'] and not result['timed_out'] and not result['truncated'] and result['exit_code'] == pred['exit_code']
            if 'stdout_sha256' in pred:
                passed = passed and result['stdout_sha256'] == pred['stdout_sha256']
            s['observations'].append(dict(criterion=cr['id'], passed=passed, method='E3', provenance='captured_local', revision=s['revision'], operation_id=p['operation_id'], artifacts=result['artifacts'], inputs=result['inputs'], limits=[result['boundary']]))
        return st.commit(s, 'record verifier capture')

def aggregate(s):
    c = s['contract']; current, pins_match = input_snapshot(c); arts = artifact_id(c); result = []
    for cr in c['criteria']:
        obs = [o for o in s['observations'] if o['criterion'] == cr['id']]
        latest = obs[-1] if obs else None
        fresh = bool(pins_match and latest and latest.get('contract_pins_match', True) and latest['revision'] == s['revision'] and latest['inputs'] == current and latest['artifacts'] == arts)
        acceptable = bool(latest and ((cr['method'] == 'E3' and latest['method'] == 'E3' and latest['provenance'] == 'captured_local') or (cr['method'] == 'E2' and latest['method'] == 'E2' and latest['provenance'] == 'host_declared')))
        result.append(dict(id=cr['id'], required=cr['required'], method=cr['method'], passed=bool(latest and latest['passed'] and fresh and acceptable), fresh=fresh, evidence=latest, history_count=len(obs)))
    by_id = {x['id']: x for x in result}
    for cr in c['criteria']:
        if cr['method'] == 'E4':
            entry = by_id[cr['id']]; components = [by_id[x] for x in cr['predicate']['components']]
            entry['passed'] = all(x['passed'] for x in components); entry['fresh'] = all(x['fresh'] for x in components)
            entry['evidence'] = {'composition': cr['predicate'], 'independence': 'host-declared; actual provenance independence must be checked by host'}
    success = all(x['passed'] for x in result if x['required']) and not any(o['status'] in ['pending', 'unknown'] for o in s['operations'])
    return dict(task_outcome='completed_verified' if success else 'completed_unverified', criteria=result, evidence_authentication='E2 is host-declared; host must authenticate actual current decision', spent=s['spent'], external_tool_calls='unknown', storage=c['storage'], learning_status='ineligible_learning_disabled' if c['learning'] == 'none' else c['learning'], pending_operations=[o['operation_id'] for o in s['operations'] if o['status'] == 'pending'], deadline_ms=s['deadline_ms'], artifacts=arts)


def validate_record(r):
    obj(r, ['version', 'id', 'revision', 'type', 'status', 'project', 'task_id', 'family', 'privacy_class', 'scope', 'created_ms', 'expires_ms', 'provenance', 'content', 'dependencies', 'privacy_review'], ['approval'])
    need(type(r['version']) is int and r['version'] == 2, 'legacy version requires explicit conversion preview')
    string(r['id']); integer(r['revision'], 1)
    need(r['type'] in STATUSES and r['status'] in STATUSES[r['type']], 'invalid lifecycle pair')
    need(r['privacy_class'] in ['public', 'internal', 'confidential', 'restricted'], 'invalid record privacy class')
    for k in ['project', 'task_id', 'family']:
        string(r[k])
    need(not high_domain(r['family']), 'ineligible learning record')
    strings(r['scope'], True); integer(r['created_ms'], 1)
    if r['expires_ms'] is not None:
        integer(r['expires_ms'], r['created_ms'] + 1)
    need(r['provenance'] in ['local', 'imported_quarantined'], 'invalid record provenance')
    strings(r['dependencies']); need(r['privacy_review'] in ['pending', 'host_reviewed'], 'invalid privacy review')
    common = ['result', 'limits']
    fields = {'observation': common, 'experience': common, 'candidate_lesson': ['trigger', 'method', 'applicability', 'exceptions', 'disconfirming_evidence', 'benefit_hypothesis', 'reuse_check', 'key', 'value'], 'approved_advisory': ['trigger', 'method', 'applicability', 'exceptions', 'disconfirming_evidence', 'benefit_hypothesis', 'reuse_check', 'key', 'value'], 'user_preference': ['quote', 'selection_ref', 'key', 'value']}[r['type']]
    obj(r['content'], fields)
    for value in r['content'].values():
        string(value)
    if 'approval' in r:
        obj(r['approval'], ['decision_ref', 'source_digest']); string(r['approval']['decision_ref']); digest(r['approval']['source_digest'])
        need(r['provenance'] == 'local' and r['type'] == 'approved_advisory', 'imported approval denied')
    need(r['type'] != 'approved_advisory' or 'approval' in r, 'advisory requires transition binding')
    return r

SECRET_KEY = re.compile(r'(password|secret|token|api.?key|credential)', re.I)
EXTRA_SECRETS = [re.compile(r'(?i)Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/-]{8,}'), re.compile(r'\bAKIA[0-9A-Z]{16}\b'), re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----'), re.compile(r'[A-Za-z]:\\(?:Users|Documents and Settings)\\[^\s]+')]
LOCAL_PATH = re.compile(r'(?<![:/\w])/(?:[A-Za-z0-9._~-]+/)*[A-Za-z0-9._~-]+|[A-Za-z]:\\[^\s]+')
SECRET_TEXT = re.compile(r'(?i)(?:\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b(?:sk-|ghp_)[A-Za-z0-9_-]{8,}\b|(?:/Users/|/home/|/workspace/)[^\s"\x27]+)')

def assert_no_credentials(value):
    if type(value) is dict:
        for key, item in value.items():
            need(not SECRET_KEY.search(key), 'security_quarantine: credential-bearing configuration forbidden')
            assert_no_credentials(item)
    elif type(value) is list:
        for item in value:
            assert_no_credentials(item)
    elif type(value) is str:
        need(not any(p.search(value) for p in EXTRA_SECRETS[:3]) and not re.search(r'\b(?:sk-|ghp_)[A-Za-z0-9_-]{8,}', value), 'security_quarantine: credential-bearing configuration forbidden')


def redact(value):
    count = [0]
    def walk(v):
        if type(v) is dict:
            out = {}
            for k, x in v.items():
                if SECRET_KEY.search(k):
                    out[k] = '[REDACTED]'; count[0] += 1
                else:
                    out[k] = walk(x)
            return out
        if type(v) is list:
            return [walk(x) for x in v]
        if type(v) is str:
            x, n = SECRET_TEXT.subn('[REDACTED]', v); count[0] += n
            for pattern in EXTRA_SECRETS + [LOCAL_PATH]:
                x, n = pattern.subn('[REDACTED]', x); count[0] += n
            return x
        return v
    safe = walk(copy.deepcopy(value))
    return safe, count[0]

def safe_record(r):
    validate_record(r); safe, n = redact(r)
    need(n == 0, 'security_quarantine: redact and review exact safe revision first')
    need(r['privacy_review'] == 'host_reviewed', 'privacy review required')
    return safe

def active(r):
    return r['status'] in ['candidate', 'approved_advisory', 'recorded'] and (r['expires_ms'] is None or now() < r['expires_ms'])

def conflicts(records):
    for r in records:
        validate_record(r)
    found = []
    for i, a in enumerate(records):
        for b in records[i + 1:]:
            if a['project'] != b['project'] or not active(a) or not active(b) or not set(a['scope']) & set(b['scope']):
                continue
            if 'key' in a['content'] and a['content'].get('key') == b['content'].get('key') and a['content']['value'] != b['content']['value']:
                found.append([a['id'], b['id']])
    return {'structured_conflicts': found, 'semantic_review': 'required; no semantic completeness claim'}

def decision(d, r, action, c):
    obj(d, ['action', 'record_id', 'revision', 'safe_digest', 'project', 'task_id', 'decision_ref'])
    string(d['decision_ref'])
    need(d['action'] == action and d['record_id'] == r['id'] and d['revision'] == r['revision'] and d['safe_digest'] == sha(r) and d['project'] == c['project'] and d['task_id'] == c['task_id'], 'decision does not bind exact safe content and current scope')

def preview(r):
    safe_record(r)
    return {'record': r, 'safe_digest': sha(r), 'effective_status': r['status'] if active(r) else 'inactive', 'human_authentication': 'not performed'}

def transition(s, p):
    obj(p, ['record', 'decision', 'action'], ['predecessor_digest'])
    c = s['contract']; check_action(c, 'create_lesson' if p['action'] == 'add' else 'curate')
    need(c['learning'] == 'workspace_ledger', 'durable lessons require workspace_ledger; ephemeral lessons stay session-only')
    r = safe_record(copy.deepcopy(p['record'])); action = p['action']
    need(r['project'] == c['project'] and r['family'] == c['family'], 'cross-scope lesson')
    decision(p['decision'], r, action, c)
    old = next((x for x in s['lessons'] if x['id'] == r['id']), None)
    if action == 'add':
        clock_check(s); need(r['task_id'] == c['task_id'], 'new record task mismatch')
        need(old is None and r['revision'] == 1 and r['type'] != 'approved_advisory', 'invalid new lesson')
        need(s['spent']['learning_records'] < c['budgets']['learning_records'], 'learning record budget exhausted')
        if r['type'] == 'candidate_lesson':
            need(s['spent']['candidates'] < c['budgets']['candidates'], 'candidate budget exhausted'); s['spent']['candidates'] += 1
        s['spent']['learning_records'] += 1
    elif action == 'revise':
        need(old is not None and p.get('predecessor_digest') == sha(old) and r['revision'] == old['revision'] + 1, 'stale predecessor revision')
        need(r['type'] in ['candidate_lesson', 'user_preference', 'experience', 'observation'] and 'approval' not in r, 'revision cannot inherit approval')
        need(old['type'] == r['type'] or (old['type'] == 'approved_advisory' and r['type'] == 'candidate_lesson'), 'revision type mismatch')
        need(active(old), 'inactive record cannot be revised')
        if r['type'] == 'user_preference':
            need(set(r['scope']) <= set(old['scope']), 'preference revision must narrow scope')
        s['history'].append({'event': 'prior record revision', 'record': old}); s['lessons'].remove(old)
        for view in s['derivatives']:
            view['valid'] = False
    else:
        need(old is not None and sha(old) == sha(r), 'stale record revision')
        need(action in ['approve', 'reject', 'expire', 'supersede', 'exclude'], 'unknown transition')
        need(action == 'exclude' or active(r), 'inactive record cannot transition')
        if action == 'approve':
            need(r['type'] == 'candidate_lesson' and r['provenance'] == 'local', 'only local candidate may be curated')
            need(not conflicts(s['lessons'])['structured_conflicts'], 'unresolved structured conflict')
            r['type'] = 'approved_advisory'; r['status'] = 'approved_advisory'; r['approval'] = {'decision_ref': p['decision']['decision_ref'], 'source_digest': sha(old)}
        else:
            status = {'reject': 'rejected', 'expire': 'expired', 'supersede': 'superseded', 'exclude': 'locally_excluded'}[action]
            need(status in STATUSES[r['type']], 'invalid transition for record type'); r['status'] = status
            r.pop('approval', None)
            # Inactive advisory retains provenance binding for schema/history, not active consent.
            if r['type'] == 'approved_advisory':
                r['approval'] = old['approval']
        r['revision'] += 1
        s['history'].append({'event': 'prior record revision', 'record': old})
        s['lessons'].remove(old)
        for view in s['derivatives']:
            view['valid'] = False
    validate_record(r); s['lessons'].append(r)
    return r

def retrieve(s, p):
    obj(p, ['record_id', 'decision', 'scope', 'dependencies'])
    check_action(s['contract'], 'retrieve'); strings(p['scope'], True); strings(p['dependencies'])
    r = next((x for x in s['lessons'] if x['id'] == p['record_id']), None)
    need(r is not None, 'record missing'); safe_record(r)
    need(r['project'] == s['contract']['project'] and r['family'] == s['contract']['family'] and r['provenance'] == 'local' and r['type'] in ['approved_advisory', 'user_preference'] and active(r), 'retrieval ineligible')
    need(set(p['scope']) <= set(r['scope']) and p['dependencies'] == r['dependencies'], 'scope or dependency mismatch')
    need(not conflicts(s['lessons'])['structured_conflicts'], 'unresolved structured conflict')
    fresh_pins(s['contract'])
    available = {x['sha256'] for x in s['contract']['sources'] + s['contract']['dependencies']}
    need(set(r['dependencies']) <= available, 'lesson dependencies not bound to current sources')
    decision(p['decision'], r, 'retrieve', s['contract'])
    return {'record': r, 'digest': sha(r), 'generation': s['generation'], 'state_digest': s['digest'], 'consistency_only': True, 'host_must_authenticate_current_permission': True}


def transfer_preview(p):
    obj(p, ['records', 'destination_project']); string(p['destination_project'])
    need(type(p['records']) is list and p['records'], 'empty transfer')
    records = []
    for source in p['records']:
        r = copy.deepcopy(validate_record(source)); r.pop('approval', None)
        if r['type'] == 'approved_advisory':
            r['type'] = 'candidate_lesson'; r['status'] = 'candidate'
        r['provenance'] = 'imported_quarantined'; r['privacy_review'] = 'pending'; r['project'] = p['destination_project']; r['revision'] = 1
        r, _ = redact(r); validate_record(r); records.append(r)
    need(len({r['id'] for r in records}) == len(records), 'duplicate transfer id')
    bundle = dict(version=2, destination_project=p['destination_project'], records=records)
    return {'bundle': bundle, 'bundle_digest': sha(bundle), 'conflicts': conflicts(records), 'authority': 'none; local preview only'}

def transfer_apply(s, p):
    obj(p, ['bundle', 'bundle_digest', 'decision_ref', 'destination_project'])
    check_action(s['contract'], 'transfer'); string(p['decision_ref'])
    need(s['contract']['learning'] == 'workspace_ledger', 'transfer needs approved local ledger')
    digest(p['bundle_digest']); need(sha(p['bundle']) == p['bundle_digest'], 'bundle digest mismatch')
    b = p['bundle']; obj(b, ['version', 'destination_project', 'records'])
    need(b['version'] == 2 and b['destination_project'] == p['destination_project'] == s['contract']['project'], 'wrong transfer destination')
    need(type(b['records']) is list and b['records'], 'empty transfer')
    existing = {r['id'] for r in s['lessons']}
    for r in b['records']:
        validate_record(r)
        need(r['id'] not in existing and r['project'] == s['contract']['project'] and r['family'] == s['contract']['family'] and r['provenance'] == 'imported_quarantined' and r['privacy_review'] == 'pending' and 'approval' not in r and r['type'] != 'approved_advisory', 'invalid imported quarantine')
        need(redact(r)[1] == 0, 'unsafe import'); existing.add(r['id'])
    clock_check(s)
    n = len(b['records']); candidates = sum(r['type'] == 'candidate_lesson' for r in b['records'])
    need(s['spent']['learning_records'] + n <= s['contract']['budgets']['learning_records'] and s['spent']['candidates'] + candidates <= s['contract']['budgets']['candidates'], 'import budget exhausted')
    s['spent']['learning_records'] += n; s['spent']['candidates'] += candidates; s['lessons'].extend(b['records'])
    return {'imported': n, 'quarantined': True, 'outside_copies': 'unknown'}


def compare_cases(p):
    obj(p, ['cases']); need(type(p['cases']) is list and p['cases'], 'empty comparison')
    out = []; ids = set()
    for case in p['cases']:
        obj(case, ['id', 'actual', 'expected']); string(case['id']); need(case['id'] not in ids, 'duplicate case'); ids.add(case['id'])
        out.append({'id': case['id'], 'matched': canon(case['actual']) == canon(case['expected'])})
    return {'kind': 'supplied_comparison_not_executed_tests', 'cases': out, 'all_matched': all(x['matched'] for x in out)}

def audit_summary(p):
    obj(p, ['selection', 'pairs', 'controls', 'incidents', 'reviewer_disagreement'])
    sel = p['selection']; obj(sel, ['ids', 'start_ms', 'end_ms', 'family', 'metric', 'missingness'])
    strings(sel['ids'], True); need(len(sel['ids']) == len(set(sel['ids'])), 'duplicate selected pair'); integer(sel['start_ms']); integer(sel['end_ms'], sel['start_ms']); string(sel['family'])
    need(not high_domain(sel['family']), 'ineligible learning audit'); need(sel['metric'] in ['errors', 'errors_then_latency'] and sel['missingness'] == 'indeterminate', 'unsupported audit plan')
    need(type(p['pairs']) is list and {x.get('id') for x in p['pairs']} == set(sel['ids']) and len(p['pairs']) == len(sel['ids']), 'pair selection mismatch')
    categories = dict(helpful=0, neutral=0, harmful=0, indeterminate=0, incomparable=0); results = []
    identity_keys = ['contract', 'artifact_spec', 'verifier', 'configuration', 'test_data', 'environment', 'budget', 'criteria', 'source', 'work']
    for pair in p['pairs']:
        obj(pair, ['id', 'at_ms', 'family', 'without', 'with', 'independence', 'provenance'])
        integer(pair['at_ms'], sel['start_ms'], sel['end_ms']); need(pair['family'] == sel['family'], 'pair family mismatch')
        need(pair['provenance'] in ['supplied', 'imported'], 'invalid pair provenance'); string(pair['independence'])
        for side in [pair['without'], pair['with']]:
            obj(side, ['identities', 'required_pass', 'errors', 'latency_ms', 'cost_decimal'])
            obj(side['identities'], identity_keys)
            for v in side['identities'].values():
                digest(v)
            need(side['required_pass'] is None or type(side['required_pass']) is bool, 'invalid quality gate')
            for key in ['errors', 'latency_ms']:
                if side[key] is not None:
                    integer(side[key])
            need(side['cost_decimal'] is None or (type(side['cost_decimal']) is str and re.fullmatch(r'\d+(\.\d+)?', side['cost_decimal'])), 'invalid cost decimal')
        a, b = pair['without'], pair['with']
        if a['identities'] != b['identities']:
            cat = 'incomparable'
        elif any(x[k] is None for x in [a, b] for k in ['required_pass', 'errors']):
            cat = 'indeterminate'
        elif a['required_pass'] != b['required_pass']:
            cat = 'helpful' if b['required_pass'] else 'harmful'
        elif b['errors'] != a['errors']:
            cat = 'helpful' if b['errors'] < a['errors'] and b['required_pass'] else 'harmful' if b['errors'] > a['errors'] else 'indeterminate'
        elif not b['required_pass']:
            cat = 'neutral'
        elif sel['metric'] == 'errors':
            cat = 'neutral'
        elif a['latency_ms'] is None or b['latency_ms'] is None:
            cat = 'indeterminate'
        else:
            cat = 'helpful' if b['latency_ms'] < a['latency_ms'] else 'harmful' if b['latency_ms'] > a['latency_ms'] else 'neutral'
        categories[cat] += 1; results.append({'id': pair['id'], 'category': cat})
    need(type(p['controls']) is list and type(p['incidents']) is list and type(p['reviewer_disagreement']) is list, 'invalid audit annotations')
    selected = len(results); comparable = selected - categories['incomparable']; determinate = comparable - categories['indeterminate']
    return dict(kind='read_only_supplied_outcome_audit', metric=sel['metric'], missing_latency=sum(x[k]['latency_ms'] is None for x in p['pairs'] for k in ['without', 'with']), counts=categories, denominators=dict(selected=selected, comparable=comparable, determinate=determinate), pairs=results, controls=p['controls'], incidents=p['incidents'], reviewer_disagreement=p['reviewer_disagreement'], missing_cost=sum(x[k]['cost_decimal'] is None for x in p['pairs'] for k in ['without', 'with']), evidence='exploratory' if comparable < 20 else 'sample_size_alone_is_not_proof', provenance='declared_not_authenticated', limitations=['No causal or independent benefit proof', 'Zero supplied incidents is limited to selected cases', 'No probes, record correction or external writes'])


def validate_legacy(r):
    need(type(r) is dict, 'invalid legacy record')
    for k in ['schema_version', 'record_id', 'record_type', 'status', 'created_at', 'task_id', 'privacy_class', 'scope', 'content', 'provenance']:
        need(k in r, 'missing legacy field')
    need(r['schema_version'] == '1.0' and r['record_type'] in STATUSES, 'unsupported legacy record')
    for k in ['record_id', 'status', 'created_at', 'task_id']:
        string(r[k])
    need(r['privacy_class'] in ['public', 'internal', 'confidential', 'restricted'] and type(r['scope']) is dict and type(r['provenance']) is list, 'invalid legacy shape')
    from datetime import datetime
    try:
        date = datetime.fromisoformat(r['created_at'].replace('Z', '+00:00'))
        need(date.tzinfo is not None, 'legacy timestamp timezone required')
    except ValueError:
        raise Fault('invalid legacy timestamp')
    return r


def dispatch(command, e):
    if command == ('contract', 'validate'):
        return {'valid': True, 'contract_digest': sha(validate_contract(e))}
    if command == ('contract', 'check-action'):
        obj(e, ['contract', 'action']); return check_action(e['contract'], e['action'])
    if command == ('contract', 'init'):
        return init(e)
    if command == ('verify',):
        return verify(e)
    if command == ('report',):
        result = aggregate(load_state(e))
        if 'terminal' in e:
            need(e['terminal'] in TERMINALS - {'completed_verified'}, 'invalid requested terminal')
            result['task_outcome'] = e['terminal']
        return result
    if command in [('step', 'reserve'), ('step', 'record'), ('lesson', 'transition'), ('transfer', 'apply')]:
        with Store(e) as st:
            s = st.state
            if command == ('step', 'reserve'):
                reserve(s, e['payload'])
            elif command == ('step', 'record'):
                record_step(s, e['payload'])
            elif command == ('lesson', 'transition'):
                transition(s, e['payload'])
            else:
                transfer_apply(s, e['payload'])
            return st.commit(s, ' '.join(command))
    if command == ('lesson', 'validate'):
        if type(e) is dict and 'legacy' in e:
            obj(e, ['legacy', 'proposed']); legacy = e['legacy']; proposed = e['proposed']
            validate_legacy(legacy); validate_record(proposed)
            need(proposed['id'] == legacy['record_id'] and proposed['task_id'] == legacy['task_id'] and proposed['privacy_class'] == legacy['privacy_class'], 'legacy identity mapping mismatch')
            need(proposed['provenance'] == 'imported_quarantined' and proposed['privacy_review'] == 'pending' and proposed['revision'] == 1 and proposed['type'] != 'approved_advisory' and 'approval' not in proposed, 'legacy conversion cannot inherit trust')
            return {'valid': True, 'conversion_preview': proposed, 'safe_digest': sha(proposed), 'inherited_trust': False, 'source_digest': sha(legacy), 'semantic_mapping': 'host must inspect; no automatic content equivalence claim'}
        if type(e) is dict and e.get('schema_version') == '1.0':
            validate_legacy(e)
            return {'valid': False, 'legacy_valid': True, 'conversion_preview_required': True, 'inherited_trust': False, 'required_input': 'legacy plus complete proposed version2 record; exact identity preserved, quarantined'}
        validate_record(e); return {'valid': True, 'digest': sha(e)}
    if command == ('lesson', 'identity'):
        return {'sha256': sha(validate_record(e)), 'identity_only': True}
    if command == ('lesson', 'redact-preview'):
        validate_record(e); safe, n = redact(e)
        if n:
            safe['revision'] += 1; safe['privacy_review'] = 'pending'; safe.pop('approval', None)
            if safe['type'] == 'approved_advisory':
                safe['type'] = 'candidate_lesson'; safe['status'] = 'candidate'
        return {'record': safe, 'safe_digest': sha(safe), 'transformations': n, 'residual_risk': 'Pattern matching is incomplete; host privacy review required; no save or erasure'}
    if command == ('lesson', 'conflicts'):
        obj(e, ['records']); return conflicts(e['records'])
    if command == ('lesson', 'preview'):
        return preview(e)
    if command == ('lesson', 'retrieve-check'):
        return retrieve(load_state(e), e['payload'])
    if command == ('transfer', 'preview'):
        return transfer_preview(e)
    if command == ('audit', 'compare-cases'):
        return compare_cases(e)
    if command == ('audit', 'summary'):
        return audit_summary(e)
    raise Fault('unknown operation')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='family', required=True)
    operations = {'contract': ['validate', 'init', 'check-action'], 'step': ['reserve', 'record'], 'lesson': ['validate', 'identity', 'redact-preview', 'conflicts', 'preview', 'transition', 'retrieve-check'], 'audit': ['summary', 'compare-cases'], 'transfer': ['preview', 'apply']}
    for family, names in operations.items():
        children = sub.add_parser(family).add_subparsers(dest='operation', required=True)
        for name in names:
            children.add_parser(name).add_argument('--input', default='-', help='JSON file, or - for stdin')
    for name in ['verify', 'report']:
        sub.add_parser(name).add_argument('--input', default='-', help='JSON file, or - for stdin')
    args = parser.parse_args()
    try:
        if args.input == '-':
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        else:
            with open(args.input, 'rb') as f:
                raw = f.read(MAX_BYTES + 1)
        e = parse(raw)
        cmd = (args.family, args.operation) if hasattr(args, 'operation') else (args.family,)
        out = dispatch(cmd, e)
        sys.stdout.buffer.write(canon(out) + b'\n')
        return 0
    except Fault as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr); return 2
    except (OSError, ValueError, KeyError, TypeError, AttributeError, RecursionError):
        print(json.dumps({'error': 'invalid input or unavailable local capability; no sensitive details emitted'}), file=sys.stderr); return 2

if __name__ == '__main__':
    sys.exit(main())
