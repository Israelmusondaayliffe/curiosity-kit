#!/usr/bin/env python3
"""Local deterministic film prompt compiler. Python 3.9+, standard library only."""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

BLOCKS = ['scene_context', 'references', 'location_map', 'first_frame', 'format', 'optics', 'camera', 'action', 'physics', 'lighting', 'audio', 'acting', 'style', 'quality', 'constraints', 'technical']
BAN = 'Use location references for geography only. Do not inherit composition, camera angle, or colour.'
AUDIO = 'Generate dialogue and diegetic SFX only. Music belongs in post. Only the quoted lines below are spoken.'
ROLES = {'character': 'identity', 'prop': 'prop-state', 'location': 'geography'}
ROLE_WORDS = {'character': 'character identity', 'prop': 'prop state', 'location': 'location space'}

class Invalid(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise Invalid(message)

def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def text(value, name):
    require(isinstance(value, str) and value.strip(), name + ' must be nonempty text')
    require('\n[' not in value and '\r' not in value, name + ' contains a reserved block heading')
    return value

def number(value, name):
    require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), name + ' must be finite')
    return value

def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', value), 'unsafe identifier: ' + str(value))
    return value

def positive(value, name):
    text(value, name)
    require(not re.search(r'\b(no|not|never|without|don.t|cannot)\b', value, re.I), name + ' must describe a positive action')
    return value

