#!/usr/bin/env python3
"""Pure, local validation for optional subordinate advisor packets.

The caller supplies a trusted Gauntlet snapshot, never worker-provided context.
This module performs no I/O, launches, model calls, or canonical state writes.
"""
from __future__ import annotations
import copy
import hashlib
import json
import math
import re
from pathlib import PurePosixPath

OWNERS = {k: 'gauntlet' for k in (
    'state', 'budget', 'approval', 'integration', 'final_answer', 'terminal_verdict')}
PERSPECTIVES = {'acceptance/scope', 'evidence/correctness', 'integration/adversarial'}
SHA = re.compile(r'^[0-9a-f]{64}$')


class AdvisorError(ValueError):
    """Invalid packet or missing authority; no side effects have occurred."""


def need(condition, message):
    if not condition:
        raise AdvisorError(message)


def obj(value, label):
    need(isinstance(value, dict), label + ' must be an object')
    return value


def strings(value, label, empty=False):
    need(isinstance(value, list) and (empty or bool(value)), label + ' must be a list')
    need(all(isinstance(x, str) and x.strip() for x in value), label + ' has invalid strings')
    need(len(value) == len(set(value)), label + ' contains duplicates')
    return value


def digest(value):
    """Canonical packet hash, UTF-8 sorted compact JSON, no trailing newline."""
    try:
        data = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                          allow_nan=False).encode('utf-8')
    except (TypeError, ValueError) as exc:
        raise AdvisorError('packet must be finite JSON data') from exc
    return hashlib.sha256(data).hexdigest()


def path(value):
    need(isinstance(value, str) and value and '\\' not in value, 'invalid relative path')
    p = PurePosixPath(value)
    need(not p.is_absolute() and '..' not in p.parts and str(p) == value and value != '.',
         'paths must be normalized project-relative paths, without traversal')
    need(p.parts[0] != '.gauntlet', 'advisor may not write Gauntlet state')
    return p


def inside(value, root):
    p, r = path(value), path(root)
    return p == r or r in p.parents


def overlap(a, b):
    return inside(a, b) or inside(b, a)


def number(value, label, minimum=0):
    need(type(value) in (int, float) and math.isfinite(value) and value >= minimum,
         label + ' must be finite and nonnegative')
    return value


def limits(value, label):
    value = obj(value, label)
    need(set(value) == {'launches', 'concurrency', 'minutes', 'cost', 'rounds'},
         label + ' requires launches, concurrency, minutes, cost and rounds')
    for key, val in value.items():
        number(val, label + '.' + key)
        if key in {'launches', 'concurrency', 'rounds'}:
            need(type(val) is int, label + '.' + key + ' must be an integer')
    return value


def validate_context(context):
    c = obj(context, 'context')
    need(c.get('host') == 'codex', 'composition is the Codex subordinate route')
    need(c.get('invocations') == {'gauntlet': True, 'advisor': True},
         'both Gauntlet and advisor must be explicitly invoked')
    need(c.get('owners') == OWNERS, 'Gauntlet must own every authority')
    need(isinstance(c.get('run_id'), str) and c['run_id'], 'missing run identity')
    p = obj(c.get('plan'), 'plan')
    need(type(p.get('version')) is int and p['version'] > 0, 'invalid plan version')
    need(isinstance(p.get('sha256'), str) and SHA.fullmatch(p['sha256']), 'invalid plan hash')
    approval = obj(c.get('approval'), 'approval')
    need(approval.get('approved') is True and approval.get('plan') == p
         and approval.get('run_id') == c['run_id'], 'missing or stale plan approval')
    need(PERSPECTIVES <= set(strings(c.get('perspectives'), 'perspectives')),
         'all three Gauntlet verification perspectives are required')
    limits(c.get('remaining'), 'remaining')
    tasks = c.get('tasks')
    need(isinstance(tasks, list) and tasks, 'tasks must be a nonempty list')
    by_id = {}
    for t in tasks:
        obj(t, 'task')
        ident = t.get('task_id')
        need(isinstance(ident, str) and ident and ident not in by_id, 'invalid or duplicate task ID')
        by_id[ident] = t
        need(isinstance(t.get('model'), str) and t['model'].strip(), 'record the selected model')
        need(isinstance(t.get('objective'), str) and t['objective'].strip(), 'missing task objective')
        roots = strings(t.get('write_roots'), 'write_roots', empty=True)
        for root in roots:
            path(root)
        outputs = strings(t.get('outputs'), 'outputs', empty=True)
        for output in outputs:
            need(any(inside(output, r) for r in roots), 'output outside authorized roots')
        strings(t.get('criteria'), 'criteria')
        strings(t.get('evidence_commands'), 'evidence_commands', empty=True)
        strings(t.get('dependencies'), 'dependencies', empty=True)
        limits(t.get('limits'), 'task limits')
        for k, v in t['limits'].items():
            need(v <= c['remaining'][k], 'task exceeds remaining ' + k)
    ancestors = {}
    def visit(ident, trail):
        need(ident in by_id, 'unknown dependency: ' + str(ident))
        need(ident not in trail, 'cyclic task graph')
        if ident in ancestors:
            return ancestors[ident]
        found = set()
        for dep in by_id[ident]['dependencies']:
            found.add(dep)
            found.update(visit(dep, trail | {ident}))
        ancestors[ident] = found
        return found
    for ident in by_id:
        visit(ident, set())
    for i, left in enumerate(tasks):
        for right in tasks[i+1:]:
            serialized = (left['task_id'] in ancestors[right['task_id']]
                          or right['task_id'] in ancestors[left['task_id']])
            need(serialized or not any(overlap(a, b) for a in left['write_roots']
                                       for b in right['write_roots']),
                 'unordered tasks have overlapping write roots')
    return by_id


