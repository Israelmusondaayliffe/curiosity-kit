"""Standalone Gauntlet ledger. Host tools execute calls; this module never does.

Approval and session receipts are coordinator attestations checked against the
actual host, not signatures or proof that a model was genuinely isolated.
"""
import contextlib
import datetime as dt
import hashlib
import html
import json
import math
import os
from pathlib import Path
import tempfile
import uuid


class StateError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise StateError(message)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def digest(value):
    return 'sha256:' + hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    return 'sha256:' + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_json(raw):
    def bad(value):
        raise StateError('Non-finite JSON: ' + value)
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, 'Duplicate JSON key: ' + key)
            out[key] = value
        return out
    return json.loads(raw, parse_constant=bad, object_pairs_hook=unique)


def read_json(path):
    return parse_json(Path(path).read_text(encoding='utf-8'))


def nonempty(value, name):
    require(isinstance(value, str) and bool(value.strip()), name + ' must be nonempty text')
    return value


def numeric(value, name, minimum=0, integer=False):
    require(type(value) in (int, float) and math.isfinite(value) and value >= minimum,
            name + ' must be finite and >= ' + str(minimum))
    require(not integer or type(value) is int, name + ' must be an integer')
    return value


def stamp(value):
    parsed = dt.datetime.fromisoformat(nonempty(value, 'timestamp').replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'Timestamp requires timezone')
    return parsed


def freeze(path):
    path = Path(path).resolve()
    require(path.is_file() and path.stat().st_size > 0, 'Missing or empty input: ' + str(path))
    return {'path': str(path), 'sha256': file_hash(path)}


def scope_path(path, roots):
    p = Path(path).resolve()
    require(any(p == Path(r) or Path(r) in p.parents for r in roots), 'Path outside approved scope: ' + str(p))
    return p


def approved_artifact(s, path, workstream_id=None):
    """Ownership comes from the frozen plan and writer records, never existence."""
    c = s['contract']
    resolved = scope_path(path, c['scope']['write_roots'])
    outputs = c['brief'].get('output_paths')
    require(isinstance(outputs, list) and outputs, 'Frozen declared output paths required')
    scope_path(resolved, [str(Path(p).resolve()) for p in outputs])
    if c['program']:
        tasks = c['program']['workstreams']
        if workstream_id is not None:
            tasks = [t for t in tasks if t['id'] == workstream_id]
            require(tasks, 'Unknown artifact workstream')
        targets = [str(Path(c['project_root']) / p) for t in tasks for p in t['write_targets']]
        scope_path(resolved, targets)
    if workstream_id is not None:
        writers = [e for e in s['launches'].values() if e['role'] in ('builder', 'smoother')
                   and e['workstream_id'] == workstream_id]
        if writers:
            require(all(e['status'] != 'reserved' for e in writers), 'Artifact writer is still pending')
            completed = [e for e in writers if e['status'] == 'completed']
            require(completed, 'No completed artifact writer establishes inspected scope')
            scope_path(resolved, [p for e in completed for p in e['write_paths']])
    return str(resolved)


def location(run_dir):
    path = Path(run_dir).resolve()
    installed = Path(__file__).resolve().parent.parent
    require(path != installed and installed not in path.parents, 'State must be outside installed skill')
    return path


