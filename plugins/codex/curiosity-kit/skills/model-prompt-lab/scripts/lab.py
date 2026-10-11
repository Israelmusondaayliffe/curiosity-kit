#!/usr/bin/env python3
"""Offline, plan-bound evidence processing. Python 3.9+, standard library only.

No providers, plugins, subprocesses, arbitrary scorers, or implicit file reads.
A digest establishes content identity, not evidence truth or prior registration.
"""
import argparse
import datetime
import hashlib
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction


class ContractError(ValueError):
    pass


REVIEW_CHECKS = ('chronology', 'sample_adequacy', 'data_rights', 'comparability',
                 'grading', 'isolation', 'deployment_scope')
METRICS = {'trial_pass_rate': 'high', 'mean_score': 'high', 'mean_latency_ms': 'low',
           'total_latency_ms': 'low', 'mean_cost': 'low', 'total_cost': 'low'}
TRANSIENT = ('timeout', 'transport_error')
STATUS = ('ok', 'refusal', 'timeout', 'transport_error', 'permission_denied', 'error', 'safety_stop')
TRUNCATED = ('max_tokens', 'length', 'truncated', 'incomplete')


def need(condition, message):
    if not condition:
        raise ContractError(message)


def obj(value, label):
    need(type(value) is dict, label + ' must be an object')


def fields(value, required, optional=(), label='object'):
    obj(value, label)
    need(set(required) <= set(value), label + ': missing ' + str(sorted(set(required) - set(value))))
    need(set(value) <= set(required) | set(optional), label + ': unknown fields ' + str(sorted(set(value) - set(required) - set(optional))))


def string(value, label):
    need(type(value) is str and bool(value.strip()), label + ' must be a nonempty string')


def number(value, label, minimum=0, maximum=None, nullable=False):
    if value is None and nullable:
        return
    need(type(value) in (int, float) and math.isfinite(value), label + ' must be a finite number (not boolean)')
    need(value >= minimum and (maximum is None or value <= maximum), label + ' out of range')


def integer(value, label, minimum=1):
    need(type(value) is int and value >= minimum, label + ' must be an integer >= ' + str(minimum))


def json_tree(value):
    if type(value) is dict:
        for k, v in value.items():
            need(type(k) is str, 'JSON keys must be strings')
            json_tree(v)
    elif type(value) is list:
        for v in value:
            json_tree(v)
    elif type(value) is float:
        need(math.isfinite(value), 'nonfinite JSON number')
    else:
        need(value is None or type(value) in (str, int, bool), 'not a JSON value')


def loads(text):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ContractError('nonfinite JSON number: ' + value)
    try:
        result = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, RecursionError) as exc:
        raise ContractError(str(exc)) from exc
    json_tree(result)
    return result