def validate_composition(packet, context):
    """Validate a manifest against a separately supplied canonical snapshot.

    This does not require an installed advisor and is not dispatch permission.
    """
    validate_context(context)
    obj(packet, 'composition packet')
    need(packet.get('packet_type') == 'CompositionPacket' and packet.get('version') == 1,
         'unsupported composition packet')
    need(set(packet) == {'packet_type', 'version', 'run_id', 'plan', 'owners',
                         'perspectives', 'tasks', 'approval_sha256', 'context_sha256'},
         'unsupported composition fields or competing authority')
    for field in ('run_id', 'plan', 'owners', 'perspectives', 'tasks'):
        need(packet.get(field) == context.get(field), 'composition mismatch: ' + field)
    need(packet.get('approval_sha256') == digest(context['approval']), 'approval binding mismatch')
    need(packet.get('context_sha256') == digest(context), 'canonical context binding mismatch')
    return {'valid': True, 'dispatch_authorized': False, 'run_id': context['run_id'],
            'plan': copy.deepcopy(context['plan']), 'packet_sha256': digest(packet)}


def build_composition_packet(context):
    """Build a static manifest for validation. Does not assert an advisor exists."""
    validate_context(context)
    packet = {key: copy.deepcopy(context[key]) for key in
              ('run_id', 'plan', 'owners', 'perspectives', 'tasks')}
    packet.update(packet_type='CompositionPacket', version=1,
                  approval_sha256=digest(context['approval']), context_sha256=digest(context))
    return packet


def host_record(context, ident, task_id, role):
    """Read only host evidence already captured and trusted by Gauntlet."""
    record = obj(obj(context.get('host_records'), 'host_records').get(ident), 'host record')
    for key, expected in [('run_id', context['run_id']), ('task_id', task_id), ('role', role),
                          ('plan', context['plan']), ('fresh', True), ('forked', False)]:
        need(record.get(key) == expected, 'host record mismatch: ' + key)
    for key in ('host_id', 'session_id', 'request_id'):
        need(isinstance(record.get(key), str) and record[key], 'missing host ' + key)
    for key in ('request_sha256', 'response_sha256'):
        need(isinstance(record.get(key), str) and SHA.fullmatch(record[key]), 'missing host evidence hash')
    need(record.get('successful') is True, 'host creation did not succeed')
    for permission in ('may_approve', 'may_integrate', 'may_update_state', 'may_update_budget',
                       'may_issue_final_verdict', 'may_spawn_workers'):
        need(record.get(permission, False) is False, 'host record claims forbidden authority')
    if role == 'reviewer':
        need(record.get('read_only') is True, 'reviewer must be read-only')
        need(all(record.get(k, False) is False for k in ('may_build', 'may_repair', 'may_write')),
             'reviewer claims write authority')
    return record


def build_task_packet(context, task_id):
    tasks = validate_context(context)
    need(context.get('advisor_available') is True, 'advisor unavailable; do not compose or dispatch')
    need(task_id in tasks, 'unknown task')
    task = tasks[task_id]
    need(all(task['limits'][k] > 0 for k in ('launches', 'concurrency', 'minutes', 'rounds')),
         'task has no execution capacity')
    records = obj(context.get('task_status'), 'canonical task_status')
    need(all(records.get(d) == 'accepted' for d in task['dependencies']), 'dependencies not accepted')
    need(records.get(task_id) == 'authorized', 'task is not ready for packet compilation')
    worker = host_record(context, task.get('worker_record'), task_id, 'worker')
    need(worker.get('model') == task['model'], 'host model differs from selected model')
    return {'packet_type': 'TaskPacket', 'version': 1, 'run_id': context['run_id'],
            'plan': copy.deepcopy(context['plan']), 'owners': copy.deepcopy(OWNERS),
            'task': copy.deepcopy(task), 'worker': copy.deepcopy(worker),
            'approval_sha256': digest(context['approval'])}


