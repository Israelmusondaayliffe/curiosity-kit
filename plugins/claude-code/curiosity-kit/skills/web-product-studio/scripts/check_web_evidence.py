#!/usr/bin/env python3
"""Check Web record shape and exact byte/ID joins; never certify behavior or pixels."""
import argparse
import hashlib
import json
import math
import re
import stat
import sys
from pathlib import Path
from urllib.parse import urlsplit

KINDS = ('route', 'flow', 'visual-contract', 'visual-review', 'sites')
STATUS = ('unrun', 'passed', 'failed', 'blocked')
HASH = re.compile(r'^[0-9a-f]{64}$')


def _json(payload):
    def constant(value):
        raise ValueError('non-finite JSON number: ' + value)
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(payload, parse_constant=constant, object_pairs_hook=pairs)


class Check:
    """Per-invocation error accumulator. No state survives validation."""
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.errors = []
        self.active = set()

    def error(self, at, message):
        self.errors.append(at + ': ' + message)

    def obj(self, value, at):
        if not isinstance(value, dict):
            self.error(at, 'must be an object')
            return {}
        return value

    def seq(self, value, at, minimum=0):
        if not isinstance(value, list):
            self.error(at, 'must be a list')
            return []
        if len(value) < minimum:
            self.error(at, 'must contain at least %s item(s)' % minimum)
        return value

    def text(self, value, at):
        if not isinstance(value, str) or not value.strip():
            self.error(at, 'must be a nonempty string')
            return False
        return True

    def texts(self, value, at, minimum=0):
        items = self.seq(value, at, minimum)
        result = []
        for i, item in enumerate(items):
            if self.text(item, '%s[%s]' % (at, i)):
                result.append(item)
        if len(set(result)) != len(result):
            self.error(at, 'duplicate values')
        return result

    def enum(self, value, values, at):
        if not isinstance(value, str) or value not in values:
            self.error(at, 'must be one of ' + ', '.join(values))
            return False
        return True

    def boolean(self, value, at):
        if type(value) is not bool:
            self.error(at, 'must be boolean')
            return False
        return True

    def fields(self, data, names, at):
        for name in names:
            self.text(data.get(name), at + '.' + name)

    def items(self, value, at, minimum=0):
        result = {}
        for i, item in enumerate(self.seq(value, at, minimum)):
            loc = '%s[%s]' % (at, i)
            item = self.obj(item, loc)
            ident = item.get('id')
            if self.text(ident, loc + '.id'):
                if ident in result:
                    self.error(loc + '.id', 'duplicate ID ' + ident)
                else:
                    result[ident] = item
        return result

    def binding(self, value, at, optional=False, as_json=False):
        if optional and value is None:
            return None
        data = self.obj(value, at)
        name, digest = data.get('path'), data.get('sha256')
        ok_name = self.text(name, at + '.path')
        ok_hash = isinstance(digest, str) and HASH.fullmatch(digest)
        if not ok_hash:
            self.error(at + '.sha256', 'must be lowercase SHA-256')
        if not ok_name:
            return None
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name:
            self.error(at + '.path', 'must be a contained relative path without traversal')
            return None
        try:
            path = (self.root / relative).resolve(strict=True)
            path.relative_to(self.root)
            if not stat.S_ISREG(path.stat().st_mode):
                raise ValueError('not a regular file')
            payload = path.read_bytes()
        except (OSError, ValueError, RuntimeError) as exc:
            self.error(at + '.path', 'unavailable or unsafe: ' + str(exc))
            return None
        if ok_hash and hashlib.sha256(payload).hexdigest() != digest:
            self.error(at + '.sha256', 'does not match current file bytes')
        if as_json:
            try:
                return self.obj(_json(payload.decode('utf-8')), at + '.content')
            except (UnicodeError, ValueError, RecursionError) as exc:
                self.error(at + '.content', 'invalid JSON: ' + str(exc))
                return None
        return payload

    def linked(self, value, kind, at, task_id, final=False):
        data = self.binding(value, at, as_json=True)
        if data is None:
            return {}
        path = value.get('path')
        if path in self.active or len(self.active) >= 12:
            self.error(at, 'cyclic or excessively deep evidence join')
            return {}
        self.active.add(path)
        self.record(kind, data, at + '.content')
        self.active.remove(path)
        if data.get('task_id') != task_id:
            self.error(at, 'task_id does not match')
        if final and data.get('stage') != 'final':
            self.error(at, 'requires final evidence, not a planned record')
        return data

    def build(self, value, at, optional=False):
        if value is None and optional:
            return {}
        data = self.obj(value, at)
        self.text(data.get('id'), at + '.id')
        self.binding(data.get('source'), at + '.source')
        self.binding(data.get('fixture'), at + '.fixture')
        origin = data.get('origin')
        if self.text(origin, at + '.origin'):
            try:
                url = urlsplit(origin)
                valid = (url.scheme in ('http', 'https') and url.hostname and not url.username
                         and not url.password and not url.path and not url.query and not url.fragment)
                _ = url.port
            except ValueError:
                valid = False
            if not valid:
                self.error(at + '.origin', 'must be an HTTP(S) origin without path, query or credentials')
        return data

    def viewports(self, value, at, framing=False):
        result = self.items(value, at, 1)
        for ident, item in result.items():
            for key in ('width', 'height'):
                if type(item.get(key)) is not int or item[key] <= 0:
                    self.error(at + '.' + ident + '.' + key, 'must be a positive integer')
            if framing:
                self.text(item.get('framing'), at + '.' + ident + '.framing')
        return result

    def joined(self, value, allowed, at):
        if not isinstance(value, str) or value not in allowed:
            self.error(at, 'does not resolve to a declared ID')
            return False
        return True

    def inspection(self, value, artifact, at, optional=False):
        if value is None and optional:
            return
        data = self.obj(value, at)
        self.fields(data, ('inspector_id',), at)
        self.enum(data.get('result'), ('viewed', 'unviewable'), at + '.result')
        if data.get('result') != 'viewed':
            self.error(at, 'successful actual viewing is required for visual acceptance')
        if not isinstance(artifact, dict) or data.get('artifact_sha256') != artifact.get('sha256'):
            self.error(at, 'inspection must bind exact artifact hash')
        self.binding(data.get('receipt'), at + '.receipt')

    def record(self, kind, value, at='record'):
        data = self.obj(value, at)
        if type(data.get('schema_version')) is not int or data.get('schema_version') != 1:
            self.error(at + '.schema_version', 'must be 1')
        if data.get('kind') != kind:
            self.error(at + '.kind', 'must be ' + kind)
        self.text(data.get('task_id'), at + '.task_id')
        self.enum(data.get('stage'), ('planned', 'final'), at + '.stage')
        getattr(self, kind.replace('-', '_'))(data, at, data.get('stage') == 'final')

    def route(self, d, at, final):
        self.enum(d.get('route'), ('greenfield', 'redesign', 'reference-to-code', 'design', 'image-first',
                  'targeted-fix', 'diagnosis', 'quality-assurance', 'sites-artifact'), at + '.route')
        self.fields(d, ('objective', 'rationale'), at)
        if d.get('design_constitution') is not None:
            self.text(d['design_constitution'], at + '.design_constitution')
        if d.get('design_selection') is not None:
            selection = self.obj(d['design_selection'], at + '.design_selection')
            if selection.get('selected') != d.get('design_constitution'):
                self.error(at + '.design_selection', 'selected constitution differs from route')
            self.texts(selection.get('evidence'), at + '.design_selection.evidence', 1)
            self.text(selection.get('rationale'), at + '.design_selection.rationale')
            for i, rejected in enumerate(self.seq(selection.get('rejected'), at + '.design_selection.rejected')):
                loc = at + '.design_selection.rejected[%s]' % i
                self.fields(self.obj(rejected, loc), ('name', 'reason'), loc)
        self.enum(d.get('visual_stakes'), ('ordinary', 'high'), at + '.visual_stakes')
        self.boolean(d.get('visual_gate_required'), at + '.visual_gate_required')
        if d.get('visual_stakes') == 'high' and d.get('visual_gate_required') is not True:
            self.error(at, 'high visual stakes require the visual gate')
        self.linked(d.get('acceptance_flow'), 'flow', at + '.acceptance_flow', d.get('task_id'), final)
        if d.get('visual_gate_required') is True:
            self.linked(d.get('visual_contract'), 'visual-contract', at + '.visual_contract', d.get('task_id'), final)
        elif d.get('visual_contract') is not None:
            self.error(at + '.visual_contract', 'must be null without required gate')
        if d.get('route') == 'sites-artifact':
            self.linked(d.get('sites_record'), 'sites', at + '.sites_record', d.get('task_id'), final)
        elif d.get('sites_record') is not None:
            self.error(at + '.sites_record', 'must be null outside Sites route')

    def flow(self, d, at, final):
        self.build(d.get('build'), at + '.build', not final)
        viewports = self.viewports(d.get('viewports'), at + '.viewports')
        states = self.texts(d.get('states'), at + '.states', 1)
        flows = self.items(d.get('flows'), at + '.flows', 1)
        for ident, flow in flows.items():
            loc = at + '.flows.' + ident
            self.fields(flow, ('name', 'actor', 'goal'), loc)
            self.texts(flow.get('preconditions'), loc + '.preconditions')
            self.boolean(flow.get('critical'), loc + '.critical')
            if flow.get('critical') is True:
                recovery = flow.get('recovery_flow_id')
                if not self.joined(recovery, flows, loc + '.recovery_flow_id') or recovery == ident:
                    self.error(loc, 'critical flow needs a distinct recovery flow')
            elif flow.get('recovery_flow_id') is not None:
                self.joined(flow['recovery_flow_id'], flows, loc + '.recovery_flow_id')
            self.enum(flow.get('status'), STATUS, loc + '.status')
            steps = self.items(flow.get('steps'), loc + '.steps', 1)
            if not final and flow.get('status') != 'unrun':
                self.error(loc, 'planned flow must remain unrun')
            for step_id, step in steps.items():
                here = loc + '.steps.' + step_id
                self.fields(step, ('action', 'expected', 'evidence_plan'), here)
                self.joined(step.get('viewport_id'), viewports, here + '.viewport_id')
                self.joined(step.get('state_id'), states, here + '.state_id')
                self.enum(step.get('status'), STATUS, here + '.status')
                evidence = self.seq(step.get('evidence'), here + '.evidence')
                for i, item in enumerate(evidence):
                    self.binding(item, here + '.evidence[%s]' % i)
                if not final:
                    if step.get('status') != 'unrun' or step.get('observation') is not None or evidence:
                        self.error(here, 'planned step cannot claim observations or execution')
                elif step.get('status') in ('passed', 'failed'):
                    self.text(step.get('observation'), here + '.observation')
                    if not evidence:
                        self.error(here, 'observed step needs bound evidence')
                elif step.get('status') == 'blocked':
                    self.text(step.get('observation'), here + '.observation')
                if flow.get('status') == 'passed' and step.get('status') != 'passed':
                    self.error(here, 'passed flow contains a non-passing step')

    def visual_contract(self, d, at, final):
        self.fields(d, ('objective', 'first_glance', 'proof_slice', 'incomplete_wording'), at)
        self.texts(d.get('author_ids'), at + '.author_ids', 1)
        self.texts(d.get('builder_ids'), at + '.builder_ids', 1)
        refs = self.items(d.get('references'), at + '.references', 1)
        for ident, ref in refs.items():
            loc = at + '.references.' + ident
            self.text(ref.get('source'), loc + '.source')
            self.enum(ref.get('permission_status'), ('owned', 'licensed', 'supplied-by-user', 'public-reference'), loc + '.permission_status')
            self.binding(ref.get('artifact'), loc + '.artifact', not final)
            self.inspection(ref.get('inspection'), ref.get('artifact'), loc + '.inspection', not final)
        for key in ('traits', 'forbidden'):
            self.texts(d.get(key), at + '.' + key, 1)
        vps = self.viewports(d.get('viewports'), at + '.viewports', True)
        states = self.texts(d.get('states'), at + '.states', 1)
        views = self.items(d.get('required_views'), at + '.required_views', 1)
        seen = set()
        for ident, view in views.items():
            loc = at + '.required_views.' + ident
            vp, state = view.get('viewport_id'), view.get('state_id')
            valid = self.joined(vp, vps, loc + '.viewport_id')
            valid = self.joined(state, states, loc + '.state_id') and valid
            if valid:
                pair = (vp, state)
                if pair in seen:
                    self.error(loc, 'duplicate viewport/state view')
                seen.add(pair)
            for rid in self.texts(view.get('reference_ids'), loc + '.reference_ids', 1):
                self.joined(rid, refs, loc + '.reference_ids')
            self.boolean(view.get('proof_slice'), loc + '.proof_slice')
        if not any(v.get('proof_slice') is True for v in views.values()):
            self.error(at + '.required_views', 'at least one proof-slice view required')
        medium = self.obj(d.get('medium'), at + '.medium')
        self.fields(medium, ('selected', 'rationale', 'switch_condition'), at + '.medium')
        self.texts(medium.get('rejected'), at + '.medium.rejected', 1)
        conflicts = self.texts(d.get('constraint_conflicts'), at + '.constraint_conflicts')
        self.boolean(d.get('conflicts_resolved'), at + '.conflicts_resolved')
        if final and conflicts and d.get('conflicts_resolved') is not True:
            self.error(at, 'locked target has unresolved conflicts')
        if d.get('secondary_features_started') is not False:
            self.error(at, 'target lock must preserve secondary-feature freeze')
        if d.get('visual_gate') != 'unrun':
            self.error(at, 'contract cannot self-declare visual acceptance')

    def visual_review(self, d, at, final):
        self.enum(d.get('state'), ('visual-passed', 'final-reviewed'), at + '.state')
        for gate in ('visual_gate', 'functional_gate'):
            self.enum(d.get(gate), STATUS, at + '.' + gate)
        self.enum(d.get('decision'), ('proceed', 'complete', 'repair', 'method-switch', 'incomplete'), at + '.decision')
        if d.get('secondary_features_started_before_visual_pass') is not False:
            self.error(at, 'secondary features must not start before visual pass')
        if not final:
            for key in ('contract', 'build', 'score', 'flow', 'previous_review', 'full_build_receipt'):
                if d.get(key) is not None:
                    self.error(at + '.' + key, 'planned review must be null')
            for key in ('captures', 'inspections', 'comparisons', 'differences'):
                if self.seq(d.get(key), at + '.' + key):
                    self.error(at + '.' + key, 'planned review cannot contain observed evidence')
            reviewer = self.obj(d.get('reviewer'), at + '.reviewer')
            if reviewer.get('receipt') is not None:
                self.error(at + '.reviewer.receipt', 'planned receipt must be null')
            if d.get('decision') != 'incomplete' or any(d.get(g) != 'unrun' for g in ('visual_gate', 'functional_gate')):
                self.error(at, 'planned review cannot pass')
            self.text(d.get('incomplete_wording'), at + '.incomplete_wording')
            return
        if d.get('visual_gate') == 'unrun':
            self.error(at + '.visual_gate', 'final review must report passed, failed or blocked')
        contract = self.linked(d.get('contract'), 'visual-contract', at + '.contract', d.get('task_id'), True)
        build = self.build(d.get('build'), at + '.build')
        reviewer = self.obj(d.get('reviewer'), at + '.reviewer')
        rid = reviewer.get('id')
        self.text(rid, at + '.reviewer.id')
        authors = self.texts(contract.get('author_ids'), at + '.contract.author_ids', 1)
        builders = self.texts(contract.get('builder_ids'), at + '.contract.builder_ids', 1)
        if reviewer.get('independent') is not True or (isinstance(rid, str) and rid in authors + builders):
            self.error(at + '.reviewer', 'reviewer must be distinct from every builder and contract author')
        self.binding(reviewer.get('receipt'), at + '.reviewer.receipt')
        captures = self.items(d.get('captures'), at + '.captures', 1)
        vps = self.items(contract.get('viewports'), at + '.contract.viewports')
        states = self.texts(contract.get('states'), at + '.contract.states')
        for ident, cap in captures.items():
            loc = at + '.captures.' + ident
            self.binding(cap.get('artifact'), loc + '.artifact')
            receipt = self.binding(cap.get('receipt'), loc + '.receipt', as_json=True) or {}
            self.joined(cap.get('viewport_id'), vps, loc + '.viewport_id')
            self.joined(cap.get('state_id'), states, loc + '.state_id')
            if cap.get('build_id') != build.get('id'):
                self.error(loc, 'capture build_id differs from current build')
            vp = vps.get(cap.get('viewport_id')) if isinstance(cap.get('viewport_id'), str) else None
            source = build.get('source') if isinstance(build.get('source'), dict) else {}
            fixture = build.get('fixture') if isinstance(build.get('fixture'), dict) else {}
            artifact = cap.get('artifact') if isinstance(cap.get('artifact'), dict) else {}
            expected = {'task_id': d.get('task_id'), 'build_id': build.get('id'),
                        'source_sha256': source.get('sha256'), 'fixture_sha256': fixture.get('sha256'),
                        'origin': build.get('origin'), 'state_id': cap.get('state_id'),
                        'artifact_sha256': artifact.get('sha256')}
            expected['viewport'] = {k: vp.get(k) for k in ('id', 'width', 'height')} if vp else None
            for key, value in expected.items():
                if value is None or receipt.get(key) != value:
                    self.error(loc + '.receipt', 'mismatched ' + key)
            self.fields(receipt, ('capture_tool', 'captured_at'), loc + '.receipt')
        inspections = self.seq(d.get('inspections'), at + '.inspections', 1)
        inspected = set()
        for i, ins in enumerate(inspections):
            loc = at + '.inspections[%s]' % i
            ins = self.obj(ins, loc)
            digest = ins.get('artifact_sha256')
            matches = [c for c in captures.values() if isinstance(c.get('artifact'), dict) and c['artifact'].get('sha256') == digest]
            self.inspection(ins, matches[0].get('artifact') if matches else None, loc)
            if isinstance(digest, str):
                if digest in inspected:
                    self.error(loc, 'duplicate inspection hash')
                inspected.add(digest)
        views = self.items(contract.get('required_views'), at + '.contract.required_views')
        required = {i: v for i, v in views.items() if d.get('state') == 'final-reviewed' or v.get('proof_slice') is True}
        comparisons = self.seq(d.get('comparisons'), at + '.comparisons', 1)
        found = set()
        used_captures = set()
        for i, comparison in enumerate(comparisons):
            loc = at + '.comparisons[%s]' % i
            comparison = self.obj(comparison, loc)
            vid, cid = comparison.get('view_id'), comparison.get('capture_id')
            good_view = self.joined(vid, required, loc + '.view_id')
            good_cap = self.joined(cid, captures, loc + '.capture_id')
            self.text(comparison.get('observation'), loc + '.observation')
            refs = self.texts(comparison.get('reference_ids'), loc + '.reference_ids', 1)
            if good_view:
                if vid in found:
                    self.error(loc, 'duplicate comparison view')
                found.add(vid)
                if refs != required[vid].get('reference_ids'):
                    self.error(loc, 'reference IDs differ from accepted view')
            if good_cap:
                used_captures.add(cid)
                cap = captures[cid]
                if good_view and any(cap.get(k) != required[vid].get(k) for k in ('viewport_id', 'state_id')):
                    self.error(loc, 'capture viewport/state does not match accepted view')
                artifact = cap.get('artifact') if isinstance(cap.get('artifact'), dict) else {}
                if not isinstance(artifact.get('sha256'), str) or artifact.get('sha256') not in inspected:
                    self.error(loc, 'render has no successful inspection record')
        if found != set(required):
            self.error(at + '.comparisons', 'missing required viewport/state coverage')
        if used_captures != set(captures):
            self.error(at + '.captures', 'captures must resolve to required comparisons')
        blocking = False
        for i, diff in enumerate(self.seq(d.get('differences'), at + '.differences')):
            loc = at + '.differences[%s]' % i
            diff = self.obj(diff, loc)
            self.joined(diff.get('view_id'), required, loc + '.view_id')
            self.enum(diff.get('severity'), ('P0', 'P1', 'P2', 'P3'), loc + '.severity')
            self.text(diff.get('description'), loc + '.description')
            if diff.get('contract_trait') is not None:
                self.joined(diff.get('contract_trait'), contract.get('traits') if isinstance(contract.get('traits'), list) else [], loc + '.contract_trait')
            if diff.get('severity') in ('P0', 'P1', 'P2'):
                blocking = True
        score = d.get('score')
        score_ok = type(score) in (int, float) and 0 <= score <= 10 and math.isfinite(score)
        if not score_ok:
            self.error(at + '.score', 'must be a finite number from 0 to 10')
        passed = d.get('visual_gate') == 'passed'
        if passed and (not score_ok or score < 7 or blocking):
            self.error(at, 'visual pass requires score >=7 and no P0-P2 gaps')
        if not passed:
            if d.get('decision') not in ('repair', 'method-switch', 'incomplete'):
                self.error(at, 'non-passing visual gate cannot proceed or complete')
            self.text(d.get('incomplete_wording'), at + '.incomplete_wording')
        if d.get('state') == 'final-reviewed':
            prior = self.linked(d.get('previous_review'), 'visual-review', at + '.previous_review', d.get('task_id'), True)
            if prior.get('state') != 'visual-passed' or prior.get('visual_gate') != 'passed' or prior.get('decision') != 'proceed':
                self.error(at, 'final review requires actual accepted proof-slice review')
            if prior.get('contract') != d.get('contract'):
                self.error(at, 'previous review uses a different visual contract')
            full = self.binding(d.get('full_build_receipt'), at + '.full_build_receipt', as_json=True) or {}
            source = build.get('source') if isinstance(build.get('source'), dict) else {}
            fixture = build.get('fixture') if isinstance(build.get('fixture'), dict) else {}
            previous = d.get('previous_review') if isinstance(d.get('previous_review'), dict) else {}
            for key, value in {'stage': 'full-build', 'task_id': d.get('task_id'), 'build_id': build.get('id'),
                               'source_sha256': source.get('sha256'), 'fixture_sha256': fixture.get('sha256'),
                               'prior_review_sha256': previous.get('sha256')}.items():
                if value is None or full.get(key) != value:
                    self.error(at + '.full_build_receipt', 'mismatched ' + key)
        elif d.get('previous_review') is not None or d.get('full_build_receipt') is not None:
            self.error(at, 'initial visual pass must not claim a later stage receipt')
        flow = {}
        if d.get('flow') is not None:
            flow = self.linked(d['flow'], 'flow', at + '.flow', d.get('task_id'), True)
            if flow.get('build') != build:
                self.error(at + '.flow', 'flow build differs from reviewed build')
        if d.get('decision') == 'complete':
            if d.get('state') != 'final-reviewed' or not passed or d.get('functional_gate') != 'passed':
                self.error(at, 'complete requires final-reviewed with both gates passed')
            if not flow or any(f.get('status') != 'passed' for f in self.items(flow.get('flows'), at + '.flow.flows', 1).values()):
                self.error(at, 'complete requires a bound final flow with every outcome passed')

    def sites(self, d, at, final):
        brief = self.obj(d.get('brief'), at + '.brief')
        self.fields(brief, ('title', 'audience', 'use_moment', 'outcome'), at + '.brief')
        self.enum(brief.get('job'), ('teaching-reference', 'portfolio', 'interactive-report', 'review-workspace',
                  'project-board', 'dashboard', 'planner', 'tracker', 'action-tracker', 'calculator',
                  'scenario-planner', 'gallery', 'registry', 'catalog', 'portal', 'hub', 'knowledge-system',
                  'operational-playbook', 'prototype', 'simulation', 'game', 'workflow-app', 'lightweight-tool'), at + '.brief.job')
        content = self.obj(brief.get('content'), at + '.brief.content')
        self.texts(content.get('spine'), at + '.brief.content.spine', 1)
        self.texts(content.get('required_provenance'), at + '.brief.content.required_provenance')
        delivery = self.obj(brief.get('delivery'), at + '.brief.delivery')
        self.enum(delivery.get('mode'), ('local', 'preview', 'private', 'public'), at + '.brief.delivery.mode')
        self.boolean(delivery.get('deployment_requested'), at + '.brief.delivery.deployment_requested')
        audiences = ('private', 'workspace', 'selected-users', 'public')
        self.enum(delivery.get('audience'), audiences, at + '.brief.delivery.audience')
        self.boolean(delivery.get('anonymous_test_required'), at + '.brief.delivery.anonymous_test_required')
        public = delivery.get('audience') == 'public' or delivery.get('mode') == 'public'
        if public and delivery.get('anonymous_test_required') is not True:
            self.error(at + '.brief.delivery', 'public delivery requires anonymous testing')
        sources = self.obj(d.get('sources'), at + '.sources')
        self.boolean(sources.get('inspection_complete'), at + '.sources.inspection_complete')
        items = self.items(sources.get('items'), at + '.sources.items', 1)
        for sid, source in items.items():
            loc = at + '.sources.items.' + sid
            self.fields(source, ('locator', 'intended_role'), loc)
            for key, choices in {
                'source_type': ('explicit-reference', 'midjourney', 'google-flow', 'flora', 'local-file', 'public-research', 'generated'),
                'access_class': ('public', 'signed-in', 'private', 'local'),
                'ownership': ('user-owned', 'licensed', 'public-domain', 'third-party', 'unresolved'),
                'prompt_status': ('exact', 'workflow', 'private', 'unavailable', 'not-applicable'),
                'public_eligibility': ('allowed', 'private-only', 'unresolved')}.items():
                self.enum(source.get(key), choices, loc + '.' + key)
            self.boolean(source.get('inspected'), loc + '.inspected')
            self.binding(source.get('evidence'), loc + '.evidence', not (final and source.get('inspected') is True))
            if source.get('prompt') is not None:
                prompt = self.obj(source['prompt'], loc + '.prompt')
                self.text(prompt.get('text'), loc + '.prompt.text')
                self.obj(prompt.get('parameters'), loc + '.prompt.parameters')
                self.binding(prompt.get('evidence'), loc + '.prompt.evidence', not final)
            elif final and source.get('prompt_status') == 'exact':
                self.error(loc + '.prompt', 'exact prompt needs original text, parameters and evidence')
            projection = source.get('public_projection')
            if projection is not None:
                projection = self.obj(projection, loc + '.public_projection')
                if set(projection) - {'name', 'url', 'attribution', 'identifier', 'prompt'}:
                    self.error(loc + '.public_projection', 'unknown export fields')
                self.text(projection.get('name'), loc + '.public_projection.name')
        content_ids = self.texts(content.get('source_ids'), at + '.brief.content.source_ids', 1)
        for sid in content_ids:
            self.joined(sid, items, at + '.brief.content.source_ids')
        curation = self.obj(d.get('curation'), at + '.curation')
        selected = set()
        decisions = set()
        for i, decision in enumerate(self.seq(curation.get('decisions'), at + '.curation.decisions', 1)):
            loc = at + '.curation.decisions[%s]' % i
            decision = self.obj(decision, loc)
            sid = decision.get('source_id')
            if self.joined(sid, items, loc + '.source_id'):
                if sid in decisions:
                    self.error(loc, 'duplicate source curation decision')
                decisions.add(sid)
                if decision.get('decision') == 'selected':
                    selected.add(sid)
            self.enum(decision.get('decision'), ('selected', 'rejected', 'retired', 'hold'), loc + '.decision')
            self.fields(decision, ('reason', 'intended_role'), loc)
            self.texts(decision.get('useful_qualities'), loc + '.useful_qualities')
        authority = self.obj(d.get('authority'), at + '.authority')
        if final or authority.get('selected_direction') is not None:
            self.text(authority.get('selected_direction'), at + '.authority.selected_direction')
        if authority.get('design_constitution') is not None:
            self.text(authority['design_constitution'], at + '.authority.design_constitution')
        authority_ids = self.texts(authority.get('source_refs'), at + '.authority.source_refs', int(final))
        for sid in authority_ids:
            self.joined(sid, items, at + '.authority.source_refs')
            if final and sid not in selected:
                self.error(at + '.authority.source_refs', 'authority source must be selected')
        rules = self.obj(authority.get('rules'), at + '.authority.rules')
        for key in ('layout', 'color', 'typography', 'imagery', 'material', 'motion', 'signature_tension'):
            self.texts(rules.get(key), at + '.authority.rules.' + key, int(final))
        self.texts(authority.get('avoid'), at + '.authority.avoid', int(final))
        self.texts(authority.get('rejected_directions'), at + '.authority.rejected_directions')
        profile = self.obj(d.get('profile'), at + '.profile')
        profiles = self.texts(profile.get('required'), at + '.profile.required')
        if brief.get('job') == 'teaching-reference' and 'teaching-library' not in profiles:
            self.error(at + '.profile.required', 'teaching-reference requires teaching-library')
        if public and any(item.get('access_class') != 'public' for item in items.values()) and 'public-source-privacy' not in profiles:
            self.error(at + '.profile.required', 'public delivery with nonpublic research requires public-source-privacy')
        requirements = {
            'teaching-library': ('first-time-reader-explanation', 'practical-examples', 'copyable-material', 'search', 'working-controls', 'mobile'),
            'public-source-privacy': ('public-source-whitelist', 'private-source-redaction', 'export-scan', 'anonymous-route-test', 'source-release-parity')}
        for name in profiles:
            self.joined(name, requirements, at + '.profile.required')
        checked = set()
        for i, check in enumerate(self.seq(profile.get('checks'), at + '.profile.checks')):
            loc = at + '.profile.checks[%s]' % i
            check = self.obj(check, loc)
            name, cid = check.get('profile'), check.get('id')
            known = self.joined(name, profiles, loc + '.profile')
            valid_id = self.text(cid, loc + '.id')
            if known and valid_id:
                pair = (name, cid)
                if pair in checked:
                    self.error(loc, 'duplicate profile check')
                checked.add(pair)
                self.joined(cid, requirements.get(name, ()), loc + '.id')
            self.enum(check.get('status'), STATUS, loc + '.status')
            self.binding(check.get('evidence'), loc + '.evidence', not final)
            if final and check.get('status') != 'passed':
                self.error(loc, 'final profile check must pass')
            if not final and check.get('status') != 'unrun':
                self.error(loc, 'planned profile cannot claim a pass')
        for name in profiles:
            for cid in requirements.get(name, ()):
                if (name, cid) not in checked:
                    self.error(at + '.profile', 'missing required check ' + name + '/' + cid)
        release = self.obj(d.get('release'), at + '.release')
        self.binding(release.get('source'), at + '.release.source', not final)
        build = self.obj(release.get('build'), at + '.release.build')
        self.enum(build.get('status'), STATUS, at + '.release.build.status')
        self.binding(build.get('evidence'), at + '.release.build.evidence', not final)
        review = self.obj(release.get('review'), at + '.release.review')
        self.enum(review.get('status'), STATUS, at + '.release.review.status')
        self.binding(review.get('evidence'), at + '.release.review.evidence', not final)
        builder_ids = self.texts(review.get('builder_ids'), at + '.release.review.builder_ids', int(final))
        sites = self.obj(release.get('sites'), at + '.release.sites')
        self.enum(sites.get('deployment_status'), ('not-requested', 'unrun', 'pending', 'succeeded', 'failed'), at + '.release.sites.deployment_status')
        health = self.obj(release.get('health'), at + '.release.health')
        self.enum(health.get('status'), ('not-required', 'unrun', 'passed', 'failed'), at + '.release.health.status')
        access = self.obj(release.get('access'), at + '.release.access')
        self.enum(access.get('audience'), audiences, at + '.release.access.audience')
        self.boolean(access.get('anonymous_test_required'), at + '.release.access.anonymous_test_required')
        self.enum(access.get('anonymous_test_status'), ('not-required', 'unrun', 'passed', 'failed'), at + '.release.access.anonymous_test_status')
        if any(access.get(k) != delivery.get(k) for k in ('audience', 'anonymous_test_required')):
            self.error(at + '.release.access', 'does not match requested delivery access')
        public_ids = self.texts(release.get('public_source_ids'), at + '.release.public_source_ids')
        for sid in public_ids:
            if self.joined(sid, items, at + '.release.public_source_ids'):
                source = items[sid]
                if sid not in selected or source.get('inspected') is not True or source.get('public_eligibility') != 'allowed' or not isinstance(source.get('public_projection'), dict):
                    self.error(at + '.release.public_source_ids', 'source must be selected, inspected, allowed and explicitly projected')
        self.texts(release.get('unresolved_non_blocking'), at + '.release.unresolved_non_blocking')
        if not final:
            for value, loc in ((build.get('status'), '.build.status'), (review.get('status'), '.review.status')):
                if value != 'unrun':
                    self.error(at + '.release' + loc, 'planned record cannot claim execution')
            if sites.get('deployment_status') not in ('unrun', 'not-requested') or health.get('status') not in ('unrun', 'not-required') or access.get('anonymous_test_status') not in ('unrun', 'not-required'):
                self.error(at + '.release', 'planned record cannot claim deployment/health/access success')
            if release.get('flow') is not None:
                self.linked(release['flow'], 'flow', at + '.release.flow', d.get('task_id'))
            return
        if sources.get('inspection_complete') is not True:
            self.error(at + '.sources', 'final source inspection must be complete')
        if not any(s.get('source_type') == 'midjourney' and s.get('inspected') is True for s in items.values()):
            self.text(sources.get('midjourney_waiver_reason'), at + '.sources.midjourney_waiver_reason')
        for sid in set(content_ids + authority_ids):
            if sid in items and (sid not in selected or items[sid].get('inspected') is not True):
                self.error(at + '.sources.' + sid, 'final used source must be selected and inspected')
        self.fields(build, ('id', 'command'), at + '.release.build')
        if build.get('status') != 'passed' or review.get('status') != 'passed':
            self.error(at + '.release', 'final build and review must pass')
        self.text(review.get('evaluator'), at + '.release.review.evaluator')
        if isinstance(review.get('evaluator'), str) and review['evaluator'] in builder_ids:
            self.error(at + '.release.review', 'evaluator must differ from builders')
        flow = self.linked(release.get('flow'), 'flow', at + '.release.flow', d.get('task_id'), True)
        flow_build = flow.get('build') if isinstance(flow.get('build'), dict) else {}
        if flow_build.get('id') != build.get('id') or flow_build.get('source') != release.get('source'):
            self.error(at + '.release.flow', 'source/build does not match released build')
        if any(f.get('status') != 'passed' for f in self.items(flow.get('flows'), at + '.release.flow.flows', 1).values()):
            self.error(at + '.release.flow', 'all final release flows must pass')
        deployed = delivery.get('deployment_requested') is True
        source = release.get('source') if isinstance(release.get('source'), dict) else {}
        identity = {'task_id': d.get('task_id'), 'build_id': build.get('id'), 'source_sha256': source.get('sha256')}
        if deployed:
            self.fields(sites, ('version', 'deployed_url'), at + '.release.sites')
            url_value = sites.get('deployed_url')
            try:
                url = urlsplit(url_value) if isinstance(url_value, str) else None
                good_url = url and url.scheme in ('http', 'https') and url.hostname and not url.username and not url.password
            except ValueError:
                good_url = False
            if not good_url:
                self.error(at + '.release.sites.deployed_url', 'must be an HTTP(S) URL without credentials')
            deployed_identity = dict(identity, version=sites.get('version'), deployed_url=sites.get('deployed_url'))
            for value, label, status in ((sites.get('receipt'), 'sites.receipt', 'succeeded'),
                                         (health.get('evidence'), 'health.evidence', 'passed')):
                loc = at + '.release.' + label
                receipt = self.binding(value, loc, as_json=True) or {}
                for key, expected in dict(deployed_identity, status=status).items():
                    if expected is None or receipt.get(key) != expected:
                        self.error(loc, 'mismatched ' + key)
            if sites.get('deployment_status') != 'succeeded' or health.get('status') != 'passed':
                self.error(at + '.release', 'deployment success and observed live health both required')
        else:
            if sites.get('deployment_status') != 'not-requested' or health.get('status') != 'not-required':
                self.error(at + '.release', 'unrequested deployment and live health must remain not-requested/not-required')
            if sites.get('receipt') is not None or health.get('evidence') is not None:
                self.error(at + '.release', 'local release cannot claim deployment/health receipts')
        anonymous = delivery.get('anonymous_test_required') is True
        if anonymous:
            receipt = self.binding(access.get('evidence'), at + '.release.access.evidence', as_json=True) or {}
            expected_access = dict(identity, status='passed', audience=access.get('audience'))
            if deployed:
                expected_access.update(version=sites.get('version'), deployed_url=sites.get('deployed_url'))
            for key, expected in expected_access.items():
                if expected is None or receipt.get(key) != expected:
                    self.error(at + '.release.access.evidence', 'mismatched ' + key)
            if access.get('anonymous_test_status') != 'passed':
                self.error(at + '.release.access', 'required anonymous access test must pass')
        elif access.get('anonymous_test_status') != 'not-required' or access.get('evidence') is not None:
            self.error(at + '.release.access', 'unrequired anonymous test must remain not-required')
        self.binding(release.get('privacy_scan'), at + '.release.privacy_scan', not public)
        if public and (not public_ids or not set(content_ids).issubset(set(public_ids))):
            self.error(at + '.release.public_source_ids', 'public content needs an explicit complete allowlist')
        doc = self.obj(release.get('documentation'), at + '.release.documentation')
        self.fields(doc, ('what_worked', 'what_failed', 'what_caused_the_fix', 'next_time'), at + '.release.documentation')


def validate(kind, data, root):
    """Return shape/binding errors. Does not establish evidence truth or quality."""
    check = Check(root)
    if not check.root.is_dir():
        return ['root: evidence root must be an existing directory']
    if not isinstance(kind, str) or kind not in KINDS:
        return ['kind: unsupported record kind']
    check.record(kind, data)
    return check.errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=KINDS)
    parser.add_argument('record', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args(argv)
    digest = None
    code = 1
    try:
        if not stat.S_ISREG(args.record.stat().st_mode):
            raise ValueError('record is not a regular file')
        payload = args.record.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        data = _json(payload.decode('utf-8'))
        errors = validate(args.kind, data, args.root)
        code = 1 if errors else 0
    except (OSError, UnicodeError, ValueError, RuntimeError, RecursionError) as exc:
        errors = ['input: ' + str(exc)]
        code = 2
    print(json.dumps({'valid': not errors, 'kind': args.kind, 'errors': errors,
                      'record_sha256': digest, 'scope': 'shape-and-binding-only'}, indent=2))
    return code


if __name__ == '__main__':
    sys.exit(main())