def load_targets(path):
    profiles = [{'id': 'generic', 'label': 'Generic film prompt', 'captured': 'undated', 'source': 'Project formula', 'format_prefix': '', 'technical_suffix': ''}]
    if path:
        profiles += read_json(path)['profiles']
    result = {}
    for p in profiles:
        require(isinstance(p['id'], str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', p['id']) and '..' not in p['id'], 'unsafe target identifier: ' + str(p['id']))
        for k in ['label', 'captured', 'source']:
            text(p[k], 'target ' + k)
        for k in ['format_prefix', 'technical_suffix']:
            require(isinstance(p.get(k, ''), str), 'target ' + k + ' must be text')
        require(p['id'] not in result or p['id'] == 'generic', 'duplicate target')
        result[p['id']] = p
    return result

def compile_project(project, targets):
    """Validate source meaning before rendering canonical, human-readable film work."""
    text(project['title'], 'title'); text(project['brief'], 'brief')
    formula = project['formula']
    layout = formula.get('layout')
    if layout is not None:
        require(isinstance(layout, list) and layout, 'formula layout must be a nonempty list')
        headings = []
        for group in layout:
            heading = text(group['heading'], 'formula heading')
            require('\n' not in heading and heading not in headings, 'formula headings must be unique single lines')
            require(isinstance(group['blocks'], list) and group['blocks'], 'each layout group needs semantic blocks')
            headings.append(heading)
        order = [name for group in layout for name in group['blocks']]
    else:
        order = formula['blocks']
        layout = [{'heading': '[' + name + ']', 'blocks': [name]} for name in order]
    require(len(order) == len(BLOCKS) and set(order) == set(BLOCKS), 'formula must declare each supported block exactly once')
    require(order[-1] == 'technical', 'technical closing tags must be last')
    require(formula['descriptor_policy'] == 'verbatim', 'only the declared verbatim descriptor policy is supported')
    style = text(formula['style_constant'], 'style constant')
    assets = {}
    tags = set()
    for a in project['assets']:
        identifier(a['id']); require(a['id'] not in assets, 'duplicate asset')
        require(a['kind'] in ROLES, 'unknown asset kind')
        for k in ['identity', 'state', 'descriptor']:
            text(a[k], 'asset ' + k)
        require(isinstance(a['version'], int) and a['version'] > 0, 'asset version must be positive integer')
        require(re.fullmatch(r'@[A-Za-z0-9_-]+', a['tag']) is not None and a['tag'] not in tags, 'invalid or duplicate asset tag')
        tags.add(a['tag']); assets[a['id']] = a
        if a['kind'] == 'character':
            text(a['voice'], 'voice'); text(a['behavior'], 'behavior')
    for a in assets.values():
        if a['parent'] is not None:
            require(a['parent'] in assets and a['parent'] != a['id'], 'missing or self parent')
            require(assets[a['parent']]['identity'] == a['identity'], 'state parent has different identity')
            seen = {a['id']}; parent = a['parent']
            while parent is not None:
                require(parent not in seen, 'cyclic asset parent'); seen.add(parent)
                parent = assets[parent]['parent']
    outputs = {}; dependencies = {}; scene_ids = set(); current = {}
    for scene in project['scenes']:
        sid = identifier(scene['id']); require(sid not in scene_ids, 'duplicate scene'); scene_ids.add(sid)
        loc = assets[scene['location']]; require(loc['kind'] == 'location', 'scene location must be a location asset')
        geo = scene['geography']
        for k in ['text', 'camera_side', 'reverse_rule']:
            text(geo[k], 'geography ' + k)
        require(geo['landmarks'] and len(set(geo['landmarks'])) == len(geo['landmarks']), 'landmarks must be unique and nonempty')
        for landmark in geo['landmarks']:
            require(landmark in geo['text'], 'landmark missing from locked geography')
        prose = text(scene['prose'], 'scene prose')
        dependencies['scenes/' + sid + '.md'] = digest(json.dumps([scene['title'], scene['dramatic_question'], prose], sort_keys=True))
        outputs['scenes/' + sid + '.md'] = '# ' + text(scene['title'], 'scene title') + '\n\n' + text(scene['dramatic_question'], 'dramatic question') + '\n\n' + prose + '\n'
        rows = ['# ' + scene['title'] + ': shotlist', '', 'Geography lock: ' + geo['text'], 'Camera side: ' + geo['camera_side'], 'Reverse rule: ' + geo['reverse_rule'], '']
        shot_ids = set()
        require(scene['shots'], 'scene needs shots')
        for shot in scene['shots']:
            qid = identifier(shot['id']); require(qid not in shot_ids, 'duplicate shot'); shot_ids.add(qid)
            duration = number(shot['duration'], 'duration'); require(duration > 0, 'duration must be positive')
            active = []; identities = set()
            for ref in shot['active']:
                a = assets[ref['asset']]
                require(ref['version'] == a['version'], 'stale asset version: ' + a['id'])
                require(ref['role'] == ROLES[a['kind']], 'incorrect reference role: ' + a['id'])
                require(a['identity'] not in identities, 'duplicate identity in shot')
                identities.add(a['identity']); active.append(a)
                if a['identity'] in current and current[a['identity']] != a['id']:
                    require(shot.get('state_changes', {}).get(a['identity']) == a['id'], 'stale or undeclared state change: ' + a['identity'])
                current[a['identity']] = a['id']
            active_ids = {a['id'] for a in active}
            require(scene['location'] in active_ids, 'location reference must be active')
            for identity, aid in shot.get('state_changes', {}).items():
                require(aid in active_ids and assets[aid]['identity'] == identity, 'state change must name active identity')
            chars = [a for a in active if a['kind'] == 'character']
            occupants = [a for a in active if a['kind'] != 'location']
            ff = shot['first_frame']
            require(len(ff) == len(occupants) and {f['asset'] for f in ff} == {a['id'] for a in occupants}, 'first frame must locate every active character and prop exactly once')
            positions = []
            for f in ff:
                require(f['landmark'] in geo['landmarks'], 'blocking uses unknown landmark')
                require(f['frame_side'] in ['left', 'right'], 'blocking uses frame-left or frame-right')
                require(number(f['distance_m'], 'distance') >= 0, 'distance must be nonnegative')
                positions.append('{}: frame-{}, {} m from {}; gaze {}.'.format(assets[f['asset']]['tag'], f['frame_side'], f['distance_m'], f['landmark'], text(f['gaze'], 'gaze')))
            beats = []; end = 0
            require(shot['beats'], 'shot needs timed beats')
            for beat in shot['beats']:
                start = number(beat['start'], 'beat start'); stop = number(beat['end'], 'beat end')
                require(start == end and stop > start and stop <= duration, 'timing must be contiguous, increasing, and within shot duration')
                action = positive(beat['action'], 'beat action')
                require(len(re.findall(r'[.!?](?:\s|$)', action)) <= 3, 'overloaded beat: more than three sentences')
                require('"' not in action and '“' not in action, 'dialogue belongs only in audio')
                beats.append('{}–{} s: {}'.format(start, stop, action)); end = stop
            require(end == duration, 'timed beats must cover duration')
            light = shot['light']; require(set(light) == {'source', 'motivation'}, 'lighting must declare exactly one source and its motivation')
            source = text(light['source'], 'light source')
            require(not re.search(r'\b(and|plus|second|another|two)\b|[;+]', source, re.I), 'lighting contains a second or compound source')
            audio = [AUDIO]; speakers = set()
            for d in shot['dialogue']:
                require(d['speaker'] in {a['id'] for a in chars}, 'speaker must be an active character')
                a = assets[d['speaker']]; speakers.add(a['id'])
                line = text(d['line'], 'dialogue line'); require('"' not in line and '\n' not in line, 'dialogue line cannot contain quotes or newline')
                require(all(line not in b['action'] for b in shot['beats']), 'dialogue duplicated in action')
                audio.append('{} voice: {}\n"{}"\nAction: {}\nReaction: {}\nAll other characters remain silent during this line.'.format(a['tag'], a['voice'], line, positive(d['action'], 'dialogue action'), positive(d['reaction'], 'dialogue reaction')))
            silent = [a['tag'] for a in chars if a['id'] not in speakers]
            audio.append('Silent throughout: ' + (', '.join(silent) if silent else 'all characters except during their own quoted lines') + '.')
            audio.append('SFX: ' + text(shot.get('sfx', 'Room tone and sounds caused by visible actions.'), 'SFX'))
            if 'silence_rule' in formula:
                audio.append(text(formula['silence_rule'], 'formula silence rule'))
            require(set(shot['acting']) == {a['id'] for a in chars}, 'acting must cover exactly the active cast')
            refs = ['{} | {}\n{}'.format(a['tag'], ROLE_WORDS[a['kind']], a['descriptor']) for a in active]
            refs.extend(text(a.get('inheritance_clause', BAN), 'location inheritance clause') for a in active if a['kind'] == 'location')
            blocks = {
                'scene_context': '{} characters: {}; no duplicates.\nScene: {}\nPurpose: {}'.format(len(chars), ', '.join(a['tag'] for a in chars), scene['title'], text(shot['purpose'], 'shot purpose')),
                'references': '\n'.join(refs),
                'location_map': geo['text'] + '\nCamera side: ' + geo['camera_side'] + '\nReverse rule: ' + geo['reverse_rule'],
                'first_frame': '\n'.join(positions),
                'format': text(shot['format'], 'format'), 'optics': text(shot['optics'], 'optics'),
                'camera': text(shot['camera'], 'camera'), 'action': '\n'.join(beats),
                'physics': text(shot['physics'], 'physics'),
                'lighting': 'One source: ' + source + '\nMotivation: ' + text(light['motivation'], 'light motivation'),
                'audio': '\n'.join(audio),
                'acting': '\n'.join(assets[k]['tag'] + ': ' + positive(v, 'acting') for k, v in shot['acting'].items()),
                'style': style, 'quality': text(shot['quality'], 'quality'),
                'constraints': '\n'.join(positive(c, 'constraint') for c in shot['constraints']),
                'technical': text(shot['technical'], 'technical')}
            require(shot['constraints'], 'positive constraints required')
            rows.append('- {} ({} s): {} | {} | {}'.format(qid, duration, shot['purpose'], shot['camera'], '; '.join(positions)))
            for target in targets:
                rendered = dict(blocks)
                template = target.get('reference_token_template', '{tag}')
                require(template in ['{tag}', '@Image {index}'], 'unsupported data-only reference token template')
                bindings = []
                for index, a in enumerate(active, 1):
                    if template != '{tag}':
                        bindings.append(template.format(tag=a['tag'], index=index) + ' = ' + a['tag'])
                rendered['references'] = '\n'.join(bindings + [blocks['references']])
                rendered['format'] = '\n'.join(x for x in [target.get('format_prefix', ''), blocks['format']] if x)
                output_path = 'prompts/{}/{}--{}.txt'.format(target['id'], sid, qid)
                require(output_path not in outputs, 'duplicate output path: ' + output_path)
                dependencies[output_path] = digest(json.dumps([formula, active, geo, scene['title'], shot, target], sort_keys=True))
                outputs[output_path] = '\n\n'.join(group['heading'] + '\n' + '\n'.join(rendered[name] for name in group['blocks']) for group in layout) + '\n'
        outputs['shotlists/' + sid + '.md'] = '\n'.join(rows) + '\n'
        dependencies['shotlists/' + sid + '.md'] = digest(outputs['shotlists/' + sid + '.md'])
    require(outputs, 'project needs scenes')
    return outputs, dependencies

def safe_path(root, relative):
    path = root / relative
    require(not path.is_symlink(), 'symlink output refused: ' + relative)
    require(root == path.resolve().parent or root in path.resolve().parents, 'output escapes project')
    for parent in path.parents:
        if parent == root:
            break
        require(not parent.is_symlink(), 'symlink directory refused')
    return path

def run(args):
    project = read_json(args.project)
    profiles = load_targets(args.targets)
    names = args.target or ['generic']
    require(len(names) == len(set(names)), 'duplicate requested target')
    require(all(n in profiles for n in names), 'unknown target')
    expected, dependencies = compile_project(project, [profiles[n] for n in names])
    root = Path(args.out).absolute()
    require(not root.is_symlink(), 'symlink output root refused')
    root = root.resolve()
    manifest_path = safe_path(root, '.film-manifest.json')
    old = read_json(manifest_path) if manifest_path.exists() else {'files': {}}
    require(not manifest_path.exists() or old.get('tool') == 'film.py', 'foreign manifest')
    files = old['files']; states = {}; conflicts = []
    for rel, content in expected.items():
        path = safe_path(root, rel); want = digest(content)
        actual = digest(path.read_text(encoding='utf-8')) if path.exists() else None
        prior = files.get(rel)
        if actual == want:
            state = 'stale-source' if prior and prior.get('dependency_sha256') != dependencies[rel] else 'current'
        elif actual is None:
            state = 'missing'
        elif prior and actual == prior['sha256']:
            state = 'stale-source'
        elif prior:
            state = 'modified-output'; conflicts.append(rel)
        else:
            state = 'unowned-conflict'; conflicts.append(rel)
        states[rel] = state
    obsolete = sorted(set(files) - set(expected))
    source_hash = digest(json.dumps(project, sort_keys=True, ensure_ascii=False))
    report = {'command': args.command, 'files': states, 'obsolete': obsolete, 'source_changed': old.get('source_sha256') != source_hash}
    if args.command == 'compile':
        blocked = [r for r in conflicts if states[r] == 'unowned-conflict' or not args.repair]
        require(not blocked, 'refusing overwrite: ' + ', '.join(blocked) + '; --repair can replace only manifest-owned modified outputs')
        root.mkdir(parents=True, exist_ok=True)
        for rel, content in expected.items():
            if states[rel] != 'current':
                path = safe_path(root, rel); path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
        new = {'tool': 'film.py', 'version': 1, 'source_sha256': source_hash, 'targets': names, 'target_profiles': [profiles[n] for n in names], 'asset_bindings': [{k: a[k] for k in ['id', 'tag', 'identity', 'state', 'parent', 'version']} for a in project['assets']], 'files': {r: {'sha256': digest(c), 'dependency_sha256': dependencies[r]} for r, c in expected.items()}}
        # Removed outputs remain on disk and in ownership history until the user handles them.
        for rel in obsolete:
            new['files'][rel] = files[rel]
        body = json.dumps(new, indent=2, ensure_ascii=False) + '\n'
        if not manifest_path.exists() or manifest_path.read_text(encoding='utf-8') != body:
            manifest_path.write_text(body, encoding='utf-8')
        report['result'] = 'compiled'; report['written'] = [r for r, s in states.items() if s != 'current']
    else:
        report['result'] = 'pass' if all(s == 'current' for s in states.values()) and not obsolete else 'needs-work'
    print(json.dumps(report, indent=2))
    return 0 if args.command == 'compile' or report['result'] == 'pass' else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['compile', 'check', 'status'])
    parser.add_argument('--project', required=True); parser.add_argument('--out', required=True)
    parser.add_argument('--target', action='append'); parser.add_argument('--targets')
    parser.add_argument('--repair', action='store_true', help='Replace edited manifest-owned outputs after host/user-authorized repair; never grants authority itself')
    args = parser.parse_args()
    try:
        return run(args)
    except (Invalid, KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({'result': 'error', 'message': str(exc)}), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