def verify_files(records, blobs, label):
    need(isinstance(records, list), label + ' must be a list')
    found = {}
    for entry in records:
        obj(entry, label + ' entry')
        name = entry.get('path')
        path(name)
        need(name not in found, 'duplicate ' + label + ' path')
        need(name in blobs and isinstance(blobs[name], bytes), 'missing raw bytes: ' + name)
        need(hashlib.sha256(blobs[name]).hexdigest() == entry.get('sha256'), 'file hash mismatch: ' + name)
        found[name] = entry['sha256']
    return found


def validate_return_packet(context, task_packet, returned, blobs, review=None):
    """Validate supplied bytes; return registration data, never a terminal verdict.

    Context task_status remains authorized while recompiling the immutable packet;
    the caller must retain that approved task snapshot and separately enforce live
    registration eligibility under its state lock.
    """
    obj(task_packet, 'task packet')
    obj(task_packet.get('task'), 'task packet task')
    obj(blobs, 'file bytes')
    expected = build_task_packet(context, task_packet['task'].get('task_id'))
    need(task_packet == expected, 'task packet differs from authorized snapshot')
    obj(returned, 'return')
    need(returned.get('owners', OWNERS) == OWNERS and 'authority' not in returned,
         'return cannot change authority')
    need(returned.get('packet_type') == 'ReturnPacket', 'wrong return packet type')
    for key in ('run_id', 'plan'):
        need(returned.get(key) == task_packet[key], 'return binding mismatch: ' + key)
    task = task_packet['task']
    need(returned.get('task_id') == task['task_id'], 'return task mismatch')
    need(returned.get('task_packet_sha256') == digest(task_packet), 'task packet hash mismatch')
    need(returned.get('status') in {'succeeded', 'blocked', 'failed', 'escalate'}, 'invalid task status')
    actual = strings(returned.get('actual_write_paths'), 'actual_write_paths', empty=True)
    need(all(any(inside(p, r) for r in task['write_roots']) for p in actual), 'actual writes exceed scope')
    artifacts = verify_files(returned.get('artifacts'), blobs, 'artifacts')
    evidence = verify_files(returned.get('evidence'), blobs, 'evidence')
    need(set(artifacts) <= set(task['outputs']), 'unapproved result artifacts')
    need(set(artifacts) <= set(actual), 'result artifacts missing from actual write set')
    if returned['status'] == 'succeeded':
        need(set(artifacts) == set(task['outputs']), 'successful result lacks expected outputs')
    usage = limits(returned.get('usage'), 'usage')
    need(all(usage[k] <= task['limits'][k] for k in usage), 'task usage exceeded limits')
    commands = returned.get('commands')
    need(isinstance(commands, list) and all(isinstance(x, dict) for x in commands), 'invalid commands')
    need([x.get('command') for x in commands] == task['evidence_commands'], 'command coverage mismatch')
    for command in commands:
        need(type(command.get('exit_code')) is int and command.get('evidence_path') in evidence,
             'command needs exit code and hashed evidence')
        if returned['status'] == 'succeeded':
            need(command['exit_code'] == 0, 'successful task contains failed command')
    coverage = obj(returned.get('criterion_to_evidence'), 'criterion_to_evidence')
    need(set(coverage) == set(task['criteria']), 'criterion coverage mismatch')
    for refs in coverage.values():
        strings(refs, 'criterion evidence')
        need(set(refs) <= (set(evidence) | set(artifacts)), 'criterion refers to missing evidence')
    if review is not None:
        obj(review, 'review')
        need(review.get('owners', OWNERS) == OWNERS and 'authority' not in review,
             'review cannot change authority')
        reviewer = host_record(context, task.get('reviewer_record'), task['task_id'], 'reviewer')
        need(reviewer['session_id'] != task_packet['worker']['session_id'], 'builder cannot review itself')
        need(reviewer['request_id'] != task_packet['worker']['request_id'], 'reviewer must be freshly created')
        need(review.get('reviewer') == reviewer, 'reviewer provenance mismatch')
        need(review.get('packet_type') == 'ReviewPacket' and review.get('run_id') == context['run_id']
             and review.get('plan') == context['plan'] and review.get('task_id') == task['task_id'],
             'review binding mismatch')
        need(review.get('task_packet_sha256') == digest(task_packet)
             and review.get('return_packet_sha256') == digest(returned), 'review packet hash mismatch')
        need(review.get('artifacts') == returned['artifacts'], 'reviewed artifact mismatch')
        need(review.get('verdict') in {'accepted', 'revise', 'blocked', 'cannot-verify'}, 'invalid review verdict')
    return {'valid': True, 'run_id': context['run_id'], 'task_id': task['task_id'],
            'status': returned['status'], 'artifacts': copy.deepcopy(returned['artifacts']),
            'evidence': copy.deepcopy(returned['evidence']), 'usage': copy.deepcopy(usage),
            'task_packet_sha256': digest(task_packet), 'return_packet_sha256': digest(returned),
            'review_packet_sha256': digest(review) if review is not None else None,
            'requires_gauntlet_registration': True, 'terminal_verdict': None}
