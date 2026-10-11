#!/usr/bin/env python3
"""Bounded advisor ledger. Records host observations; never executes their commands.

Files and hashes prove byte identity, not who wrote them or whether a reported
host event happened. The parent must obtain observations from actual host tools.
No secrets should be put in receipts. State and ownership files are local control
records, not an authorization source or protection against a malicious operator.
"""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile

VERSION = 1
OWNER = '.agent-ops-owner.json'
GUARD = '.agent-ops.lock'
HEX = re.compile(r'^[0-9a-f]{64}$')
CONTROLS = ('outcome', 'evidence', 'authority', 'stops', 'state', 'tool_contracts', 'recovery', 'cost', 'observability', 'verification')
PEER_TERMINAL = {'verified', 'verified-with-dissent', 'failed', 'unverifiable', 'stopped'}
IDENT = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$')


class Invalid(Exception):
    pass


class Refused(Exception):
    pass


def need(test, message, kind=Refused):
    if not test:
        raise kind(message)


def keys(obj, required):
    need(isinstance(obj, dict), 'expected an object', Invalid)
    need(set(obj) == set(required.split()), 'object fields must be: ' + required, Invalid)


def string(value, label):
    need(isinstance(value, str) and bool(value.strip()), label + ' must be a nonempty string', Invalid)
    return value


def identifier(value, label):
    need(isinstance(value, str) and bool(IDENT.fullmatch(value)), label + ' is invalid', Invalid)
    return value


def strings(value, label):
    need(isinstance(value, list), label + ' must be an array', Invalid)
    for item in value:
        string(item, label + ' entry')
    need(len(set(value)) == len(value), label + ' contains duplicates', Invalid)
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def reject_duplicate(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key, Invalid)
        result[key] = value
    return result


def read_json(path):
    try:
        return json.loads(Path(path).read_text(), object_pairs_hook=reject_duplicate,
                          parse_constant=lambda x: (_ for _ in ()).throw(Invalid('nonfinite JSON number')))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Invalid('cannot read JSON: ' + str(exc)) from exc


def relative(value):
    string(value, 'path')
    p = PurePosixPath(value)
    need(not p.is_absolute() and str(p) == value and '\\' not in value
         and all(part not in ('.', '..', '') for part in p.parts), 'unsafe relative path: ' + value, Invalid)
    return value


def overlap(a, b):
    return a == b or a.startswith(b + '/') or b.startswith(a + '/')


def safe(root, rel, must_exist=False):
    relative(rel)
    path = root / rel
    current = root
    for part in PurePosixPath(rel).parts:
        current = current / part
        need(not current.is_symlink(), 'symlink path refused: ' + rel)
    need(path.resolve().is_relative_to(root), 'path leaves workspace: ' + rel)
    if must_exist:
        need(path.is_file(), 'missing regular file: ' + rel)
        need(stat.S_ISREG(path.stat().st_mode), 'not a regular file: ' + rel)
    if path.exists() and path.is_file():
        need(path.stat().st_nlink == 1, 'hard-linked file refused: ' + rel)
    return path