@contextlib.contextmanager
def lock(run_dir):
    path = location(run_dir)
    path.mkdir(parents=True, exist_ok=True)
    require(not (path / '.lock').is_symlink(), 'Symlink lock refused')
    with open(path / '.lock', 'a+b') as handle:
        if os.name == 'nt':
            import msvcrt
            handle.write(b'0'); handle.flush(); handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield path
        finally:
            if os.name == 'nt':
                handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def atomic(path, value):
    require(not path.is_symlink(), 'Symlink output refused')
    fd, temporary = tempfile.mkstemp(prefix='.pending-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(canonical(value) + b'\n'); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path)
        if os.name != 'nt':
            fd = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


PEER_TERMINAL = {'accepted-and-synthesized', 'blocked', 'failed', 'cancelled', 'budget-exhausted'}


def peer_terminal_state(manifest):
    """Recorded terminal state of a Fable Advisor run, else None (active or unknown).
    The run manifest has no run-status field. The peer parent closes the run with a final record in the sibling
    run-log.jsonl; observed shapes are {event: run_closed, terminal_state} and {event: terminal, state}. Only the last
    record counts, so later activity reopens the run."""
    try:
        read_json(manifest)
        lines = [x for x in (Path(manifest).parent / 'run-log.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        last = json.loads(lines[-1]) if lines else None
    except (OSError, ValueError):
        return None
    if not isinstance(last, dict):
        return None
    value = {'run_closed': last.get('terminal_state'), 'terminal': last.get('state')}.get(last.get('event'))
    return value if isinstance(value, str) and value in PEER_TERMINAL else None


def precheck(data):
    """Optional caller-selected peer probe; never searches private sibling paths."""
    require(data.get('explicit_invocation') is True, 'Explicit Gauntlet invocation required')
    require(not data.get('fable_requested'), 'Gauntlet and Fable Advisor both named: choose one before state creation')
    require(data.get('peer_active', False) is False, 'Active Fable Advisor run: choose or end it first')
    probe = data.get('peer_probe')
    probes = [Path(probe)] if probe else []
    if data.get('project_root'):
        # Declared target-root compatibility probe, optional by absence, never a dependency.
        probes += list((Path(data['project_root']).resolve() / '.fable-advisor' / 'runs').glob('*/run-manifest.json'))
    for manifest in dict.fromkeys(probes):
        if not manifest.exists():
            continue
        require(peer_terminal_state(manifest) is not None,
                'Active or unknown Fable Advisor run at ' + str(manifest) + ': choose or end it first')
    caps = data.get('capabilities')
    require(isinstance(caps, dict) and caps, 'Provide observed host capabilities')
    for key in ('fresh_context', 'artifact_inspection'):
        require(caps.get(key) is True, 'Unsupported surface: missing ' + key)
    require(all(type(v) is bool for v in caps.values()), 'Capabilities must be boolean observations')
    missing = sorted(k for k, v in caps.items() if not v)
    return {'status': 'degraded' if missing else 'supported', 'missing': missing,
            'capabilities': caps, 'checked_at': now(), 'peer_probe': probe,
            'peer_absent': bool(probe and not Path(probe).exists())}


def budget_check(b):
    require(isinstance(b, dict), 'budget must be an object')
    for name in ('max_launches', 'max_iterations', 'max_concurrency', 'max_critic_rounds_per_workstream'):
        numeric(b.get(name), name, 1, True)
    numeric(b.get('max_seconds'), 'max_seconds', 1)
    numeric(b.get('max_cost'), 'max_cost')


def audit(s, action, data):
    s['revision'] += 1
    s['events'].append({'sequence': s['revision'], 'at': now(), 'action': action, 'data': data})


def validate(s, check_files=True):
    require(isinstance(s, dict) and s.get('schema_version') == 1, 'Unsupported state schema')
    require(s.get('status') in {'awaiting_approval', 'ready', 'running', 'paused', 'blocked', 'stopped',
                              'exhausted', 'verification', 'verified', 'verified-with-dissent', 'failed', 'unverifiable'}, 'Invalid status')
    c = s.get('contract')
    require(isinstance(c, dict) and digest(c) == s.get('contract_hash'), 'Frozen contract changed')
    require(digest(c['task']) == s.get('task_hash'), 'Task hash mismatch')
    budget_check(c['budget'])
    for name, kind in (('events', list), ('launches', dict), ('rounds', list), ('approvals', list), ('handoffs', list)):
        require(isinstance(s.get(name), kind), 'Invalid state ' + name)
    require(s['revision'] == len(s['events']), 'Audit revision mismatch')
    for i, e in enumerate(s['events'], 1):
        require(e.get('sequence') == i, 'Audit sequence mismatch')
    for key in ('launches', 'iterations', 'elapsed_seconds', 'cost', 'peak_concurrency'):
        numeric(s['usage'].get(key), 'usage.' + key)
    if check_files:
        for f in list(c['frozen'].values()) + c['sources'] + c.get('immutable_artifacts', []):
            require(file_hash(f['path']) == f['sha256'], 'Frozen input changed: ' + f['path'])
    return s


def _load(path, check_files=True):
    require(not (path / 'state.json').is_symlink(), 'Symlink state refused')
    return validate(read_json(path / 'state.json'), check_files)


def load_run(run_dir, check_files=True):
    with lock(run_dir) as path:
        return _load(path, check_files)


def mutate(run_dir, action, fn, check_files=True):
    with lock(run_dir) as path:
        s = _load(path, check_files)
        accrue_time(s, uncertain=action in ('recover', 'resume'))
        result, changed = fn(s)
        if changed:
            if s['status'] in ('paused', 'stopped', 'exhausted', 'verified', 'verified-with-dissent', 'failed', 'unverifiable'):
                s['session']['active_since'] = None
            audit(s, action, result)
            validate(s, check_files)
            atomic(path / 'state.json', s)
        return result


def init_run(run_dir, data):
    nonempty(data.get('project_root'), 'Declared project_root for scoped peer and ownership checks')
    surface = precheck(data)  # Must precede even creating a directory or lock.
    budget_check(data.get('budget'))
    import inspection
    brief = data.get('brief')
    require(isinstance(brief, dict), 'Decision-complete brief object required')
    brief = dict(brief, output_paths=[str(Path(p).resolve()) for p in brief.get('output_paths', [])])
    brief_check = inspection.validate_brief(brief)
    require(brief.get('budget') == data['budget'], 'Brief and runtime budgets must match exactly')
    nonempty(data.get('task'), 'task')
    mode = data.get('mode')
    require(mode in ('artifact', 'project', 'verification-only'), 'Invalid mode')
    frozen = data.get('frozen', {})
    require(set(frozen) == {'plan', 'bar', 'criteria', 'reader_questions'}, 'Four frozen document paths required')
    roots = data.get('scope', {}).get('write_roots')
    actions = data.get('scope', {}).get('allowed_actions')
    require(isinstance(roots, list) and roots and all(isinstance(x, str) and x for x in roots), 'Write roots required')
    require(isinstance(actions, list) and actions and all(isinstance(x, str) and x for x in actions), 'Allowed actions required')
    sources = data.get('source_paths')
    require(isinstance(sources, list) and sources, 'Inspectable source_paths required')
    immutable = data.get('artifact_paths', []) if mode == 'verification-only' else []
    require(mode != 'verification-only' or immutable, 'Verification-only requires frozen artifact_paths')
    contract = {'task': data['task'], 'brief': brief, 'brief_check': brief_check, 'mode': mode, 'budget': data['budget'],
                'scope': {'write_roots': [str(Path(x).resolve()) for x in roots], 'allowed_actions': actions},
                'frozen': {k: freeze(v) for k, v in frozen.items()}, 'sources': [freeze(x) for x in dict.fromkeys(sources + [r['path'] for r in brief_check['bar_files']])],
                'immutable_artifacts': [freeze(x) for x in immutable], 'capabilities': surface['capabilities'],
                'goal': data['task'], 'bar_description': data.get('bar_description', Path(frozen['bar']).read_text(encoding='utf-8')),
                'acceptance_criterion': data.get('acceptance_criterion', Path(frozen['criteria']).read_text(encoding='utf-8')),
                'completion_mode': data.get('completion_mode', 'blind-consecutive'),
                'review': data.get('review'), 'program': data.get('program'), 'project_root': str(Path(data.get('project_root', '.')).resolve())}
    for name in ('goal', 'bar_description', 'acceptance_criterion'):
        value = contract[name]
        require(isinstance(value, str) and len(' '.join(line for line in value.splitlines() if not line.lstrip().startswith('#')).strip()) >= 8,
                'Decision-complete ' + name + ' required; headings alone are insufficient')
    require(contract['completion_mode'] in ('blind-consecutive', 'measured-plus-independent'), 'Invalid frozen completion mode')
    require(contract['completion_mode'] != 'measured-plus-independent' or contract['program'], 'Measured completion requires a program and integration gate')
    require(isinstance(contract['review'], dict), 'Frozen review policy is required')
    if contract['review']:
        import review
        r = contract['review']
        require(not review.validate_policy(r.get('policy')), 'Invalid frozen review policy')
        require(review.string_list(r.get('criteria_ids'), 1), 'Frozen criteria IDs required')
        require(review.string_list(r.get('required_perspectives'), 3), 'Three frozen perspectives required')
        required = r.get('required_criteria_ids', r['criteria_ids'])
        require(review.string_list(required) and set(required) <= set(r['criteria_ids']), 'Invalid required criteria subset')
        if r.get('judging'):
            require(not review.validate_judging_policy(r['judging'], r['criteria_ids']), 'Invalid frozen judging policy')
    if contract['program']:
        import planning
        contract['program'] = planning.validate_program(contract['program'], contract['project_root'])
        b = contract['program']['budget']
        for key, other in (('max_launches', 'max_agent_launches'), ('max_concurrency', 'max_concurrency'),
                           ('max_critic_rounds_per_workstream', 'max_critic_rounds_per_workstream'), ('max_cost', 'max_cost')):
            require(contract['budget'][key] == b[other], 'Program/runtime budget mismatch: ' + key)
        require(contract['budget']['max_seconds'] == b['max_elapsed_minutes'] * 60, 'Program/runtime time budget mismatch')
    with lock(run_dir) as path:
        require(not (path / 'state.json').exists(), 'Run exists; resume it or choose a new directory')
        s = {'schema_version': 1, 'run_id': uuid.uuid4().hex, 'created_at': now(), 'status': 'awaiting_approval',
             'contract': contract, 'contract_hash': digest(contract), 'task_hash': digest(data['task']),
             'surface': surface, 'revision': 0, 'events': [], 'launches': {}, 'rounds': [], 'approvals': [],
             'handoffs': [], 'workstreams': {}, 'pieces': {}, 'integration': None, 'verification': None, 'stop_reason': None,
             'session': {'index': 0, 'active_since': None, 'elapsed_seconds': 0, 'uncertain_seconds': 0},
             'usage': {'launches': 0, 'iterations': 0, 'elapsed_seconds': 0, 'uncertain_seconds': 0, 'cost': 0, 'peak_concurrency': 0}}
        audit(s, 'init', {'contract_hash': s['contract_hash'], 'surface': surface})
        validate(s); atomic(path / 'state.json', s)
        return s


def approve(run_dir, data):
    def apply(s):
        require(s['status'] == 'awaiting_approval', 'Not awaiting approval')
        require(data.get('contract_hash') == s['contract_hash'], 'Approval contract mismatch')
        require(data.get('host_verified') is True, 'Coordinator must verify approval on actual host')
        for key in ('host', 'message_id', 'actor', 'verified_by'):
            nonempty(data.get(key), key)
        stamp(data.get('verified_at'))
        s['approvals'].append(dict(data, kind='host attestation, not cryptographic authority'))
        s['status'] = 'ready'
        s['session'] = {'index': 1, 'active_since': None, 'elapsed_seconds': 0, 'uncertain_seconds': 0}
        return {'status': 'ready'}, True
    return mutate(run_dir, 'approve', apply)


def limit(s):
    b, u = s['contract']['budget'], s['usage']
    elapsed = session_elapsed(s)
    for used, maximum, name in ((elapsed, b['max_seconds'], 'time'), (u['launches'], b['max_launches'], 'launch'),
                                (u['iterations'], b['max_iterations'], 'iteration')):
        if used >= maximum:
            return name + ' budget exhausted'
    if u['peak_concurrency'] > b['max_concurrency']:
        return 'observed concurrency exceeded budget'
    if u['cost'] > b['max_cost']:
        return 'cost budget exceeded'
    return None


def launch(run_dir, data):
    def apply(s):
        rid = nonempty(data.get('request_id'), 'request_id')
        for entry in s['launches'].values():
            if entry['request_id'] == rid:
                require(entry['request_hash'] == digest(data), 'Conflicting request replay')
                return {'may_launch': False, 'replayed': True, 'launch': entry}, False
        require(s['status'] in ('ready', 'running', 'verification'), 'Run not launchable: ' + s['status'])
        require(s['approvals'], 'Approval required')
        if data.get('capabilities') != s['contract']['capabilities']:
            s['status'], s['stop_reason'] = 'blocked', 'capability drift; re-plan before dispatch'
            return {'may_launch': False, 'reason': s['stop_reason']}, True
        require(not data.get('peer_active') and not data.get('fable_requested'), 'Peer conflict before dispatch')
        role = data.get('role')
        require(role in ('builder', 'smoother', 'critic', 'reader', 'quality', 'integrity'), 'Invalid helper role')
        require(not (s['contract']['mode'] == 'verification-only' and role in ('builder', 'smoother', 'critic')),
                'Verification-only forbids builders and build-loop critics')
        nonempty(data.get('actor'), 'actor')
        nonempty(data.get('workstream_id'), 'workstream_id')
        require(data.get('action') in s['contract']['scope']['allowed_actions'], 'Action outside scope')
        paths = data.get('write_paths')
        require(isinstance(paths, list), 'write_paths required')
        frozen_paths = [Path(f['path']) for f in list(s['contract']['frozen'].values()) + s['contract']['sources'] + s['contract']['immutable_artifacts']]
        for p in paths:
            resolved = scope_path(p, s['contract']['scope']['write_roots'])
            runtime = location(run_dir)
            require(resolved != runtime and runtime not in resolved.parents and resolved not in runtime.parents, 'Writer target overlaps canonical run state')
            require(not any(resolved == f or resolved in f.parents for f in frozen_paths), 'Write target includes frozen input')
        if role in ('critic', 'quality', 'integrity'):
            require(isinstance(data.get('evidence_paths'), dict) and data['evidence_paths'], 'Observed evidence_paths required before dispatch')
            for evidence_path in data['evidence_paths'].values():
                freeze(evidence_path)
        if role == 'critic' and s['contract']['review'].get('judging', {}).get('mode', 'blind') != 'rubric':
            for key in ('packet_hash', 'sealed_map_hash'):
                require(isinstance(data.get(key), str) and data[key].startswith('sha256:') and len(data[key]) == 71, 'Pre-dispatch ' + key + ' required')
        require(data.get('fresh_context') is True, 'Fresh context required')
        require(role in ('builder', 'smoother') or paths == [], 'Reviewers and reader proxy must be read-only')
        estimated = numeric(data.get('estimated_cost'), 'estimated_cost')
        pending = [x for x in s['launches'].values() if x['status'] == 'reserved']
        require(len(pending) < s['contract']['budget']['max_concurrency'], 'Concurrency cap reached')
        if role in ('critic', 'builder'):
            # Every critic reservation counts, including interrupted ones whose outcome is uncertain.
            count = sum(x['role'] == 'critic' and x['workstream_id'] == data['workstream_id'] for x in s['launches'].values())
            cap = s['contract']['budget']['max_critic_rounds_per_workstream']
            if s['contract']['program']:
                task = next((t for t in s['contract']['program']['workstreams'] if t['id'] == data['workstream_id']), None)
                require(task is not None, 'Unknown workstream')
                cap = min(cap, task['max_critic_rounds'])
            if role == 'critic':
                require(count < cap, 'Workstream critic cap reached')
            else:
                # New builder bytes restart the win streak, so they need the full independent review count to be accepted.
                needed = 1 if s['contract']['completion_mode'] == 'measured-plus-independent' else s['contract']['review']['policy'].get('consecutive_wins', 2)
                require(cap - count >= needed, 'Builder refused: workstream ' + data['workstream_id'] + ' has ' + str(max(0, cap - count))
                        + ' critic review(s) left but accepting new bytes needs ' + str(needed)
                        + '; pause and use an approved successor contract')
        for existing in pending:
            for a in paths:
                for b in existing['write_paths']:
                    pa, pb = Path(a).resolve(), Path(b).resolve()
                    require(pa != pb and pa not in pb.parents and pb not in pa.parents, 'Parallel write overlap')
        reason = limit(s)
        if s['usage']['cost'] + sum(x['estimated_cost'] for x in pending) + estimated > s['contract']['budget']['max_cost']:
            reason = 'cost reservation exceeds budget'
        if reason:
            s['status'], s['stop_reason'] = 'exhausted', reason
            return {'may_launch': False, 'reason': reason}, True
        if s['contract']['program'] and role == 'builder':
            import planning
            ready = planning.ready_workstreams(s['contract']['program'], s['workstreams'], s['contract']['project_root'])
            require(data['workstream_id'] in ready, 'Workstream dependencies are not accepted')
            task = next(t for t in s['contract']['program']['workstreams'] if t['id'] == data['workstream_id'])
            allowed = [str(Path(s['contract']['project_root']) / p) for p in task['write_targets']]
            for target in paths:
                scope_path(target, allowed)
        if role == 'smoother':
            if s['contract']['program']:
                import planning
                program, root = s['contract']['program'], s['contract']['project_root']
                require(planning.integration_readiness(program, s['workstreams'], root)['ready'], 'Smoothing waits for accepted workstreams')
                task = next((t for t in program['workstreams'] if t['id'] == data['workstream_id']), None)
                require(task is not None, 'Unknown smoother workstream')
                for target in paths:
                    scope_path(target, [str(Path(root) / p) for p in task['write_targets']])
                s['workstreams'] = planning.invalidate_dependents(program, s['workstreams'], [data['workstream_id']], root)
                affected = [key for key, record in s['workstreams'].items() if record.get('status') == 'invalidated']
            else:
                piece = s['pieces'].get(data['workstream_id'])
                require(piece and piece['status'] == 'converged', 'Smoothing requires a converged piece')
                for target in paths:
                    scope_path(target, [piece['artifact_path']])
                affected = [data['workstream_id']]
            for identifier in affected:
                if identifier in s['pieces']:
                    s['pieces'][identifier].update(status='looping', consecutive_wins=0)
            s['integration'] = None
        if not s['session']['active_since']:
            s['session']['active_since'] = now()
        lid = uuid.uuid4().hex
        entry = dict(data, id=lid, request_hash=digest(data), status='reserved', reserved_at=now(),
                     write_paths=[str(Path(p).resolve()) for p in paths])
        if role in ('builder', 'smoother'):
            entry['watch_roots'] = s['contract']['brief']['output_paths']
            entry['snapshot_exclusions'] = [str(location(run_dir))]
            entry['before_files'] = write_snapshot(entry['watch_roots'], entry['snapshot_exclusions'])
        if role in ('critic', 'quality', 'integrity'):
            entry['evidence_manifest'] = {key: file_hash(path) for key, path in data['evidence_paths'].items()}
        reason = limit(s)
        if reason:
            s['status'], s['stop_reason'] = 'exhausted', reason
            return {'may_launch': False, 'reason': reason}, True
        s['launches'][lid] = entry
        s['usage']['launches'] += 1
        s['usage']['peak_concurrency'] = max(s['usage']['peak_concurrency'], len(pending) + 1)
        s['status'] = 'verification' if role in ('reader', 'quality', 'integrity') else 'running'
        return {'may_launch': True, 'replayed': False, 'launch': entry}, True
    return mutate(run_dir, 'launch-reservation', apply)


def complete(run_dir, data):
    def apply(s):
        e = s['launches'].get(data.get('launch_id'))
        require(e is not None, 'Unknown launch')
        if e.get('completion_hash'):
            require(e['completion_hash'] == digest(data), 'Conflicting completion replay')
            return e, False
        require(e['status'] == 'reserved', 'Launch not reserved')
        cost = numeric(data.get('actual_cost'), 'actual_cost')
        receipt = data.get('host_receipt')
        require(isinstance(receipt, dict) and receipt.get('author_id') == e['actor'], 'Host receipt identity mismatch')
        require(receipt.get('role') == e['role'], 'Receipt role differs from assigned role')
        nonempty(receipt.get('session_id'), 'session_id')
        nonempty(receipt.get('host_record'), 'host_record')
        require(not any(x.get('host_receipt', {}).get('session_id') == receipt['session_id'] for x in s['launches'].values()), 'Host session replay')
        if e['role'] != 'builder':
            require(receipt.get('fresh_context') is True and receipt.get('inherited_turns') == 0
                    and receipt.get('forbidden_context_seen') is False, 'Host did not establish fresh context')
        if e['role'] in ('builder', 'smoother'):
            e['observed_writes'] = validate_writes(e, receipt, data.get('changed_outputs', False), list(s['launches'].values()))
        e.update(status='completed', actual_cost=cost, completed_at=now(), host_receipt=receipt, completion_hash=digest(data))
        s['usage']['cost'] += cost
        if s['usage']['cost'] > s['contract']['budget']['max_cost']:
            s['status'], s['stop_reason'] = 'exhausted', 'actual cost exceeded budget'
        return e, True
    return mutate(run_dir, 'complete-launch', apply)


def record_round(run_dir, data):
    def apply(s):
        eid = nonempty(data.get('evidence_id'), 'evidence_id')
        for prior in s['rounds']:
            if prior['evidence_id'] == eid:
                require(prior['input_hash'] == digest(data), 'Conflicting evidence replay')
                return dict(prior, replayed=True), False
        require(s['status'] in ('running', 'ready'), 'Run cannot record round: ' + s['status'])
        e = s['launches'].get(data.get('launch_id'))
        require(e and e['role'] == 'critic' and e['status'] == 'completed', 'Completed fresh critic launch required')
        require(not any(x['launch_id'] == e['id'] for x in s['rounds']), 'Critic launch already consumed')
        require(data.get('contract_hash') == s['contract_hash'], 'Round contract mismatch')
        artifact = freeze(approved_artifact(s, data['artifact_path'], e['workstream_id']))
        require(artifact['sha256'] == data.get('artifact_hash'), 'Artifact bytes changed')
        report = freeze(data['report_path'])
        require(not any(x['report']['sha256'] == report['sha256'] for x in s['rounds']), 'Report replay')
        import review
        raw = data.get('review')
        require(isinstance(raw, dict), 'Critic review packet required')
        require(read_json(report['path']) == raw.get('verdict'), 'Persisted critic report differs from submitted verdict')
        context = raw.get('context', {})
        require(context.get('piece_id') == e['workstream_id'], 'Critic workstream differs from dispatch')
        require(context.get('contract_hash') == s['contract_hash'] and context.get('artifact_hash') == artifact['sha256'], 'Critic binding mismatch')
        require(context.get('criteria_ids') == s['contract']['review']['criteria_ids'], 'Frozen critic criteria mismatch')
        receipt = e['host_receipt']
        require(context.get('expected_sessions') == {receipt['session_id']: receipt}, 'Critic receipt differs from host ledger')
        judging = s['contract']['review'].get('judging', {})
        if judging.get('mode') == 'rubric':
            require(context.get('judging_policy') == judging, 'Frozen judging policy mismatch')
        else:
            for key in ('packet_hash', 'sealed_map_hash'):
                require(context.get(key) == e.get(key), 'Blind anchor differs from pre-dispatch record')
        manifest = {key: file_hash(path) for key, path in e['evidence_paths'].items()}
        require(context.get('evidence_manifest') == manifest == e['evidence_manifest'], 'Critic evidence bytes mismatch')
        builders = {x['actor'] for x in s['launches'].values() if x['role'] in ('builder', 'smoother')}
        require(builders.issubset(set(context.get('excluded_authors', []))), 'Builder must be excluded from critic')
        unsealed = (review.evaluate_rubric_critic(raw.get('verdict'), context) if judging.get('mode') == 'rubric'
                    else review.unseal_critic(raw.get('verdict'), context, raw.get('packet'), raw.get('sealed_map')))
        verdict = 'win' if unsealed['winner_is_ours'] else 'revise'
        if unsealed['winner'] == 'unable_to_evaluate':
            verdict = 'blocked'
        require(data.get('verdict') == verdict, 'Claimed verdict differs from blind critic')
        require(data.get('gap') == unsealed.get('largest_gap'), 'Gap differs from blind critic')
        if verdict != 'win':
            nonempty(data.get('gap'), 'gap')  # revise and blocked rounds always carry the concrete gap or blocker
        require(s['usage']['iterations'] < s['contract']['budget']['max_iterations'], 'Iteration cap reached')
        row = dict(data, input_hash=digest(data), artifact=artifact, report=report, iteration=len(s['rounds']) + 1)
        s['rounds'].append(row); s['usage']['iterations'] += 1
        piece = s['pieces'].get(e['workstream_id'], {})
        wins = piece.get('consecutive_wins', 0) if piece.get('artifact_hash') == artifact['sha256'] else 0
        wins = wins + 1 if verdict == 'win' else 0
        required_wins = 1 if s['contract']['completion_mode'] == 'measured-plus-independent' else s['contract']['review']['policy'].get('consecutive_wins', 2)
        s['pieces'][e['workstream_id']] = {'artifact_hash': artifact['sha256'], 'artifact_path': artifact['path'],
            'consecutive_wins': wins, 'required_wins': required_wins, 'status': 'converged' if wins >= required_wins else 'looping',
            'last_verdict': verdict, 'largest_gap': data.get('gap')}
        if wins >= required_wins and s['contract']['program']:
            import planning
            accepted_evidence = data.get('acceptance_evidence')
            require(isinstance(accepted_evidence, list) and accepted_evidence, 'Acceptance evidence required')
            bound_files = {str(Path(path).resolve()): e['evidence_manifest'][key] for key, path in e['evidence_paths'].items()}
            bound_files[artifact['path']] = artifact['sha256']
            for ref in accepted_evidence:
                path = str((Path(s['contract']['project_root']) / ref['path']).resolve())
                require(bound_files.get(path) == 'sha256:' + ref['sha256'], 'Acceptance evidence was not inspected in this round')
            s['workstreams'][e['workstream_id']] = planning.acceptance_record(
                s['contract']['program'], s['workstreams'], e['workstream_id'], accepted_evidence, s['contract']['project_root'])
        if verdict in ('failed', 'blocked'):
            s['status'], s['stop_reason'] = verdict, data['gap']
        previous = [x for x in s['rounds'][:-1] if x['artifact']['path'] == artifact['path']]
        if previous and verdict == previous[-1]['verdict'] == 'revise' and data['gap'] == previous[-1]['gap']:
            s['status'], s['stop_reason'] = 'blocked', 'Repeated gap: no gain; re-plan required'
        return dict(row, status=s['status']), True
    return mutate(run_dir, 'round', apply)


def usage(run_dir, data):
    def apply(s):
        for key, value in data.items():
            require(key in s['usage'], 'Unknown usage counter')
            numeric(value, key, integer=key in ('launches', 'iterations', 'peak_concurrency'))
            require(value >= s['usage'][key], 'Usage counters cannot decrease')
        for key in ('elapsed_seconds', 'uncertain_seconds'):
            if key in data:
                delta = data[key] - s['usage'][key]
                s['session']['elapsed_seconds'] += delta
                if key == 'uncertain_seconds':
                    s['session']['uncertain_seconds'] += delta
        s['usage'].update(data)
        reason = limit(s)
        if reason:
            s['status'], s['stop_reason'] = 'exhausted', reason
        return {'usage': s['usage'], 'status': s['status']}, True
    return mutate(run_dir, 'usage', apply)


def recover(run_dir, data):
    def apply(s):
        require(s['status'] in ('ready', 'running', 'verification', 'paused'), 'Terminal run cannot recover into an active phase')
        e = s['launches'].get(data.get('launch_id'))
        require(e is not None, 'Unknown launch')
        nonempty(data.get('reason'), 'reason')
        if e['status'] == 'interrupted':
            return e, False
        require(e['status'] == 'reserved', 'Only uncertain reservations need recovery')
        e['status'] = 'interrupted'; e['recovery_reason'] = data['reason']
        s['usage']['cost'] += e['estimated_cost']
        s['status'], s['stop_reason'] = 'paused', data['reason']
        return e, True
    return mutate(run_dir, 'recover', apply)


def resume(run_dir, data):
    def apply(s):
        require(s['status'] in ('paused', 'running', 'verification', 'ready'), 'Run cannot resume in current status')
        require(not any(e['status'] == 'reserved' for e in s['launches'].values()), 'Reconcile pending launches first')
        require(data.get('capabilities') == s['contract']['capabilities'], 'Capability drift')
        require(not data.get('peer_active'), 'Active peer conflict')
        s['session'] = {'index': s['session']['index'] + 1, 'active_since': now(), 'elapsed_seconds': 0, 'uncertain_seconds': 0}
        require(limit(s) is None, limit(s) or '')
        s['status'], s['stop_reason'] = 'ready', None
        return {'status': 'ready', 'run_id': s['run_id']}, True
    return mutate(run_dir, 'resume', apply)


def stop(run_dir, data):
    def apply(s):
        nonempty(data.get('reason'), 'reason')
        if s['status'] == 'stopped':
            return {'status': 'stopped', 'reason': s['stop_reason']}, False
        require(s['status'] not in ('verified', 'verified-with-dissent', 'failed', 'unverifiable', 'exhausted'), 'Terminal verdict is immutable; stop cannot relabel it')
        s['status'], s['stop_reason'] = 'stopped', data['reason']
        return {'status': 'stopped', 'reason': data['reason']}, True
    return mutate(run_dir, 'stop', apply, check_files=False)


def verify(run_dir):
    s = load_run(run_dir)
    return {'ok': True, 'status': s['status'], 'contract_hash': s['contract_hash'], 'usage': s['usage'],
            'pending': [k for k, e in s['launches'].items() if e['status'] == 'reserved'], 'limit_reason': limit(s)}


def handoff(run_dir):
    def apply(s):
        if s['status'] in ('ready', 'running', 'verification'):
            s['status'] = 'paused'
            if any(e['status'] == 'reserved' for e in s['launches'].values()):
                s['session']['pending_since'] = now()
            s['session']['active_since'] = None
        h = {'sequence': len(s['handoffs']) + 1, 'at': now(), 'run_id': s['run_id'], 'status': s['status'],
             'state_path': str(location(run_dir) / 'state.json'), 'task': s['contract']['task'],
             'scope': s['contract']['scope'], 'frozen': s['contract']['frozen'],
             'sources': s['contract']['sources'], 'budget': s['contract']['budget'],
             'workstreams': s['workstreams'], 'pieces': s['pieces'], 'integration': s['integration'],
             'contract_hash': s['contract_hash'], 'usage': dict(s['usage']), 'session': dict(s['session']), 'stop_reason': s['stop_reason'],
             'pending_launches': [k for k, e in s['launches'].items() if e['status'] == 'reserved'],
             'last_round': s['rounds'][-1] if s['rounds'] else None,
             'next_action': 'Verify host receipts; reconcile interrupted calls; use remaining approved budget.'}
        s['handoffs'].append(h)
        return h, True
    result = mutate(run_dir, 'handoff', apply, check_files=False)
    with lock(run_dir) as path:
        # Numbered snapshots never overwrite older handoffs; latest is a view.
        body = '# Gauntlet handoff ' + str(result['sequence']) + '\n\n' + json.dumps(result, indent=2) + '\n'
        export_text(path / ('handoff-%04d.md' % result['sequence']), body)
        latest = _load(path, check_files=False)['handoffs'][-1]
        export_text(path / 'HANDOFF.md', '# Gauntlet handoff ' + str(latest['sequence']) + '\n\n' + json.dumps(latest, indent=2) + '\n')
    return result


def report(run_dir):
    """Export recoverable views from canonical state, including failure states."""
    with lock(run_dir) as path:
        s = _load(path, check_files=False)
        stale = []
        try:
            validate(s)
            latest = {}
            for row in s['rounds']:
                latest[row['artifact']['path']] = row['artifact']
                require(file_hash(row['report']['path']) == row['report']['sha256'], 'Round report changed: ' + row['report']['path'])
            for artifact in latest.values():
                require(file_hash(artifact['path']) == artifact['sha256'], 'Latest round artifact changed: ' + artifact['path'])
            if s['verification']:
                for inspected in s['verification'].get('inspections', {}).values():
                    f = inspected['file']
                    require(file_hash(f['path']) == f['sha256'], 'Inspection report changed')
                artifact = s['verification'].get('artifact')
                if artifact:
                    require(file_hash(artifact['path']) == artifact['sha256'], 'Final artifact changed')
                for e in s['launches'].values():
                    if e['role'] in ('quality', 'integrity'):
                        for key, source in e.get('evidence_paths', {}).items():
                            require(file_hash(source) == s['verification']['context']['evidence_manifest'].get(key), 'Verification evidence changed: ' + source)
        except (ValueError, OSError, KeyError) as exc:
            stale.append(str(exc))
        if stale and s['status'] in ('verified', 'verified-with-dissent'):
            s['status'], s['stop_reason'] = 'unverifiable', '; '.join(stale)
            if s['verification']:
                s['verification']['prior_consensus'] = s['verification']['consensus']
                s['verification']['consensus'] = 'unverifiable'
                s['verification']['validation_errors'].extend(stale)
            audit(s, 'stale-evidence', {'errors': stale})
            atomic(path / 'state.json', s)
        content = {'run_id': s['run_id'], 'status': s['status'], 'task': s['contract']['task'],
                   'contract_hash': s['contract_hash'], 'surface': s['surface'], 'usage': s['usage'],
                   'stop_reason': s['stop_reason'], 'verification': s['verification'],
                   'rounds': s['rounds'], 'launches': s['launches'], 'frozen': s['contract']['frozen'],
                   'sources': s['contract']['sources'], 'events': s['events']}
        content['current_integrity_errors'] = stale
        atomic(path / 'evidence-report.json', content)
        export_text(path / 'evidence-report.md', '# Gauntlet evidence report\n\nStatus: ' + s['status'] + '\n\n' + json.dumps(content, indent=2) + '\n')
        body = '<!doctype html><meta charset="utf-8"><title>Gauntlet workbench</title><h1>Gauntlet: ' + html.escape(s['status']) + '</h1><pre>' + html.escape(json.dumps(content, indent=2)) + '</pre>'
        out = path / 'workbench.html'
        require(not out.is_symlink(), 'Symlink workbench refused')
        fd, temp = tempfile.mkstemp(prefix='.workbench-', dir=str(path))
        with os.fdopen(fd, 'w', encoding='utf-8') as h:
            h.write(body); h.flush(); os.fsync(h.fileno())
        os.replace(temp, out)
        return {'status': s['status'], 'evidence_report': str(path / 'evidence-report.json'), 'workbench': str(out), 'markdown_report': str(path / 'evidence-report.md')}


def integrate(run_dir, data):
    def apply(s):
        import planning
        require(s['status'] in ('ready', 'running', 'verification'), 'Terminal/paused run cannot integrate')
        require(s['contract']['program'], 'Project program required')
        gate = planning.integration_readiness(s['contract']['program'], s['workstreams'], s['contract']['project_root'])
        require(gate['ready'], 'Workstreams missing/stale: ' + str(gate['missing_or_stale']))
        evidence = freeze(data['evidence_path'])
        observed = read_json(evidence['path'])
        require(type(data.get('exit_code')) is int and data['exit_code'] == 0, 'Integration check did not pass')
        require(observed.get('exit_code') == 0 and observed.get('timed_out') is False
                and isinstance(observed.get('argv'), list) and observed['argv']
                and observed.get('started_at'), 'Integration evidence needs captured inspection check result')
        require(data.get('contradictions') == [], 'Resolve integration contradictions first')
        nonempty(data.get('command'), 'integration command')
        s['integration'] = dict(data, evidence=evidence, workstreams_hash=digest(s['workstreams']))
        s['status'] = 'verification'
        return s['integration'], True
    return mutate(run_dir, 'integrate', apply)


def finalize(run_dir, data):
    """Compute terminal verdict; invalid or unavailable evidence stays exportable."""
    def apply(s):
        if s['verification']:
            require(s['verification']['request_hash'] == digest(data), 'Final verdict immutable; start a new run for changed evidence')
            return s['verification'], False
        import review
        errors = []
        try:
            validate(s)
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
        policy = s['contract'].get('review')
        if not policy:
            errors.append('Frozen review policy/criteria/perspectives missing')
            policy = {}
        context = dict(data.get('context') or {})
        try:
            actual = freeze(data['artifact_path'])
            if s['contract']['mode'] == 'verification-only':
                approved = s['contract']['immutable_artifacts']
                require(len(approved) == 1, 'Single-artifact finalization cannot cover multiple approved artifacts; use a separate run per target')
                require(actual == approved[0] and str(Path(data['artifact_path']).resolve()) == approved[0]['path'],
                        'Final artifact path and bytes must match the exact approved immutable target')
            else:
                approved_artifact(s, actual['path'])
                matching = [p for p in s['pieces'].values() if p['artifact_path'] == actual['path']
                            and p['artifact_hash'] == actual['sha256'] and p['status'] == 'converged']
                require(matching, 'Final artifact is not an accepted current output')
            require(context.get('artifact_hash') == actual['sha256'], 'Artifact hash mismatch')
        except (KeyError, ValueError, OSError) as exc:
            errors.append(str(exc))
        if context.get('contract_hash') != s['contract_hash']:
            errors.append('Contract hash mismatch')
        for key in ('criteria_ids', 'required_perspectives'):
            if context.get(key) != policy.get(key):
                errors.append('Frozen ' + key + ' mismatch')
        if context.get('required_criteria_ids', context.get('criteria_ids')) != policy.get('required_criteria_ids', policy.get('criteria_ids')):
            errors.append('Frozen required-criterion classification mismatch')
        receipts = {e['host_receipt']['session_id']: e['host_receipt'] for e in s['launches'].values()
                    if e['status'] == 'completed' and e['role'] in ('quality', 'integrity')}
        if context.get('expected_sessions') != receipts:
            errors.append('Verification receipts differ from recorded host launches')
        manifest = {}
        for e in s['launches'].values():
            if e['status'] == 'completed' and e['role'] in ('quality', 'integrity'):
                for key, path in e['evidence_paths'].items():
                    try:
                        value = file_hash(path)
                        if value != e['evidence_manifest'].get(key):
                            errors.append('Evidence changed since dispatch: ' + key)
                        if key in manifest and manifest[key] != value:
                            errors.append('Conflicting evidence ID: ' + key)
                        manifest[key] = value
                    except OSError as exc:
                        errors.append(str(exc))
        if context.get('evidence_manifest') != manifest:
            errors.append('Verification evidence differs from actual bytes')
        builders = {e['actor'] for e in s['launches'].values() if e['role'] in ('builder', 'smoother')}
        if not builders.issubset(set(context.get('excluded_authors', []))):
            errors.append('Builder exclusion missing')
        if any(e['status'] == 'reserved' for e in s['launches'].values()):
            errors.append('Unreconciled launches remain')
        if s['status'] not in ('ready', 'running', 'verification'):
            errors.append('Run cannot certify in status ' + s['status'])
        if s['usage']['cost'] > s['contract']['budget']['max_cost']:
            errors.append('Cost budget exceeded')
        elapsed = session_elapsed(s)
        if elapsed > s['contract']['budget']['max_seconds']:
            errors.append('Time budget exhausted')
        try:
            if s['contract']['program']:
                import planning
                gate = planning.integration_readiness(s['contract']['program'], s['workstreams'], s['contract']['project_root'])
                if not gate['ready'] or not s['integration'] or s['integration']['workstreams_hash'] != digest(s['workstreams']):
                    errors.append('Required work or integration is unready')
                elif file_hash(s['integration']['evidence']['path']) != s['integration']['evidence']['sha256']:
                    errors.append('Integration evidence changed')
            if s['contract']['mode'] == 'artifact':
                if not s['pieces'] or any(p['status'] != 'converged' for p in s['pieces'].values()):
                    errors.append('Artifact pieces have not met frozen consecutive-win condition')
                for piece in s['pieces'].values():
                    if file_hash(piece['artifact_path']) != piece['artifact_hash']:
                        errors.append('Converged artifact bytes changed')
        except (ValueError, OSError, KeyError) as exc:
            errors.append('Missing or stale acceptance/integration evidence: ' + str(exc))
        inspections = {}
        inspection_failures = []
        methods = s['contract']['brief']['inspection_methods']
        reports = data.get('inspection_reports', {})
        for method, key in (('reader-proxy', 'reader'), ('claim-audit', 'claims')):
            if method not in methods:
                continue
            try:
                snapshot = freeze(reports[key])
                observed = read_json(snapshot['path'])
                inspections[key] = {'file': snapshot, 'result': observed}
                inspected = observed.get('artifact', {})
                expected_hash = locals().get('actual', {}).get('sha256', '').removeprefix('sha256:')
                require(inspected.get('sha256') == expected_hash, 'Inspection artifact mismatch')
                require(observed.get('status') in ('passed', 'failed', 'unverifiable'), 'Invalid inspection result')
                if observed['status'] == 'unverifiable':
                    errors.append(method + ' reported unverifiable')
                elif observed['status'] == 'failed':
                    inspection_failures.append(method + ' reported substantive defects')
                if key == 'reader':
                    require(any(e['role'] == 'reader' and e['status'] == 'completed' for e in s['launches'].values()), 'Completed reader-proxy host receipt required')
                    expected = s['contract']['frozen']['reader_questions']['sha256'].removeprefix('sha256:')
                    require(observed.get('questions', {}).get('sha256') == expected, 'Reader question hash mismatch')
            except (KeyError, ValueError, OSError) as exc:
                errors.append('Missing/invalid ' + method + ' evidence: ' + str(exc))
        context['eligible'] = not errors
        result = review.compute_consensus(data.get('verdicts'), context, policy.get('policy'))
        result['validation_errors'] = errors + result['validation_errors']
        if errors:
            result['consensus'] = 'unverifiable'
        elif inspection_failures and result['consensus'] != 'unverifiable':
            result['consensus'] = 'failed'
        result['inspection_failures'] = inspection_failures
        result.update(request_hash=digest(data), verdicts=data.get('verdicts'), context=context,
                      artifact=locals().get('actual'), inspections=inspections)
        s['verification'] = result
        if s['status'] not in ('exhausted', 'stopped'):
            s['status'] = result['consensus']
        return result, True
    result = mutate(run_dir, 'finalize', apply, check_files=False)
    result = dict(result, exports=report(run_dir))
    return result


def export_text(path, body):
    require(not path.is_symlink(), 'Symlink output refused')
    fd, temp = tempfile.mkstemp(prefix='.view-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(body); handle.flush(); os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def session_elapsed(s):
    session = s['session']
    extra = max(0, (dt.datetime.now(dt.timezone.utc) - stamp(session['active_since'])).total_seconds()) if session['active_since'] else 0
    return session['elapsed_seconds'] + extra


def accrue_time(s, uncertain=False):
    session = s['session']
    since = session['active_since'] or session.get('pending_since')
    if not since:
        return
    uncertain = uncertain or bool(session.get('pending_since'))
    elapsed = max(0, (dt.datetime.now(dt.timezone.utc) - stamp(since)).total_seconds())
    if uncertain:
        elapsed = min(elapsed, max(0, s['contract']['budget']['max_seconds'] - session['elapsed_seconds']))
        session['uncertain_seconds'] += elapsed
        s['usage']['uncertain_seconds'] += elapsed
    else:
        s['usage']['elapsed_seconds'] += elapsed
    session['elapsed_seconds'] += elapsed
    if session.get('pending_since'):
        session['pending_since'] = now()
    else:
        session['active_since'] = now()


def pause(run_dir, data):
    def apply(s):
        require(s['status'] in ('ready', 'running', 'verification'), 'Only active work can pause')
        require(not any(e['status'] == 'reserved' for e in s['launches'].values()), 'Reconcile active launches before pausing')
        s['status'], s['stop_reason'] = 'paused', nonempty(data.get('reason'), 'reason')
        s['session']['active_since'] = None
        return {'status': 'paused', 'session': dict(s['session'])}, True
    return mutate(run_dir, 'pause', apply)


def write_snapshot(paths, exclusions=()):
    """Bounded byte snapshot of declared output roots, never an OS sandbox."""
    snapshot, count = {}, 0
    excluded = [Path(p) for p in exclusions]
    def skip(path):
        return any(path == p or p in path.parents for p in excluded)
    def failure(error):
        raise error
    for target in paths:
        root = Path(target).resolve()
        if skip(root):
            continue
        if root.is_dir():
            candidates = []
            for base, dirs, files in os.walk(root, onerror=failure, followlinks=False):
                dirs[:] = [d for d in dirs if not skip(Path(base) / d)]
                nodes = [Path(base) / n for n in dirs + files if not skip(Path(base) / n)]
                count += len(nodes)
                require(count <= 10000, 'Write scope too large for bounded snapshot; declare narrower targets')
                require(not any(p.is_symlink() for p in nodes), 'Symlink in snapshot scope; declare narrower directly owned targets')
                candidates.extend(Path(base) / n for n in files if not skip(Path(base) / n))
        else:
            candidates = [root]
        for path in candidates:
            if path.is_file():
                actual = scope_path(path, [str(root)])
                snapshot[str(actual)] = file_hash(actual)
    return snapshot


def validate_writes(entry, receipt, changed_outputs=False, launches=()):
    require(receipt.get('write_observations_complete') is True, 'Host must attest complete observed write set')
    observations = receipt.get('write_observations')
    require(isinstance(observations, list), 'Host write observations required')
    before, after = entry['before_files'], write_snapshot(entry['watch_roots'], entry['snapshot_exclusions'])
    changed = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
    def owned(path, roots):
        p = Path(path)
        return any(p == Path(root) or Path(root) in p.parents for root in roots)
    concurrent_scopes = [p for other in launches if other['id'] != entry['id']
                         and other['role'] in ('builder', 'smoother')
                         and (other['status'] == 'reserved' or other.get('completed_at', '') >= entry['reserved_at'])
                         for p in other['write_paths']]
    foreign = {p for p in changed if not owned(p, entry['write_paths'])}
    require(all(owned(p, concurrent_scopes) for p in foreign), 'Unreported out-of-scope write or deletion in declared output area')
    changed -= foreign
    seen = set()
    for observation in observations:
        require(isinstance(observation, dict), 'Invalid write observation')
        path = str(scope_path(observation['path'], entry['write_paths']))
        require(path not in seen, 'Duplicate observed write')
        seen.add(path)
        require('before_sha256' in observation and 'after_sha256' in observation, 'Before/after hashes or null required')
        require(observation['before_sha256'] == before.get(path) and observation['after_sha256'] == after.get(path), 'Observed write hashes differ from captured files')
    require(changed <= seen, 'Observed write set omits actual changed/deleted files')
    require(not changed_outputs or observations, 'Claimed changes require observed write evidence')
    return {'before': before, 'after': after, 'changed': sorted(changed), 'concurrent_lane_changes': sorted(foreign),
            'snapshot_exclusions': entry['snapshot_exclusions'], 'boundary': 'Declared output roots only; concurrent ownership is reservation-based, actual actor and other locations require host audit.'}
