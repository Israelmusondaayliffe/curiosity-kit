#!/usr/bin/env python3
"""Gauntlet's local plan validator and dependency-readiness checks.

No tasks, shell commands, or model calls are executed. Paths are checked against
an explicit existing root, including symlink ancestors of not-yet-created files.
Recheck before writes: this is validation, not a race-proof filesystem sandbox.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

class PlanningError(ValueError):
    pass

PROTECTED = {'.git', '.gauntlet', '.ssh', '.aws', '.codex', '.agents'}
BUDGET_KEYS = ('max_elapsed_minutes', 'max_agent_launches', 'max_concurrency',
               'max_critic_rounds_per_workstream')

def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise PlanningError(f'{label} must be a nonempty string')
    return value

def _strings(value, label, empty=False):
    if not isinstance(value, list) or (not value and not empty):
        raise PlanningError(f'{label} must be a list' + ('' if empty else ' with entries'))
    for entry in value:
        _text(entry, label)
    if len(set(value)) != len(value):
        raise PlanningError(f'{label} contains duplicates')
    return value

def _positive(value, label):
    if type(value) is not int or value < 1:
        raise PlanningError(f'{label} must be a positive integer')
    return value

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()

def project_root(root):
    if root is None or not str(root).strip():
        raise PlanningError('an explicit project root is required')
    result = Path(root).expanduser().resolve(strict=True)
    if not result.is_dir():
        raise PlanningError('project root must be an existing directory')
    return result

def paths_overlap(left, right):
    a, b = Path(left), Path(right)
    return a == b or a in b.parents or b in a.parents

def canonical_path(root, target):
    base = project_root(root)
    _text(target, 'path')
    if '\x00' in target or any(c in target for c in '*?[]'):
        raise PlanningError('paths must be literal, without wildcard characters')
    try:
        result = (base / target).resolve(strict=False)
        relative = result.relative_to(base)
    except (ValueError, RuntimeError, OSError) as exc:
        raise PlanningError(f'path escapes root or cannot resolve: {target}') from exc
    if relative == Path('.'):
        raise PlanningError('whole-project ownership or evidence is not allowed')
    return relative.as_posix()

def canonical_scope(root, target, protected_paths=()):
    relative = canonical_path(root, target)
    if any(p in PROTECTED for p in Path(target).parts + Path(relative).parts):
        raise PlanningError(f'protected write target: {target}')
    for protected in protected_paths:
        if paths_overlap(relative, canonical_path(root, protected)):
            raise PlanningError(f'write target overlaps protected path: {target}')
    return relative

def file_reference(reference, root):
    if not isinstance(reference, dict):
        raise PlanningError('file evidence must be {path, sha256}')
    path = canonical_path(root, reference.get('path'))
    expected = reference.get('sha256')
    if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
        raise PlanningError(f'file reference requires sha256: {path}')
    actual = project_root(root) / path
    if not actual.is_file() or hashlib.sha256(actual.read_bytes()).hexdigest() != expected:
        raise PlanningError(f'missing or changed evidence: {path}')
    return {'path': path, 'sha256': expected}

def _graph(program, root):
    p = deepcopy(program)
    if not isinstance(p, dict):
        raise PlanningError('program must be an object')
    _text(p.get('goal'), 'goal')
    budget = p.get('budget')
    if not isinstance(budget, dict):
        raise PlanningError('budget must be an object')
    for key in BUDGET_KEYS:
        _positive(budget.get(key), 'budget.' + key)
    if budget.get('extension_requires_user_approval') is not True:
        raise PlanningError('budget extension requires explicit user approval')
    # Zero paid spending is a valid finite ceiling. No builder-project cap is set here.
    cost = budget.get('max_cost', 0)
    if type(cost) not in (int, float) or cost < 0 or not cost < float('inf'):
        raise PlanningError('budget.max_cost must be finite and nonnegative')
    p['budget']['max_cost'] = cost
    if budget['max_concurrency'] > budget['max_agent_launches']:
        raise PlanningError('concurrency cannot exceed total launches')
    execution = p.get('execution', {})
    if not isinstance(execution, dict):
        raise PlanningError('execution must be an object')
    if 'write_isolation' in execution and execution['write_isolation'] not in (
            'disjoint_targets', 'serialized', 'separate_worktrees'):
        raise PlanningError('unknown write isolation policy')
    streams = p.get('workstreams')
    if not isinstance(streams, list) or not streams:
        raise PlanningError('program requires workstreams')
    panel = _strings(p.get('verification_panel'), 'verification_panel')
    if len(panel) < 3:
        raise PlanningError('at least three verification perspectives are required')
    protected = list(_strings(p.get('protected_paths', []), 'protected_paths', empty=True))
    bars = p.get('external_bar', [])
    if not isinstance(bars, list):
        raise PlanningError('external_bar must be a list of file references')
    p['external_bar'] = [file_reference(ref, root) for ref in bars]
    if len({r['path'] for r in p['external_bar']}) != len(bars):
        raise PlanningError('external_bar has duplicate paths')
    protected += [ref['path'] for ref in p['external_bar']]
    if p.get('reader_questions') is not None:
        p['reader_questions'] = file_reference(p['reader_questions'], root)
        protected.append(p['reader_questions']['path'])
    ids = []
    for task in streams:
        if not isinstance(task, dict):
            raise PlanningError('workstream must be an object')
        identifier = _text(task.get('id'), 'workstream.id')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', identifier):
            raise PlanningError('workstream id must be a simple identifier')
        ids.append(identifier)
        for key in ('objective', 'builder_charter', 'critic_charter', 'critic'):
            _text(task.get(key), identifier + '.' + key)
        task.setdefault('owner', identifier + '-builder')
        _text(task['owner'], identifier + '.owner')
        for key in ('dependencies', 'write_targets'):
            _strings(task.get(key), identifier + '.' + key, empty=True)
        for key in ('acceptance_criteria', 'evidence_required', 'stop_conditions'):
            _strings(task.get(key), identifier + '.' + key)
        rounds = _positive(task.get('max_critic_rounds'), identifier + '.max_critic_rounds')
        if rounds > budget['max_critic_rounds_per_workstream']:
            raise PlanningError('workstream critic ceiling exceeds program budget')
        task['write_targets'] = [canonical_scope(root, path, protected) for path in task['write_targets']]
        for i, scope in enumerate(task['write_targets']):
            if any(paths_overlap(scope, other) for other in task['write_targets'][i+1:]):
                raise PlanningError(f'duplicate or nested write targets: {identifier}')
    if len(set(ids)) != len(ids):
        raise PlanningError('duplicate workstream ids')
    tasks = {t['id']: t for t in streams}
    for task in streams:
        if any(d not in tasks for d in task['dependencies']):
            raise PlanningError(f"unknown dependency: {task['id']}")
    pending, visited = set(ids), set()
    while pending:
        ready = sorted(i for i in pending if set(tasks[i]['dependencies']) <= visited)
        if not ready:
            raise PlanningError('workstream dependency cycle')
        visited.update(ready)
        pending.difference_update(ready)
    return p

def _conflict(a, b):
    return any(paths_overlap(x, y) for x in a['write_targets'] for y in b['write_targets'])

def _parallel_limit(program):
    execution = program.get('execution', {})
    if execution.get('write_isolation') == 'serialized' or execution.get('allow_parallel_agents') is False:
        return 1
    return program['budget']['max_concurrency']

def validate_program(program, root):
    """Return an independently copied, normalized program or raise PlanningError."""
    p = _graph(program, root)
    tasks = {t['id']: t for t in p['workstreams']}
    waves = p.get('integration_waves')
    if not isinstance(waves, list) or not waves:
        raise PlanningError('integration_waves must be a nonempty list')
    seen, wave_ids = set(), set()
    for wave in waves:
        if not isinstance(wave, dict):
            raise PlanningError('wave must be an object')
        identifier = _text(wave.get('id'), 'wave.id')
        if identifier in wave_ids:
            raise PlanningError('duplicate wave id')
        wave_ids.add(identifier)
        members = _strings(wave.get('workstreams'), 'wave.workstreams')
        if len(members) > _parallel_limit(p):
            raise PlanningError('wave exceeds max_concurrency')
        for index, member in enumerate(members):
            if member not in tasks or member in seen:
                raise PlanningError('wave contains unknown or duplicate workstream')
            if not set(tasks[member]['dependencies']) <= seen:
                raise PlanningError(f'dependencies must appear in earlier waves: {member}')
            for other in members[:index]:
                if _conflict(tasks[member], tasks[other]):
                    raise PlanningError(f'parallel write scopes overlap: {member}, {other}')
        seen.update(members)
    if seen != set(tasks):
        raise PlanningError('waves must cover every workstream exactly once')
    return p

def compile_waves(program, root):
    """Deterministic dependency waves; overlapping writers are serialized."""
    p = _graph(program, root)
    tasks = {t['id']: t for t in p['workstreams']}
    pending, done, waves = set(tasks), set(), []
    while pending:
        wave = []
        for identifier in sorted(pending):
            if set(tasks[identifier]['dependencies']) <= done and not any(
                    _conflict(tasks[identifier], tasks[other]) for other in wave):
                wave.append(identifier)
                if len(wave) == _parallel_limit(p):
                    break
        waves.append({'id': f'wave-{len(waves)+1}', 'workstreams': wave})
        done.update(wave)
        pending.difference_update(wave)
    return waves

def acceptance_fingerprint(record):
    return digest({key: record.get(key) for key in
                   ('task_hash', 'evidence', 'dependency_evidence')})

def _accepted(tasks, records, identifier, root, checked):
    if identifier in checked:
        return checked[identifier]
    record = records.get(identifier, {})
    valid = isinstance(record, dict) and record.get('status') == 'accepted'
    if valid:
        valid = record.get('task_hash') == digest(tasks[identifier])
    if valid:
        evidence = record.get('evidence')
        valid = isinstance(evidence, list) and bool(evidence)
        if valid:
            try:
                refs = [file_reference(ref, root) for ref in evidence]
                valid = refs == evidence and len({r['path'] for r in refs}) == len(refs)
            except (ValueError, OSError, RuntimeError):
                valid = False
    if valid:
        deps = tasks[identifier]['dependencies']
        bindings = record.get('dependency_evidence')
        valid = isinstance(bindings, dict) and set(bindings) == set(deps)
        if valid:
            valid = all(_accepted(tasks, records, d, root, checked) and
                        bindings[d] == acceptance_fingerprint(records[d]) for d in deps)
    checked[identifier] = bool(valid)
    return bool(valid)

def accepted_workstreams(program, records, root):
    p = validate_program(program, root)
    if not isinstance(records, dict):
        raise PlanningError('workstream state must be an object indexed by id')
    if set(records) - {t['id'] for t in p['workstreams']}:
        raise PlanningError('state contains unknown workstreams')
    if any(not isinstance(record, dict) for record in records.values()):
        raise PlanningError('each workstream state must be an object')
    tasks = {t['id']: t for t in p['workstreams']}
    checked = {}
    return sorted(i for i in tasks if _accepted(tasks, records, i, root, checked))

def ready_workstreams(program, records, root):
    """Return the first unfinished wave's dependency-ready, non-running units.

    Accepted evidence is checked from disk. Wave ordering remains owned by the
    lead; readiness does not dispatch work or authorize external side effects.
    """
    p = validate_program(program, root)
    accepted = set(accepted_workstreams(p, records, root))
    tasks = {t['id']: t for t in p['workstreams']}
    running = [identifier for identifier, r in records.items()
               if isinstance(r, dict) and r.get('status') == 'running']
    capacity = max(0, _parallel_limit(p) - len(running))
    for wave in p['integration_waves']:
        missing = [i for i in wave['workstreams'] if i not in accepted]
        if missing:
            ready = []
            for identifier in sorted(missing):
                record = records.get(identifier, {})
                if record.get('status', 'pending') not in ('pending', 'invalidated'):
                    continue
                if set(tasks[identifier]['dependencies']) <= accepted and not any(
                        _conflict(tasks[identifier], tasks[other]) for other in running):
                    ready.append(identifier)
            return ready[:capacity]
    return []

schedule_ready = ready_workstreams

def acceptance_record(program, records, identifier, evidence, root):
    """Create the evidence binding AFTER a separate critic acceptance gate.

    This function validates dependencies and files, not substantive quality.
    Callers must never equate successfully constructing a record with a verdict.
    """
    p = validate_program(program, root)
    tasks = {t['id']: t for t in p['workstreams']}
    if identifier not in tasks:
        raise PlanningError('unknown workstream')
    accepted = set(accepted_workstreams(p, records, root))
    if not set(tasks[identifier]['dependencies']) <= accepted:
        raise PlanningError('predecessor acceptance evidence is missing or stale')
    if not isinstance(evidence, list) or not evidence:
        raise PlanningError('acceptance requires file evidence')
    refs = [file_reference(ref, root) for ref in evidence]
    if len({r['path'] for r in refs}) != len(refs):
        raise PlanningError('acceptance evidence contains duplicate paths')
    return {'status': 'accepted', 'task_hash': digest(tasks[identifier]),
            'evidence': refs, 'dependency_evidence': {
                d: acceptance_fingerprint(records[d]) for d in tasks[identifier]['dependencies']}}

def integration_readiness(program, records, root):
    p = validate_program(program, root)
    accepted = set(accepted_workstreams(p, records, root))
    missing = sorted({t['id'] for t in p['workstreams']} - accepted)
    return {'ready': not missing, 'missing_or_stale': missing,
            'accepted': sorted(accepted)}

def invalidate_dependents(program, records, changed_task_ids, root):
    """Invalidate changed tasks and every transitive dependent, preserving history."""
    p = validate_program(program, root)
    tasks = {t['id']: t for t in p['workstreams']}
    changed = set(_strings(changed_task_ids, 'changed task ids'))
    if changed - set(tasks):
        raise PlanningError('unknown changed workstream')
    affected = set(changed)
    while True:
        larger = affected | {i for i, t in tasks.items() if set(t['dependencies']) & affected}
        if larger == affected:
            break
        affected = larger
    result = deepcopy(records)
    for identifier in sorted(affected):
        previous = deepcopy(result.get(identifier, {}))
        result[identifier] = {'status': 'invalidated', 'changed_dependencies': sorted(changed),
                              'previous_record': previous}
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'compile', 'ready', 'integration', 'invalidate'))
    parser.add_argument('--project-root', required=True)
    parser.add_argument('--program', required=True, help='JSON program file')
    parser.add_argument('--state', help='JSON map of workstream id to record')
    parser.add_argument('--changed', action='append', default=[])
    args = parser.parse_args(argv)
    try:
        program = json.loads(Path(args.program).read_text())
        records = json.loads(Path(args.state).read_text()) if args.state else {}
        if args.command == 'compile':
            result = deepcopy(program)
            result['integration_waves'] = compile_waves(program, args.project_root)
            result = validate_program(result, args.project_root)
        elif args.command == 'validate':
            result = validate_program(program, args.project_root)
        elif args.command == 'ready':
            result = {'ready': ready_workstreams(program, records, args.project_root)}
        elif args.command == 'integration':
            result = integration_readiness(program, records, args.project_root)
        else:
            result = invalidate_dependents(program, records, args.changed, args.project_root)
        print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
        return 0
    except (ValueError, TypeError, KeyError, OSError, RuntimeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