def hash_file(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def file_ref(root, ref, evidence_dir=None):
    keys(ref, 'path sha256')
    relative(ref['path'])
    need(isinstance(ref['sha256'], str) and bool(HEX.fullmatch(ref['sha256'])), 'bad sha256', Invalid)
    if evidence_dir:
        need(ref['path'].startswith(evidence_dir + '/'), 'evidence must be inside evidence_dir')
    need(hash_file(safe(root, ref['path'], True)) == ref['sha256'], 'file hash drift: ' + ref['path'])
    return ref


def refs(root, value, evidence_dir=None):
    need(isinstance(value, list), 'file references must be an array', Invalid)
    for ref in value:
        file_ref(root, ref, evidence_dir)
    paths = [ref['path'] for ref in value]
    need(len(paths) == len(set(paths)), 'duplicate artifact path', Invalid)
    return paths


def workspace(value):
    string(value, 'workspace')
    root = Path(value)
    need(root.is_absolute() and root.is_dir() and root.resolve() == root, 'workspace must be an existing absolute real directory', Invalid)
    return root


def activation_gate(m):
    text = string(m['activation_request'], 'activation_request')
    need(type(m['peer_active']) is bool and type(m['gauntlet_requested']) is bool,
         'peer flags must be booleans', Invalid)
    need(not m['peer_active'] and not m['gauntlet_requested'], 'Gauntlet/controller exclusion')
    need(not re.search(r'\bgauntlet\b', text, re.I), 'Gauntlet and delegation named together')
    names = r'(?:bounded[ -]delegation|agent[ -]ops(?:[ -]bounded)?[ -]delegation|(?:fable|sol|astra)[ -]advisor)'
    # The opening clause must be an imperative, never a quotation or condition.
    match = re.match(r'^\s*(?:please\s+)?(?:use|run|start)\s+' + names + r'\b', text, re.I)
    alternate = re.match(r'^\s*run this as a multi-thread session\b', text, re.I)
    need(bool(match or alternate), 'no explicit delegation imperative')
    tail = text[(match or alternate).end():]
    first_clause = re.split(r'[;\n.]', tail, maxsplit=1)[0]
    need(not re.search(r'\b(?:if|unless|provided that|only when)\b', first_clause, re.I),
         'conditional activation refused')
    revoked = r"\b(?:cancel|revoke|stop|disable|(?:do not|don['’]t|never)\s+(?:use|run|start))\s+(?:(?:using|running)\s+)?(?:it\b|this(?:\s+run)?\b|the\s+(?:advisor|delegation|run)\b|" + names + r'\b)'
    need(not re.search(revoked, tail, re.I), 'same-request revoked activation refused')


def peer_gate(m):
    root = Path(m['workspace'])
    paths = list(strings(m['peer_state_paths'], 'peer_state_paths'))
    for rel in paths:
        peer = read_json(safe(root, rel, True))
        need(isinstance(peer, dict), 'invalid peer state', Invalid)
        need(peer.get('status') in PEER_TERMINAL, 'declared Gauntlet peer is active or unknown: ' + rel)


def validate_manifest(m, state_path, manifest_path=None):
    keys(m, 'version owner mode run_id workspace parent_id plan inputs evidence_dir integration_outputs integration_criteria integration_checks tasks budget peer_controllers activation_request peer_active gauntlet_requested peer_state_paths')
    need(type(m['version']) is int and m['version'] == VERSION, 'unsupported manifest version', Invalid)
    need(m['owner'] == 'agent-ops' and m['mode'] == 'advisor', 'unsupported owner or mode', Invalid)
    identifier(m['run_id'], 'run_id')
    string(m['parent_id'], 'parent_id')
    root = workspace(m['workspace'])
    activation_gate(m)
    peer_gate(m)
    expected_state = root / '.fable-advisor' / 'runs' / m['run_id'] / 'run-manifest.json'
    need(state_path == expected_state, 'state must use .fable-advisor/runs/<run_id>/run-manifest.json', Invalid)
    state_rel = state_path.relative_to(root).as_posix() if state_path.is_relative_to(root) else None
    need(state_rel is not None, 'state must be inside workspace', Invalid)
    safe(root, state_rel)
    file_ref(root, m['plan'])
    input_paths = refs(root, m['inputs'])
    need(m['plan']['path'] not in input_paths, 'plan duplicated as input', Invalid)
    relative(m['evidence_dir'])
    integrated = strings(m['integration_outputs'], 'integration_outputs')
    need(bool(integrated), 'integration_outputs must not be empty', Invalid)
    check_definitions(m['integration_criteria'], m['integration_checks'])
    keys(m['budget'], 'launches repairs concurrency')
    need(type(m['budget']['launches']) is int and m['budget']['launches'] > 0, 'launch budget must be positive', Invalid)
    need(type(m['budget']['concurrency']) is int and m['budget']['concurrency'] > 0, 'concurrency budget must be positive', Invalid)
    need(type(m['budget']['repairs']) is int and m['budget']['repairs'] >= 0, 'repair budget must be nonnegative', Invalid)
    need(m['peer_controllers'] == [], 'another controller is selected')
    need(isinstance(m['tasks'], list) and bool(m['tasks']), 'tasks must be a nonempty array', Invalid)
    tasks = {}
    for task in m['tasks']:
        keys(task, 'id depends_on reads outputs required criteria checks')
        identifier(task['id'], 'task id')
        need(task['id'] not in tasks, 'duplicate task id', Invalid)
        strings(task['depends_on'], 'depends_on')
        strings(task['reads'], 'reads')
        strings(task['outputs'], 'outputs')
        need(type(task['required']) is bool, 'required must be boolean', Invalid)
        need(bool(task['outputs']), 'worker tasks need at least one output', Invalid)
        check_definitions(task['criteria'], task['checks'])
        tasks[task['id']] = task
    need(any(t['required'] for t in tasks.values()), 'at least one task must be required', Invalid)
    for task in tasks.values():
        need(all(d in tasks and d != task['id'] for d in task['depends_on']), 'unknown/self dependency', Invalid)
    seen, visiting = set(), set()
    def visit(task_id):
        need(task_id not in visiting, 'task dependency cycle', Invalid)
        if task_id in seen:
            return
        visiting.add(task_id)
        for dep in tasks[task_id]['depends_on']:
            visit(dep)
        visiting.remove(task_id)
        seen.add(task_id)
    for task_id in tasks:
        visit(task_id)
    protected = [state_rel, state_rel + '.lock', str(PurePosixPath(state_rel).with_name('run-log.jsonl')), OWNER, GUARD, m['plan']['path']] + input_paths + m['peer_state_paths']
    if manifest_path and manifest_path.is_relative_to(root):
        protected.append(manifest_path.relative_to(root).as_posix())
    need(all(not overlap(m['evidence_dir'], p) for p in protected), 'evidence directory overlaps control/input files', Invalid)
    outputs = integrated + [p for task in tasks.values() for p in task['outputs']]
    for index, path in enumerate(outputs):
        safe(root, path)
        need(all(not overlap(path, p) for p in protected + [m['evidence_dir']]), 'output overlaps protected path: ' + path, Invalid)
        need(all(not overlap(path, p) for p in outputs[:index]), 'output scopes overlap: ' + path, Invalid)
    base_reads = set(input_paths + [m['plan']['path']])
    for task in tasks.values():
        allowed_reads = base_reads | {p for d in task['depends_on'] for p in tasks[d]['outputs']}
        need(all(relative(p) in allowed_reads for p in task['reads']), 'read scope is not an approved input/direct dependency', Invalid)
    return root


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(canonical(value) + b'\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextlib.contextmanager
def locked(path):
    need(not path.is_symlink(), 'lock symlink refused')
    flags = os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(path, flags, 0o600)
    try:
        need(os.fstat(fd).st_nlink == 1, 'hard-linked lock refused')
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def sync_log(path, s):
    log = path.with_name('run-log.jsonl')
    safe(Path(s['manifest']['workspace']), log.relative_to(Path(s['manifest']['workspace'])).as_posix())
    records = [{'event': 'initialized', 'run_id': s['manifest']['run_id'], 'contract_sha256': s['contract_sha256']}]
    if s['terminal'] and not s['terminal'].get('outstanding'):
        terminal_map = {'complete': 'accepted-and-synthesized', 'stopped': 'cancelled', 'revoked': 'cancelled',
                        'blocked': 'blocked', 'failed': 'failed', 'budget-exhausted': 'budget-exhausted'}
        records.append({'event': 'terminal', 'state': terminal_map[s['terminal']['status']]})
    wanted = b''.join(canonical(r) + b'\n' for r in records)
    if log.exists() and log.read_bytes() == wanted:
        return
    fd, temporary = tempfile.mkstemp(prefix='.run-log.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(wanted)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, log)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save(path, s):
    s['state_sha256'] = digest({k: v for k, v in s.items() if k != 'state_sha256'})
    atomic(path, s)
    sync_log(path, s)


def load(path, check_drift=True):
    need(not path.is_symlink(), 'state symlink refused')
    s = read_json(path)
    keys(s, 'version manifest manifest_path manifest_sha256 contract_sha256 activation launches reviews integration repair_cycles terminal state_sha256')
    need(s['version'] == VERSION, 'unsupported state version', Invalid)
    need(s['state_sha256'] == digest({k: v for k, v in s.items() if k != 'state_sha256'}), 'state integrity mismatch')
    need(s['contract_sha256'] == digest(s['manifest']), 'contract digest mismatch')
    root = workspace(s['manifest']['workspace'])
    safe(root, path.relative_to(root).as_posix(), True)
    need(all(isinstance(s[k], list) for k in ('launches', 'reviews', 'repair_cycles')), 'invalid state arrays', Invalid)
    if check_drift:
        validate_manifest(s['manifest'], path, Path(s['manifest_path']))
        manifest_path = Path(s['manifest_path'])
        need(manifest_path == manifest_path.resolve() and manifest_path.is_file(), 'manifest path changed or is a symlink')
        need(hash_file(manifest_path) == s['manifest_sha256'], 'manifest bytes changed')
        for launch in s['launches']:
            if launch['observation']:
                file_ref(root, launch['observation']['evidence'], s['manifest']['evidence_dir'])
                if 'continuation_evidence' in launch['observation']:
                    file_ref(root, launch['observation']['continuation_evidence'], s['manifest']['evidence_dir'])
            if launch['result']:
                verify_result_files(s, launch['result'], current_artifacts=(
                    launch['result'].get('status') == 'success' and launch['launch_id'] not in invalidated(s)))
        for cycle in s['repair_cycles']:
            file_ref(root, cycle['request']['evidence'], s['manifest']['evidence_dir'])
            verify_result_files(s, cycle['archived_integration'], current_artifacts=False)
        if s['activation']:
            file_ref(root, s['activation']['evidence'], s['manifest']['evidence_dir'])
        for review in s['reviews']:
            verify_result_files(s, review)
        if s['integration']:
            verify_result_files(s, s['integration'])
    return s


def commands(s, value, successful=True):
    need(isinstance(value, list), 'commands must be an array', Invalid)
    for command in value:
        keys(command, 'argv exit_code evidence')
        need(isinstance(command['argv'], list) and bool(command['argv']), 'argv must be nonempty array', Invalid)
        for arg in command['argv']:
            string(arg, 'argv entry')
        need(type(command['exit_code']) is int, 'exit_code must be integer', Invalid)
        need(not successful or command['exit_code'] == 0, 'successful receipt contains a failed command')
        file_ref(Path(s['manifest']['workspace']), command['evidence'], s['manifest']['evidence_dir'])


def verify_result_files(s, result, current_artifacts=True):
    root = Path(s['manifest']['workspace'])
    file_ref(root, result['evidence'], s['manifest']['evidence_dir'])
    successful_result = result.get('status', 'success') == 'success' and result.get('verdict') != 'rejected'
    commands(s, result.get('commands', []), successful_result)
    if 'criteria' in result:
        criteria(s, result['criteria'], successful_result)
    if current_artifacts and 'artifacts' in result:
        refs(root, result['artifacts'])
    if current_artifacts and 'integrated_artifacts' in result:
        refs(root, result['integrated_artifacts'])


def check_definitions(names, checks):
    strings(names, 'criteria')
    need(bool(names), 'approved criteria must not be empty', Invalid)
    need(isinstance(checks, list), 'checks must be an array', Invalid)
    for argv in checks:
        need(isinstance(argv, list) and bool(argv), 'check argv must be a nonempty array', Invalid)
        for arg in argv:
            string(arg, 'check argv entry')
    need(len({canonical(a) for a in checks}) == len(checks), 'duplicate approved check', Invalid)


def coverage(data, names, checks):
    need({c['name'] for c in data['criteria']} == set(names), 'return criteria do not match approved criteria')
    need(sorted(canonical(c['argv']) for c in data['commands']) == sorted(canonical(a) for a in checks),
         'return commands do not exactly cover approved checks')


def criteria(s, value, successful_status=True):
    need(isinstance(value, list) and bool(value), 'criteria must be a nonempty array', Invalid)
    names = []
    for criterion in value:
        keys(criterion, 'name status evidence')
        names.append(string(criterion['name'], 'criterion name'))
        need(criterion['status'] in ('pass', 'fail'), 'invalid criterion status', Invalid)
        need(not successful_status or criterion['status'] == 'pass', 'successful return contains a failed criterion')
        file_ref(Path(s['manifest']['workspace']), criterion['evidence'], s['manifest']['evidence_dir'])
    need(len(names) == len(set(names)), 'duplicate criterion', Invalid)


def task_map(s):
    return {t['id']: t for t in s['manifest']['tasks']}


def invalidated(s):
    return {launch_id for cycle in s['repair_cycles'] for launch_id in cycle['invalidated_launch_ids']}


def current_reviews(s):
    start = s['repair_cycles'][-1]['reviews_before'] if s['repair_cycles'] else 0
    return s['reviews'][start:]


def repairs_used(s):
    # One authorized repair cycle includes first replacement launches and its fresh critic.
    # Repeating a failed task or an unchanged critic outside that grant costs another unit.
    return len(s['repair_cycles']) + sum(l['repair'] for l in s['launches'])


def latest(s, task_id):
    stale = invalidated(s)
    return next((l for l in reversed(s['launches']) if l['task_id'] == task_id and l['launch_id'] not in stale), None)


def successful(launch):
    return bool(launch and launch['result'] and launch['result']['status'] == 'success')


def ready(s, task):
    return all(successful(latest(s, d)) for d in task['depends_on'])


def all_done(s):
    return all(not task['required'] or successful(latest(s, task['id'])) for task in s['manifest']['tasks'])


def subject(s):
    return digest({'workers': [{'launch_id': l['launch_id'], 'observation': l['observation'], 'result': l['result']}
                   for l in s['launches'] if l['role'] == 'worker' and successful(l) and l['launch_id'] not in invalidated(s)],
                   'integration': s['integration'], 'repair_cycle': len(s['repair_cycles'])})


def active(s):
    need(s['activation'] is not None, 'run is not explicitly activated')
    need(s['terminal'] is None, 'run is terminal: ' + str(s['terminal'] and s['terminal']['status']))


def bound(s, data):
    need(data['contract_sha256'] == s['contract_sha256'], 'receipt is bound to another contract')


def find_launch(s, launch_id):
    found = next((l for l in s['launches'] if l['launch_id'] == launch_id), None)
    need(found is not None, 'unknown launch_id')
    return found


def owner_value(s, path):
    return {'state': str(path), 'run_id': s['manifest']['run_id'], 'contract_sha256': s['contract_sha256']}


def check_owner(s, path):
    owner = safe(Path(s['manifest']['workspace']), OWNER)
    need(owner.is_file() and read_json(owner) == owner_value(s, path), 'workspace has no matching active owner')


def response(s):
    tasks = task_map(s)
    return {'run_id': s['manifest']['run_id'], 'contract_sha256': s['contract_sha256'],
            'active': s['activation'] is not None and s['terminal'] is None,
            'launches_used': len(s['launches']),
            'repairs_used': repairs_used(s), 'repair_cycles': s['repair_cycles'],
            'ready_tasks': [t['id'] for t in tasks.values() if ready(s, t) and latest(s, t['id']) is None],
            'subject_sha256': subject(s), 'review_sha256': digest(current_reviews(s)[-1]) if current_reviews(s) else None,
            'terminal': s['terminal'], 'launches': s['launches']}


def outstanding(s):
    return [{'launch_id': l['launch_id'],
             'worker_id': l['observation']['worker_id'] if l['observation'] else None,
             'status': 'host_completion_unconfirmed'} for l in s['launches'] if l['result'] is None]


def release_if_closed(s, path):
    if s['terminal'] and not s['terminal'].get('outstanding'):
        owner = safe(Path(s['manifest']['workspace']), OWNER)
        if owner.exists() and read_json(owner) == owner_value(s, path):
            owner.unlink()


def terminate(s, path, status, reason):
    s['terminal'] = {'status': status, 'reason': reason, 'outstanding': outstanding(s)}
    save(path, s)
    release_if_closed(s, path)
    raise Refused(reason + '; terminal=' + status)


def mutate(command, path, data, contract_sha=None):
    # One workspace writer also serializes different state files competing for ownership.
    initial = load(path, check_drift=False)
    root = Path(initial['manifest']['workspace'])
    safe(root, GUARD)
    with locked(root / GUARD):
        closing_observation = command == 'observe' and initial['terminal'] is not None
        s = load(path, check_drift=command not in ('stop', 'revoke', 'settle') and not closing_observation)
        if command in ('stop', 'revoke'):
            keys(data, 'reason')
            string(data['reason'], 'reason')
            if s['terminal'] is None:
                s['terminal'] = {'status': 'revoked' if command == 'revoke' else 'stopped', 'reason': data['reason'], 'outstanding': outstanding(s)}
                save(path, s)
            sync_log(path, s)
            release_if_closed(s, path)
            return response(s)
        if command == 'settle':
            keys(data, 'contract_sha256 launch_id worker_id status evidence')
            bound(s, data)
            need(s['terminal'] is not None and s['terminal']['status'] != 'complete', 'settle is only for stopped dispatch')
            launch = find_launch(s, data['launch_id'])
            file_ref(root, data['evidence'], s['manifest']['evidence_dir'])
            if launch['observation']:
                need(data['worker_id'] == launch['observation']['worker_id'], 'settlement child mismatch')
                need(data['status'] in ('cancelled', 'failed', 'completed'), 'invalid host terminal status', Invalid)
            else:
                need(data['worker_id'] is None and data['status'] == 'not_started', 'unobserved reservation needs not_started evidence')
            if launch['result'] is not None:
                need(launch['result'] == data, 'launch already has another terminal receipt')
                return response(s)
            launch['result'] = data
            s['terminal']['outstanding'] = outstanding(s)
            save(path, s)
            release_if_closed(s, path)
            return response(s)
        if command == 'approve':
            keys(data, 'contract_sha256 evidence')
            bound(s, data)
            need(contract_sha == s['contract_sha256'], 'approval digest does not match contract')
            need(s['terminal'] is None, 'terminal run cannot be activated')
            file_ref(root, data['evidence'], s['manifest']['evidence_dir'])
            owner = safe(root, OWNER)
            if owner.exists():
                need(read_json(owner) == owner_value(s, path), 'workspace already has another controller')
            else:
                atomic(owner, owner_value(s, path))
            if s['activation'] is None:
                s['activation'] = data
                save(path, s)
            else:
                need(s['activation'] == data, 'activation already recorded with different evidence')
            return response(s)
        recovering_observation = command == 'observe' and s['terminal'] is not None
        if recovering_observation:
            need(s['terminal']['status'] != 'complete' and bool(s['terminal'].get('outstanding')), 'closed run cannot receive a new observation')
            need(any(item['launch_id'] == data.get('launch_id') for item in s['terminal']['outstanding']), 'observation is not for an outstanding reservation')
        else:
            active(s)
        check_owner(s, path)
        if command == 'launch':
            keys(data, 'contract_sha256 launch_id role task_id read_only requested_identity runtime_available')
            bound(s, data)
            identifier(data['launch_id'], 'launch_id')
            keys(data['requested_identity'], 'model reasoning_effort')
            for v in data['requested_identity'].values():
                need(v is None or isinstance(v, str) and bool(v.strip()), 'requested identity must be text or null', Invalid)
            need(type(data['runtime_available']) is bool, 'runtime_available must be boolean', Invalid)
            if not data['runtime_available']:
                terminate(s, path, 'blocked', 'requested runtime, model, effort, or role tool is unavailable')
            need(data['role'] in ('worker', 'critic'), 'unsupported launch role', Invalid)
            need(type(data['read_only']) is bool, 'read_only must be boolean', Invalid)
            existing = next((l for l in s['launches'] if l['launch_id'] == data['launch_id']), None)
            if existing:
                need(all(existing[k] == data[k] for k in data if k != 'contract_sha256'), 'launch_id reused with different scope')
                return response(s)
            if len(s['launches']) >= s['manifest']['budget']['launches']:
                terminate(s, path, 'budget-exhausted', 'launch budget exhausted')
            if sum(l['result'] is None for l in s['launches']) >= s['manifest']['budget']['concurrency']:
                terminate(s, path, 'budget-exhausted', 'concurrency budget exhausted')
            repair = False
            if data['role'] == 'worker':
                need(data['task_id'] in task_map(s), 'unknown task_id', Invalid)
                need(data['read_only'] is False, 'worker launch must have its approved write scope')
                task = task_map(s)[data['task_id']]
                previous = latest(s, task['id'])
                need(previous is None or (previous['result'] and previous['result']['status'] == 'failed'), 'task already running or successful')
                need(ready(s, task), 'dependencies are not complete')
                repair = previous is not None
            else:
                need(data['task_id'] is None and data['read_only'] is True, 'critic must be read-only with null task_id')
                need(all_done(s) and s['integration'] is not None, 'critic requires successful returns and parent integration')
                need(all(l['result'] is not None for l in s['launches']), 'a launch is still outstanding')
                repair = bool(current_reviews(s))
            if repair and repairs_used(s) >= s['manifest']['budget']['repairs']:
                terminate(s, path, 'budget-exhausted', 'repair budget exhausted')
            s['launches'].append({k: data[k] for k in ('launch_id', 'role', 'task_id', 'read_only', 'requested_identity', 'runtime_available')} |
                                {'repair': repair, 'subject_sha256': subject(s) if data['role'] == 'critic' else None,
                                 'observation': None, 'result': None})
        elif command == 'observe':
            # continuation_evidence is optional: present only when a failed child is continued under its own ID.
            keys({k: v for k, v in data.items() if k != 'continuation_evidence'}, 'contract_sha256 launch_id worker_id host observed_identity evidence')
            bound(s, data)
            launch = find_launch(s, data['launch_id'])
            string(data['worker_id'], 'worker_id')
            need(data['host'] == 'native', 'only native host observations are supported', Invalid)
            keys(data['observed_identity'], 'model reasoning_effort')
            for field in data['observed_identity'].values():
                need(field is None or isinstance(field, str) and bool(field.strip()), 'identity must be observed text or null', Invalid)
            file_ref(root, data['evidence'], s['manifest']['evidence_dir'])
            if launch['observation']:
                need(launch['observation'] == data, 'launch observation already fixed')
                return response(s)
            need(launch['result'] is None, 'returned launch cannot be rebound')
            need(data['worker_id'] != s['manifest']['parent_id'], 'parent cannot act as a worker or critic')
            prior = [l for l in s['launches'] if l is not launch and l['observation'] and l['observation']['worker_id'] == data['worker_id']]
            if prior:
                # Only a worker continuing the same current task after its own terminal failed return may keep its ID,
                # and only with inspected native continuation evidence. Critics and every other reuse need a fresh child.
                stale = invalidated(s)
                need('continuation_evidence' in data and launch['role'] == 'worker' and all(
                    l['role'] == 'worker' and l['task_id'] == launch['task_id'] and l['launch_id'] not in stale
                    and l['result'] and l['result']['status'] == 'failed' for l in prior),
                    'child identity reused; a fresh child is required')
                file_ref(root, data['continuation_evidence'], s['manifest']['evidence_dir'])
            else:
                need('continuation_evidence' not in data, 'continuation evidence requires a failed same-task child', Invalid)
            for field, requested in launch['requested_identity'].items():
                observed = data['observed_identity'][field]
                if requested is not None and observed is not None and requested != observed:
                    launch['observation'] = data
                    if recovering_observation:
                        s['terminal']['outstanding'] = outstanding(s)
                        s['terminal'].setdefault('recovery_errors', []).append('observed ' + field + ' contradicts explicit request')
                        save(path, s)
                        raise Refused('recovered ' + field + ' contradicts explicit request; dispatch remains stopped')
                    terminate(s, path, 'blocked', 'observed ' + field + ' contradicts explicit request')
            launch['observation'] = data
            if recovering_observation:
                s['terminal']['outstanding'] = outstanding(s)
        elif command == 'complete':
            keys(data, 'contract_sha256 task_id launch_id worker_id status artifacts reported_writes criteria commands evidence')
            bound(s, data)
            launch = find_launch(s, data['launch_id'])
            need(launch['role'] == 'worker' and launch['task_id'] == data['task_id'], 'return task/launch mismatch')
            need(launch['observation'] and launch['observation']['worker_id'] == data['worker_id'], 'return does not match observed child')
            need(launch['result'] is None, 'duplicate return refused')
            need(data['status'] in ('success', 'failed'), 'unknown return status', Invalid)
            task = task_map(s)[data['task_id']]
            strings(data['reported_writes'], 'reported_writes')
            paths = refs(root, data['artifacts'])
            need(set(data['reported_writes']) <= set(task['outputs']), 'reported writes outside task scope')
            need(set(paths) <= set(task['outputs']), 'artifact outside task scope')
            if data['status'] == 'success':
                need(set(paths) == set(task['outputs']), 'successful return must bind every task output')
                need(set(data['reported_writes']) == set(task['outputs']), 'successful return must report exact task writes')
            verify_result_files(s, data)
            coverage(data, task['criteria'], task['checks'])
            launch['result'] = data
        elif command == 'repair':
            keys(data, 'contract_sha256 repair_id review_sha256 task_ids reason evidence')
            bound(s, data)
            identifier(data['repair_id'], 'repair_id')
            strings(data['task_ids'], 'task_ids')
            string(data['reason'], 'reason')
            file_ref(root, data['evidence'], s['manifest']['evidence_dir'])
            existing = next((c for c in s['repair_cycles'] if c['request']['repair_id'] == data['repair_id']), None)
            if existing:
                need(existing['request'] == data, 'repair_id reused with different scope')
                return response(s)
            need(all(l['result'] is not None for l in s['launches']), 'repair cannot start with outstanding children')
            reviews = current_reviews(s)
            need(bool(reviews) and reviews[-1]['verdict'] == 'rejected', 'repair requires the current fresh critic rejection')
            need(data['review_sha256'] == digest(reviews[-1]), 'repair references another review')
            need(s['integration'] is not None, 'repair requires the reviewed parent integration')
            affected = set(data['task_ids'])
            need(affected <= set(task_map(s)), 'repair names an unapproved task')
            need(all(successful(latest(s, task_id)) for task_id in affected), 'repair task has no accepted current result')
            if repairs_used(s) >= s['manifest']['budget']['repairs']:
                terminate(s, path, 'budget-exhausted', 'repair budget exhausted')
            # A changed dependency makes every descendant's prior acceptance stale.
            while True:
                expanded = affected | {t['id'] for t in s['manifest']['tasks'] if affected.intersection(t['depends_on'])}
                if expanded == affected:
                    break
                affected = expanded
            stale = [l['launch_id'] for l in s['launches'] if l['task_id'] in affected and l['launch_id'] not in invalidated(s)]
            s['repair_cycles'].append({'request': data, 'affected_task_ids': sorted(affected),
                                      'invalidated_launch_ids': stale, 'archived_integration': s['integration'],
                                      'reviews_before': len(s['reviews'])})
            s['integration'] = None
        elif command == 'integrate':
            keys(data, 'contract_sha256 parent_id integrated_artifacts reported_writes criteria commands evidence')
            bound(s, data)
            need(data['parent_id'] == s['manifest']['parent_id'], 'integration is not attributed to parent')
            need(all_done(s) and all(l['result'] is not None for l in s['launches']), 'integration dependencies are unfinished')
            need(not current_reviews(s), 'reviewed integration cannot be replaced before an authorized repair transition')
            paths = refs(root, data['integrated_artifacts'])
            strings(data['reported_writes'], 'reported_writes')
            need(set(paths) == set(data['reported_writes']) == set(s['manifest']['integration_outputs']), 'integration must bind exact approved parent output scope')
            criteria(s, data['criteria'])
            verify_result_files(s, data)
            coverage(data, s['manifest']['integration_criteria'], s['manifest']['integration_checks'])
            if s['integration'] is not None:
                need(s['integration'] == data, 'integration already recorded with different evidence')
                return response(s)
            s['integration'] = data
        elif command == 'review':
            keys(data, 'contract_sha256 launch_id worker_id subject_sha256 verdict read_only reported_writes findings commands evidence')
            bound(s, data)
            launch = find_launch(s, data['launch_id'])
            need(launch['role'] == 'critic' and launch['read_only'], 'review must use critic reservation')
            need(launch['observation'] and launch['observation']['worker_id'] == data['worker_id'], 'review child mismatch')
            need(launch['result'] is None, 'duplicate review refused')
            need(all_done(s), 'review cannot accept incomplete/failed work')
            need(data['subject_sha256'] == launch['subject_sha256'] == subject(s), 'stale review subject')
            need(data['read_only'] is True and data['reported_writes'] == [], 'critic must report read-only work')
            need(data['verdict'] in ('accepted', 'rejected'), 'unknown review verdict', Invalid)
            strings(data['findings'], 'findings')
            need(data['verdict'] != 'accepted' or data['findings'] == [], 'accepted review has unresolved findings')
            verify_result_files(s, data)
            if data['verdict'] == 'accepted':
                need(sorted(canonical(c['argv']) for c in data['commands']) == sorted(canonical(a) for a in s['manifest']['integration_checks']),
                     'accepted review must exactly cover approved integration checks')
            launch['result'] = {'status': 'success', 'verdict': data['verdict'], 'evidence': data['evidence'], 'commands': data['commands']}
            s['reviews'].append(data)
        elif command == 'finalize':
            keys(data, 'contract_sha256 parent_id subject_sha256 review_sha256')
            bound(s, data)
            need(data['parent_id'] == s['manifest']['parent_id'], 'integration is not attributed to parent')
            need(all_done(s) and all(l['result'] is not None for l in s['launches']), 'unfinished launch or required work')
            reviews = current_reviews(s)
            need(bool(reviews) and reviews[-1]['verdict'] == 'accepted', 'fresh accepted review required')
            review = reviews[-1]
            need(data['subject_sha256'] == review['subject_sha256'] == subject(s), 'stale integration/review subject')
            need(data['review_sha256'] == digest(review), 'integration references another review')
            need(s['integration'] is not None, 'parent integration missing')
            verify_result_files(s, s['integration'])
            s['terminal'] = {'status': 'complete', 'integration': s['integration']}
        else:
            raise Invalid('unknown command')
        save(path, s)
        release_if_closed(s, path)
        return response(s)


def check_audit(data, root):
    keys(data, 'controls')
    need(isinstance(data['controls'], list) and len(data['controls']) == len(CONTROLS), 'audit must cover all ten controls', Invalid)
    ids, findings = [], []
    for control in data['controls']:
        keys(control, 'id status evidence findings')
        need(control['id'] in CONTROLS, 'unknown audit control', Invalid)
        ids.append(control['id'])
        need(control['status'] in ('pass', 'fail', 'unknown'), 'invalid control status', Invalid)
        need(isinstance(control['evidence'], list) and bool(control['evidence']), 'each control needs inspectable evidence', Invalid)
        refs(root, control['evidence'])
        need(isinstance(control['findings'], list), 'findings must be an array', Invalid)
        need(control['status'] != 'fail' or bool(control['findings']), 'failed control needs a finding', Invalid)
        need(control['status'] != 'pass' or control['findings'] == [], 'passing control has findings', Invalid)
        for finding in control['findings']:
            keys(finding, 'severity detail')
            need(finding['severity'] in ('blocker', 'high', 'medium', 'low'), 'invalid severity', Invalid)
            string(finding['detail'], 'finding detail')
            findings.append({'control': control['id'], **finding})
    need(set(ids) == set(CONTROLS) and len(set(ids)) == len(ids), 'missing or duplicate control', Invalid)
    order = {'blocker': 0, 'high': 1, 'medium': 2, 'low': 3}
    return {'controls_checked': len(ids), 'findings': sorted(findings, key=lambda f: order[f['severity']]),
            'all_pass': all(c['status'] == 'pass' for c in data['controls'])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'approve', 'launch', 'observe', 'complete', 'repair', 'integrate', 'review', 'finalize', 'stop', 'revoke', 'settle', 'status', 'resume', 'validate'):
        p = subs.add_parser(name)
        p.add_argument('--state', required=True)
        if name == 'init':
            p.add_argument('--manifest', required=True)
        elif name not in ('status', 'resume', 'validate'):
            p.add_argument('--input', required=True)
        if name == 'approve':
            p.add_argument('--contract-sha', required=True)
    audit_parser = subs.add_parser('check-audit')
    audit_parser.add_argument('--input', required=True)
    audit_parser.add_argument('--workspace', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'check-audit':
            result = check_audit(read_json(args.input), workspace(args.workspace))
            print(json.dumps({'ok': True, **result}, sort_keys=True))
            return 0
        path = Path(args.state).absolute()
        need(path == path.resolve(), 'state path must not contain symlinks or traversal', Invalid)
        if args.command == 'init':
            manifest_path = Path(args.manifest).absolute()
            need(manifest_path == manifest_path.resolve() and manifest_path.is_file(), 'manifest must be a real file', Invalid)
            m = read_json(manifest_path)
            root = validate_manifest(m, path, manifest_path)
            need(manifest_path != path, 'state cannot overwrite manifest', Invalid)
            path.parent.mkdir(parents=True, exist_ok=True)
            with locked(root / GUARD):
                need(not path.exists(), 'state already exists; use status/resume')
                s = {'version': VERSION, 'manifest': m, 'manifest_path': str(manifest_path),
                     'manifest_sha256': hash_file(manifest_path), 'contract_sha256': digest(m),
                     'activation': None, 'launches': [], 'reviews': [], 'integration': None, 'repair_cycles': [], 'terminal': None}
                save(path, s)
                result = response(s)
        elif args.command in ('status', 'resume', 'validate'):
            s = load(path)
            if s['activation'] and not s['terminal']:
                check_owner(s, path)
            result = response(s)
        else:
            result = mutate(args.command, path, read_json(args.input), getattr(args, 'contract_sha', None))
        print(json.dumps({'ok': True, **result}, sort_keys=True))
        return 0
    except Invalid as exc:
        print(json.dumps({'ok': False, 'error': str(exc), 'kind': 'invalid_input'}))
        return 2
    except (TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc), 'kind': 'invalid_input'}))
        return 2
    except (Refused, OSError, ValueError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc), 'kind': 'refused'}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