def canonical(value):
    json_tree(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def validate_plan(p):
    json_tree(p)
    fields(p, ('schema', 'experiment', 'population', 'environment', 'baseline', 'repetitions',
               'candidates', 'cases', 'retry', 'resources', 'rule'), ('stopping_rules',))
    need(p['schema'] == 'mpl-plan-v1', 'unsupported plan schema')
    if 'stopping_rules' in p:
        need(type(p['stopping_rules']) is list and len(p['stopping_rules']) > 0, 'stopping_rules must be a nonempty list')
        for rule in p['stopping_rules']: string(rule, 'stopping rule')
    for key in ('experiment', 'population', 'baseline'):
        string(p[key], key)
    obj(p['environment'], 'environment')
    for key in ('host', 'profile_revision'):
        string(p['environment'].get(key), 'environment.' + key)
    integer(p['repetitions'], 'repetitions')
    need(type(p['candidates']) is list and len(p['candidates']) >= 2, 'at least two candidates required')
    need(type(p['cases']) is list and len(p['cases']) > 0, 'cases must be a nonempty list')
    for candidate in p['candidates']:
        fields(candidate, ('id', 'prompt', 'native_config', 'tools', 'parser'))
        string(candidate['id'], 'candidate.id'); string(candidate['prompt'], 'candidate.prompt')
        obj(candidate['native_config'], 'native_config'); obj(candidate['parser'], 'parser')
        need(type(candidate['tools']) is list, 'tools must be a list')
    for case in p['cases']:
        fields(case, ('id', 'input', 'demonstrations', 'output_contract', 'expected', 'scorer', 'exposure', 'family'))
        string(case['id'], 'case.id'); string(case['family'], 'case.family')
        need(type(case['demonstrations']) is list, 'demonstrations must be a list')
        need(type(case['output_contract']) in (str, dict), 'output_contract must be text or object')
        need(case['exposure'] in ('held_out', 'development', 'unknown'), 'unsupported case exposure')
        s = case['scorer']; obj(s, 'scorer')
        need(s.get('kind') in ('exact_text', 'json_equal', 'imported'), 'unsupported scorer; no code/formulas executed')
        if s['kind'] == 'imported':
            fields(s, ('kind', 'rubric', 'pass_threshold')); string(s['rubric'], 'rubric')
            number(s['pass_threshold'], 'pass_threshold', maximum=1)
        else:
            fields(s, ('kind',))
            if s['kind'] == 'exact_text':
                need(type(case['expected']) is str, 'exact_text expected must be a string')
    for key in ('candidates', 'cases'):
        ids = [item['id'] for item in p[key]]
        need(len(set(ids)) == len(ids), 'duplicate ' + key + ' identity')
    need(p['baseline'] in [c['id'] for c in p['candidates']], 'baseline is not a candidate')
    retry = p['retry']; fields(retry, ('max_attempts', 'transient_statuses'))
    integer(retry['max_attempts'], 'max_attempts')
    need(type(retry['transient_statuses']) is list and all(type(x) is str and x in TRANSIENT for x in retry['transient_statuses']), 'only timeout/transport_error retries supported')
    need(len(set(retry['transient_statuses'])) == len(retry['transient_statuses']), 'duplicate retry category')
    r = p['resources']; fields(r, ('currency', 'cost_basis', 'latency_region', 'max_total_cost', 'max_candidate_mean_cost'))
    for key in ('currency', 'latency_region'): string(r[key], key)
    need(r['cost_basis'] in ('measured', 'estimated_marginal'), 'unsupported cost basis')
    for key in ('max_total_cost', 'max_candidate_mean_cost'): number(r[key], key, nullable=True)
    rule = p['rule']; fields(rule, ('metric', 'aggregation', 'threshold', 'minimum_improvement', 'tie'),
                            ('quality_threshold', 'on_insufficient_improvement'))
    need(rule['metric'] in METRICS, 'unsupported metric; use a separately justified manual analysis')
    need(rule['aggregation'] == 'uniform', 'only uniform fixed-design aggregation supported')
    need(rule['tie'] == 'no_decision', 'only no_decision ties supported')
    need(rule.get('on_insufficient_improvement', 'no_decision') in ('no_decision', 'retain_baseline'), 'unsupported improvement fallback')
    number(rule['threshold'], 'threshold', maximum=1 if METRICS[rule['metric']] == 'high' else None)
    number(rule['minimum_improvement'], 'minimum_improvement')
    if METRICS[rule['metric']] == 'low': need('quality_threshold' in rule, 'resource ranking requires quality_threshold')
    if 'quality_threshold' in rule: number(rule['quality_threshold'], 'quality_threshold', maximum=1)
    return p


def freeze(plan):
    validate_plan(plan)
    # Round trip prevents callers from mutating the envelope through the input object.
    return {'schema': 'mpl-frozen-v1', 'digest': digest(plan), 'plan': loads(canonical(plan)),
            'frozen_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'identity_limit': 'Local content receipt, not proof of preregistration, permission, or remote model identity.'}


def check_frozen(f):
    fields(f, ('schema', 'digest', 'plan', 'frozen_at', 'identity_limit'))
    need(f['schema'] == 'mpl-frozen-v1', 'unsupported frozen schema')
    need(f['digest'] == digest(f['plan']), 'frozen plan digest mismatch')
    string(f['frozen_at'], 'frozen_at'); string(f['identity_limit'], 'identity_limit')
    return validate_plan(f['plan'])


def prepare(f):
    p = check_frozen(f)
    packets = []
    for c in p['candidates']:
        for k in p['cases']:
            for rep in range(1, p['repetitions'] + 1):
                packets.append({'candidate': c['id'], 'case': k['id'], 'repetition': rep,
                                'prompt': c['prompt'], 'native_config': c['native_config'], 'tools': c['tools'],
                                'parser': c['parser'], 'input': k['input'], 'demonstrations': k['demonstrations'],
                                'output_contract': k['output_contract']})
    identities = {'plan': f['digest'], 'candidates': {c['id']: digest(c) for c in p['candidates']},
                  'cases': {k['id']: digest(k) for k in p['cases']}}
    return {'schema': 'mpl-packets-v1', 'packets': packets, 'identities': identities,
            'warning': 'Allowed-field projection only. Host must enforce evaluator isolation; IDs must be neutral if blinding is required. Do not give the whole plan, identities or provenance receipt to the candidate.'}


def check_review(review):
    if review is None: return
    fields(review, ('reviewer', 'receipt', 'scope', 'limitations', 'checks'))
    for key in ('reviewer', 'receipt', 'scope'): string(review[key], 'review.' + key)
    need(type(review['limitations']) is list, 'review limitations must be a list')
    for limitation in review['limitations']: string(limitation, 'limitation')
    fields(review['checks'], REVIEW_CHECKS)
    for key, check in review['checks'].items():
        fields(check, ('status', 'evidence'))
        need(check['status'] in ('supported', 'unknown', 'failed'), 'invalid review status')
        string(check['evidence'], 'review evidence')


def grade(attempt, case):
    """Return (score, passed, provenance); grading failure is unknown, never zero."""
    s = case['scorer']
    if attempt['status'] not in ('ok', 'refusal'):
        result = (None, None, 'terminal_execution_failure')
    elif s['kind'] == 'exact_text':
        score = int(attempt['output'] == case['expected'])
        result = (score, bool(score), 'recomputed_exact_text')
    elif s['kind'] == 'json_equal':
        try:
            actual = loads(attempt['output'])
            score = int(canonical(actual) == canonical(case['expected']))
        except ContractError:
            score = 0
        result = (score, bool(score), 'recomputed_json_equal')
    else:
        g = attempt.get('assessment')
        if g is None: return (None, None, 'missing_imported_assessment')
        obj(g, 'assessment')
        required = ('status', 'grader', 'grader_config', 'rubric_digest', 'output_digest', 'receipt', 'explanation', 'score')
        if 'score' in g: number(g['score'], 'assessment.score', maximum=1, nullable=True)
        if not set(required) <= set(g): return (None, None, 'unsupported_import_missing_receipt_fields')
        fields(g, required)
        need(g['status'] in ('ok', 'error'), 'assessment status invalid')
        obj(g['grader_config'], 'grader_config')
        for key in ('grader', 'receipt', 'explanation'): string(g[key], 'assessment.' + key)
        need(g['rubric_digest'] == digest(s), 'assessment rubric identity mismatch')
        need(g['output_digest'] == digest(attempt['output']), 'assessment output identity mismatch')
        number(g['score'], 'assessment.score', maximum=1, nullable=g['status'] == 'error')
        if g['status'] == 'error':
            need(g['score'] is None, 'failed assessment must have null score')
            return (None, None, 'imported_grader_failure')
        result = (g['score'], g['score'] >= s['pass_threshold'], 'attributed_import_not_independently_verified')
    if 'score' in attempt:
        number(attempt['score'], 'supplied score', maximum=1)
        need(attempt['score'] == result[0], 'supplied score contradicts recomputed/attributed score')
    if 'passed' in attempt:
        need(type(attempt['passed']) is bool and attempt['passed'] == result[1], 'supplied passed contradicts grade')
    return result


def normalize(f, raw):
    p = check_frozen(f); json_tree(raw)
    fields(raw, ('schema', 'plan_digest', 'attempts', 'campaign_status'), ('review',))
    need(raw['schema'] == 'mpl-raw-v1', 'unsupported raw schema')
    need(raw['plan_digest'] == f['digest'], 'raw plan identity mismatch')
    need(raw['campaign_status'] in ('complete', 'partial', 'budget_stop', 'safety_stop', 'permission_stop'), 'invalid campaign status')
    need(type(raw['attempts']) is list, 'attempts must be a list')
    check_review(raw.get('review'))
    candidates = {c['id']: c for c in p['candidates']}; cases = {k['id']: k for k in p['cases']}
    groups = defaultdict(list)
    for a in raw['attempts']:
        fields(a, ('candidate', 'case', 'repetition', 'attempt', 'plan_digest', 'candidate_digest', 'case_digest',
                   'status', 'stop_reason', 'output', 'evidence', 'source', 'cost', 'latency_ms', 'usage'),
               ('assessment', 'score', 'passed', 'trace'))
        string(a['candidate'], 'candidate'); string(a['case'], 'case')
        need(a['candidate'] in candidates and a['case'] in cases, 'unknown candidate/case')
        integer(a['repetition'], 'repetition'); integer(a['attempt'], 'attempt')
        need(a['repetition'] <= p['repetitions'], 'repetition outside frozen design')
        need(a['attempt'] <= p['retry']['max_attempts'], 'attempt exceeds frozen retry cap')
        need(a['plan_digest'] == f['digest'], 'attempt plan identity mismatch')
        need(a['candidate_digest'] == digest(candidates[a['candidate']]), 'candidate identity mismatch')
        need(a['case_digest'] == digest(cases[a['case']]), 'case identity mismatch')
        need(a['status'] in STATUS, 'unsupported attempt status')
        string(a['stop_reason'], 'stop_reason'); need(type(a['output']) is str, 'raw output must be text')
        need(a['evidence'] in ('observed', 'synthetic', 'unknown'), 'invalid evidence class')
        obj(a['source'], 'source'); string(a['source'].get('receipt'), 'source.receipt')
        if 'observed_model' in a['source'] and a['source']['observed_model'] is not None:
            string(a['source']['observed_model'], 'observed_model')
        number(a['cost'], 'cost', nullable=True); number(a['latency_ms'], 'latency_ms', nullable=True)
        need(a['usage'] is None or type(a['usage']) is dict, 'usage must be object or null')
        if a['usage'] is not None:
            for key, value in a['usage'].items(): number(value, 'usage.' + key, nullable=True)
        key = (a['candidate'], a['case'], a['repetition'])
        groups[key].append(a)
    expected = [(c['id'], k['id'], r) for c in p['candidates'] for k in p['cases'] for r in range(1, p['repetitions'] + 1)]
    trials = []; blockers = []
    for key in expected:
        attempts = groups.get(key, [])
        if not attempts: continue
        attempts = sorted(attempts, key=lambda a: a['attempt'])
        need([a['attempt'] for a in attempts] == list(range(1, len(attempts) + 1)), 'duplicate or nonconsecutive attempt identity: ' + str(key))
        for a in attempts[:-1]:
            need(a['status'] in p['retry']['transient_statuses'] and a['stop_reason'] not in TRUNCATED + ('safety_stop', 'permission_denied'),
                 'retry after terminal/nonretryable attempt: ' + str(key))
            need('assessment' not in a and 'score' not in a and 'passed' not in a, 'retryable failure cannot carry a grade')
        last = attempts[-1]
        score, passed, provenance = grade(last, cases[key[1]])
        if 'score' in last:
            number(last['score'], 'supplied score', maximum=1)
            need(last['score'] == score, 'supplied score contradicts recomputed/attributed score')
        if 'passed' in last:
            need(type(last['passed']) is bool and last['passed'] == passed, 'supplied passed contradicts grade')
        incomplete = last['stop_reason'] in TRUNCATED
        if incomplete: blockers.append('incomplete_delivery')
        if last['status'] in ('ok', 'refusal') and last['stop_reason'] not in ('complete', 'stop', 'end_turn', 'refusal') + TRUNCATED:
            blockers.append('unknown_delivery')
        if last['status'] == 'safety_stop' or last['stop_reason'] == 'safety_stop': blockers.append('campaign_safety_stop')
        if last['status'] == 'permission_denied' or last['stop_reason'] == 'permission_denied': blockers.append('permission_stop')
        if provenance == 'terminal_execution_failure': blockers.append('terminal_execution_failure')
        if score is None: blockers.append('missing_grade')
        trials.append({'candidate': key[0], 'case': key[1], 'repetition': key[2], 'attempts': len(attempts),
                       'terminal_attempt': last['attempt'], 'status': last['status'], 'stop_reason': last['stop_reason'],
                       'score': score, 'passed': passed, 'grading': provenance,
                       'total_cost': total([a['cost'] for a in attempts]),
                       'total_latency_ms': total([a['latency_ms'] for a in attempts])})
    missing = [list(key) for key in expected if key not in groups]
    if missing: blockers.append('missing_trials')
    if raw['campaign_status'] != 'complete': blockers.append('campaign_' + raw['campaign_status'])
    aggregates = {}
    for cid in candidates:
        ts = [t for t in trials if t['candidate'] == cid]
        count = len(ts); scores = [t['score'] for t in ts]
        costs = [t['total_cost'] for t in ts]; times = [t['total_latency_ms'] for t in ts]
        known_grades = count > 0 and None not in scores
        aggregates[cid] = {'trials': count, 'attempts': sum(t['attempts'] for t in ts),
                           'mean_score': average(scores) if known_grades else None,
                           'pass_rate': sum(t['passed'] for t in ts) / count if known_grades else None,
                           'score_min': min(scores) if known_grades else None,
                           'score_max': max(scores) if known_grades else None,
                           'total_cost': total(costs), 'mean_cost': average(costs),
                           'total_latency_ms': total(times), 'mean_latency_ms': average(times)}
    return {'schema': 'mpl-normalized-v1', 'plan_digest': f['digest'], 'raw_digest': digest(raw), 'raw': raw,
            'attempt_count': len(raw['attempts']), 'trial_count': len(trials), 'expected_trials': len(expected),
            'missing_trials': missing, 'trials': trials, 'aggregates': aggregates, 'blockers': sorted(set(blockers))}


def total(values):
    if not values or None in values: return None
    value = float(sum((Fraction(str(v)) for v in values), Fraction(0)))
    need(math.isfinite(value), 'aggregate overflow')
    return value


def average(values):
    if not values or None in values: return None
    value = float(sum((Fraction(str(v)) for v in values), Fraction(0)) / len(values))
    need(math.isfinite(value), 'aggregate overflow')
    return value


def verify(f, n):
    obj(n, 'normalized artifact')
    need('raw' in n, 'normalized artifact must retain raw evidence')
    rebuilt = normalize(f, n['raw'])
    need(canonical(n) == canonical(rebuilt), 'normalized evidence/aggregate mismatch')
    return rebuilt


def decide(f, normalized):
    n = verify(f, normalized); p = f['plan']; raw = n['raw']; rule = p['rule']
    blockers = list(n['blockers']); arithmetic_blockers = list(blockers)
    metric = rule['metric']; direction = METRICS[metric]
    key = 'pass_rate' if metric == 'trial_pass_rate' else metric
    values = {cid: a[key] for cid, a in n['aggregates'].items()}
    if None in values.values(): arithmetic_blockers.append('required_metric_unknown')
    all_costs = [a['cost'] for a in raw['attempts']]
    if p['resources']['max_total_cost'] is not None:
        cost = total(all_costs)
        if cost is None: arithmetic_blockers.append('required_cost_unknown')
        elif cost > p['resources']['max_total_cost']: arithmetic_blockers.append('campaign_budget_exceeded')
    ceiling = p['resources']['max_candidate_mean_cost']
    if ceiling is not None and any(a['mean_cost'] is None for a in n['aggregates'].values()):
        arithmetic_blockers.append('required_cost_unknown')
    hypothetical = 'no_decision'; eligible = []
    if not arithmetic_blockers:
        for cid, value in values.items():
            a = n['aggregates'][cid]
            quality = a['mean_score']
            primary_ok = value >= rule['threshold'] if direction == 'high' else value <= rule['threshold']
            quality_ok = quality is not None and quality >= rule.get('quality_threshold', 0)
            cost_ok = ceiling is None or a['mean_cost'] <= ceiling
            if primary_ok and quality_ok and cost_ok: eligible.append(cid)
        if eligible:
            best_value = (max if direction == 'high' else min)(values[cid] for cid in eligible)
            winners = [cid for cid in eligible if values[cid] == best_value]
            if len(winners) == 1:
                best = winners[0]; baseline = p['baseline']
                delta = Fraction(str(values[best])) - Fraction(str(values[baseline]))
                if direction == 'low': delta = -delta
                if best == baseline or delta >= Fraction(str(rule['minimum_improvement'])):
                    hypothetical = 'select:' + best
                elif rule.get('on_insufficient_improvement') == 'retain_baseline' and baseline in eligible:
                    hypothetical = 'select:' + baseline
    blockers = arithmetic_blockers
    classes = sorted(set(a['evidence'] for a in raw['attempts']))
    if 'synthetic' in classes: blockers.append('synthetic_evidence')
    if 'unknown' in classes: blockers.append('unknown_evidence')
    review = raw.get('review')
    if review is None: blockers.append('missing_review')
    else:
        for name, check in review['checks'].items():
            if check['status'] != 'supported': blockers.append('review:' + name)
        if review['scope'] != p['population']: blockers.append('review_scope_mismatch')
    if any(k['exposure'] != 'held_out' for k in p['cases']): blockers.append('cases_not_held_out')
    if hypothetical == 'no_decision': blockers.append('rule_not_decisive')
    limitations = [
        'Review receipts and observed labels are attributed assertions, not authenticated by this helper.',
        'Hashes bind local content, not chronology, permission, remote weights, or truth.',
        'Full matrix is accounting, not proof of sample adequacy or independent observations.',
        'No statistical significance or uncertainty interval is inferred.',
        'Latency covers the declared region; it is not automatically end-to-end task latency.'
    ]
    if None in all_costs: limitations.append('Cost unknown; no affordability claim.')
    if p['resources']['cost_basis'] == 'estimated_marginal': limitations.append('Cost is estimated marginal cost, not a billing total.')
    if any(a['source'].get('observed_model') is None for a in raw['attempts']):
        limitations.append('At least one served model/version is unobserved; remote drift is unresolved.')
    if review: limitations.extend(review['limitations'])
    return {'schema': 'mpl-decision-v1', 'plan_digest': f['digest'], 'normalized_digest': digest(n),
            'outcome': hypothetical if not blockers else 'no_decision',
            'hypothetical_rule_outcome': hypothetical, 'eligible_candidates': eligible,
            'metric': metric, 'direction': direction, 'values': values,
            'blockers': sorted(set(blockers)), 'evidence_classes': classes,
            'review_authentication': 'not_verified', 'limitations': limitations}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('check-plan', 'freeze', 'prepare', 'normalize', 'decide', 'verify'):
        cmd = sub.add_parser(name)
        cmd.add_argument('input', help='plan for check-plan/freeze; frozen plan otherwise')
        if name in ('normalize', 'decide', 'verify'): cmd.add_argument('evidence')
        if name not in ('check-plan', 'verify'): cmd.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        def read(path):
            with open(path, encoding='utf-8') as handle: return loads(handle.read())
        first = read(args.input)
        if args.command == 'check-plan': validate_plan(first); result = {'valid': True, 'digest': digest(first)}
        elif args.command == 'freeze': result = freeze(first)
        elif args.command == 'prepare': result = prepare(first)
        elif args.command == 'normalize': result = normalize(first, read(args.evidence))
        elif args.command == 'decide': result = decide(first, read(args.evidence))
        else: verify(first, read(args.evidence)); result = {'valid': True, 'claim': 'structural identity and recomputed arithmetic only'}
        encoded = json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False) + '\n'
        if hasattr(args, 'out'):
            with open(args.out, 'x', encoding='utf-8') as handle: handle.write(encoded)
            print(json.dumps({'written': args.out, 'outcome': result.get('outcome')}))
        else: print(encoded, end='')
        return 0
    except (ContractError, OSError, ValueError, TypeError, RecursionError, OverflowError) as exc:
        print('error: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
