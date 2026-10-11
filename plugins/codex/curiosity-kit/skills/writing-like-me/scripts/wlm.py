#!/usr/bin/env python3
"""Writing Like Me local helpers. Python 3.9+, standard library, no network.
Diagnostics do not establish authorship, truth, voice match or publication readiness.
"""
import argparse
import csv
import difflib
import hashlib
import json
import os
import re
import statistics
import sys
import tempfile
import uuid
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSE = {'.md', '.markdown', '.txt'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path_ok(value, write=False):
    # Guards apply to the real location, so a symlinked ancestor (macOS /tmp, /var) neither blocks
    # ordinary use nor lets a write escape into a guarded tree. A symlinked target itself is refused.
    given = Path(os.path.abspath(os.path.expanduser(str(value))))
    if given.is_symlink():
        raise ValueError('Symlinked target; select the real file or folder')
    p = Path(os.path.realpath(str(given)))
    if write:
        if p == ROOT or ROOT in p.parents:
            raise ValueError('Runtime writes into this skill are forbidden')
        if any(x.lower() in {'plugins', 'cache', 'caches', 'marketplaces', '.git'} for x in p.parts):
            raise ValueError('Runtime writes into source/cache locations are forbidden')
        if any((x / 'SKILL.md').is_file() or (x / '.claude-plugin').exists() or
               (x / '.codex-plugin').exists() for x in (p.parent, *p.parents)):
            raise ValueError('Runtime writes into a skill/plugin source tree are forbidden')
    return p


def read(value, prose=False):
    p = path_ok(value)
    if prose and p.suffix.lower() not in PROSE:
        raise ValueError('Select Markdown or plain text; other formats need explicit prose extraction')
    return p, p.read_bytes().decode('utf-8')


def protected(text):
    """Conservative textual spans, not a general Markdown or source-code parser."""
    spans, issues = [], []
    lines = text.splitlines(keepends=True)
    offset, fence, front = 0, None, text.startswith('---\n') or text.startswith('---\r\n')
    front_end = False
    for n, line in enumerate(lines):
        end = offset + len(line)
        stripped = line.rstrip('\r\n')
        if front and not front_end:
            if n and stripped.strip() in {'---', '...'}:
                spans.append((0, end)); front_end = True
        elif fence:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(fence[1]) + r',}\s*', stripped):
                spans.append((fence[2], end)); fence = None
        else:
            opening = re.match(r' {0,3}(`{3,}|~{3,})', line)
            if opening:
                fence = (opening[1][0], len(opening[1]), offset)
            elif re.match(r'\s*>|(?: {4}|\t)\S|\s*\[[^\]]+\]:|\s*(?:\$ |#!)|\s*\|', line):
                spans.append((offset, end))
        offset = end
    if front and not front_end:
        spans.append((0, len(text))); issues.append('unclosed_frontmatter')
    if fence:
        spans.append((fence[2], len(text))); issues.append('unclosed_fence')
    patterns = [r'(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)', r'"[^"\n]*"', r'“[^”]*”',
                r"(?<!\w)'[^'\n]+'(?!\w)", r'‘[^’]*’', r'https?://[^\s<>]+',
                r'<[^>]*>', r'\[(?:\d+|\^[^\]]+)\]']
    for pattern in patterns:
        spans.extend(m.span() for m in re.finditer(pattern, text))
    for m in re.finditer(r'!?\[[^\]\n]*\]\(', text):
        i, depth = m.end(), 1
        while i < len(text) and depth and text[i] not in '\r\n':
            if text[i] == '\\':
                i += 2; continue
            depth += (text[i] == '(') - (text[i] == ')'); i += 1
        spans.append((m.start(), i))
        if depth:
            issues.append('unclosed_link')
    for m in re.finditer(r'[^\n]+(?:\n(?!\s*\n)[^\n]+)*', text):
        if re.match(r'\s*[\[{]', m[0]) or len(re.findall(r'^[\w.-]+:\s', m[0], re.M)) >= 2:
            spans.append(m.span())
    merged = []
    for a, b in sorted(spans):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    masked = list(text)
    for a, b in merged:
        for i in range(a, b):
            if masked[i] not in '\r\n': masked[i] = ' '
    visible = ''.join(masked)
    if any(c in visible for c in ['"', '“', '”', '`', '‘', '’']):
        # Apostrophes within words are ordinary prose, not quote delimiters.
        rem = re.sub(r'\w[’]\w', '', visible)
        if any(c in rem for c in ['"', '“', '”', '`', '‘', '’']):
            issues.append('ambiguous_quote_or_code')
    return merged, visible, sorted(set(issues))


def discover(args):
    # Host is recorded, not used to invent personal guide paths.
    workspace = path_ok(args.workspace)
    home = path_ok(args.home) if args.home else workspace
    rows = []
    for name in ('VOICE.md', 'STYLE.md'):
        p = path_ok(home / name)
        rows.append({'name': name, 'path': str(p), 'exists': p.is_file()})
    return {'host': args.host, 'selected_home': str(home) if args.home else None,
            'candidate_basis': 'explicit_home' if args.home else 'active_workspace_only',
            'guides': rows, 'content_read': False, 'cross_host_search': False,
            'note': 'Absent guides do not block drafting; no home created or inferred'}


def initialize(args):
    home = path_ok(args.home, True)
    template = ROOT / 'assets' / 'home'
    files = sorted(p for p in template.rglob('*') if p.is_file())
    if not files: raise ValueError('Missing local home templates')
    if home.exists() and not home.is_dir(): raise ValueError('Home is not a directory')
    if home.exists() and any(home.iterdir()) and not args.add_missing:
        raise ValueError('Home is nonempty; inspect first, then explicitly use --add-missing')
    create, preserve = [], []
    for src in files:
        dst = path_ok(home / src.relative_to(template), True)
        if dst.exists() and not dst.is_file(): raise ValueError('Template destination has conflicting type')
        for parent in dst.parents:
            if parent.exists() and not parent.is_dir(): raise ValueError('Destination parent is not a directory')
        (preserve if dst.exists() else create).append(str(dst))
    if args.confirmed:
        for src in files:
            dst = path_ok(home / src.relative_to(template), True)
            if str(dst) in create:
                dst.parent.mkdir(parents=True, exist_ok=True)
                with dst.open('xb') as f: f.write(src.read_bytes())
    return {'mode': 'apply' if args.confirmed else 'preview', 'home': str(home),
            'created' if args.confirmed else 'would_create': create, 'preserved': preserve}


def guide(args):
    home = path_ok(args.home, True)
    if not home.is_dir(): raise ValueError('Home missing; resolve setup separately')
    target = path_ok(home / args.guide, True)
    _, proposed = read(args.proposed)
    before = target.read_bytes() if target.exists() else None
    old = before.decode('utf-8') if before is not None else ''
    current = digest(before) if before is not None else 'missing'
    change = ''.join(difflib.unified_diff(old.splitlines(True), proposed.splitlines(True),
                                       fromfile=args.guide, tofile=args.guide))
    report = {'mode': 'preview', 'path': str(target), 'expected_sha256': current,
              'proposed_sha256': digest(proposed.encode('utf-8')), 'diff': change}
    if not args.confirmed: return report
    if not args.expected_sha256 or current != args.expected_sha256:
        raise ValueError('Missing or stale expected hash; read again and revise proposal')
    if old == proposed:
        report.update(mode='unchanged', saved=False); return report
    lock = path_ok(home / '.wlm-guide.lock', True)
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    temp = None
    try:
        path_ok(target, True)
        latest = target.read_bytes() if target.exists() else None
        if latest != before: raise ValueError('Concurrent edit; no guide was replaced')
        history = path_ok(home / '.history', True)
        history.mkdir(exist_ok=True)
        backup = None
        if before is not None:
            backup = history / (args.guide + '.' + uuid.uuid4().hex + '.bak')
            with backup.open('xb') as f: f.write(before)
        fd, temp = tempfile.mkstemp(prefix='.wlm-', dir=str(home))
        with os.fdopen(fd, 'wb') as f:
            f.write(proposed.encode('utf-8')); f.flush(); os.fsync(f.fileno())
        path_ok(target, True)
        latest = target.read_bytes() if target.exists() else None
        if latest != before: raise ValueError('Concurrent edit before replace; no guide was replaced')
        os.replace(temp, target); temp = None
        report.update(mode='apply', saved=True, backup=str(backup) if backup else None)
        return report
    finally:
        if temp and os.path.exists(temp): os.unlink(temp)
        lock.unlink()


def protection(args):
    _, before = read(args.before, True); _, after = read(args.after, True)
    a, _, ai = protected(before); b, _, bi = protected(after)
    seq_a = [digest(before[x:y].encode()) for x, y in a]
    seq_b = [digest(after[x:y].encode()) for x, y in b]
    exact_errors = []
    for filename in args.exact:
        _, exact = read(filename)
        if not exact or before.count(exact) == 0 or before.count(exact) != after.count(exact):
            exact_errors.append(str(filename))
    valid = seq_a == seq_b and not ai and not bi and not exact_errors
    return {'valid': valid, 'before_spans': len(a), 'after_spans': len(b),
            'changed': seq_a != seq_b, 'manual_review': sorted(set(ai + bi)),
            'exact_block_failures': exact_errors,
            'limit': 'Textual protected-span comparison; semantic/code validity requires the owning workflow'}, 0 if valid else 1


def stats(text):
    words = re.findall(r"\b[\w]+(?:['’][\w]+)*\b", text)
    sentences = [x for x in re.split(r'[.!?]+(?:\s+|$)', text) if x.strip()]
    lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    return {'words': len(words), 'characters': len(text), 'utf8_bytes': len(text.encode()),
            'paragraphs': len([x for x in re.split(r'\n\s*\n', text) if x.strip()]),
            'sentence_word_counts': lengths, 'mean_sentence_words': statistics.mean(lengths) if lengths else None,
            'sentence_words_stdev': statistics.pstdev(lengths) if lengths else None,
            'contractions': len(re.findall(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", text, re.I)),
            'questions': text.count('?'), 'first_person': len(re.findall(r'\b(?:I|me|my|mine|we|us|our)\b', text)),
            'limit': 'Mechanical text statistics; not an identity, authorship or quality score'}


def scan(args):
    _, text = read(args.file, True)
    spans, visible, warnings = protected(text)
    findings = []
    lexicon = ROOT / 'references' / 'lexicon.csv'
    if not lexicon.is_file(): raise ValueError('Missing local lexicon')
    with lexicon.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    for i, row in enumerate(rows, 2):
        phrase = row.get('Example (literal or template)', '').strip()
        if not phrase or '[' in phrase or '...' in phrase: continue
        pattern = r'(?<!\w)' + re.escape(phrase) + r'(?!\w)'
        for m in re.finditer(pattern, visible, re.I):
            findings.append({'line': text.count('\n', 0, m.start()) + 1, 'offset': m.start(),
                             'lexicon_row': i, 'category': row.get('Category'), 'kind': 'contextual_candidate'})
    for label, regex in [
        ('em_dash', r'—|―|[ \t]+–[ \t]+'),
        ('trailing_analysis', r',\s*(?:highlighting|showcasing|symbolizing|underscoring)\b'),
        ('negative_parallelism', r'\bnot (?:just|only|merely)\b'),
        ('staged_reveal', r'\b(?:plot twist|the best part|the answer)\s*[:?]'),
        ('vague_authority', r'\b(?:experts (?:say|agree|believe)|studies show|research indicates)\b'),
        ('hedge_cluster', r'\b(?:could|might|possibly|potentially|perhaps)\s+(?:possibly|potentially|perhaps)\b'),
        ('recap_ending', r'\b(?:in conclusion|to sum up|the future looks bright)\b')]:
        for m in re.finditer(regex, visible, re.I):
            findings.append({'line': text.count('\n', 0, m.start()) + 1, 'offset': m.start(), 'category': label, 'kind': 'contextual_candidate'})
    return {'profile': args.profile, 'findings': sorted(findings, key=lambda x: (x['offset'], x.get('lexicon_row', 0))),
            'protected_spans': len(spans), 'manual_review': warnings,
            'result': 'diagnostics_only', 'limit': 'Does not detect all 47 semantic families or prove authorship, truth, voice or readiness'}


def claims(args):
    _, text = read(args.file); data = json.loads(text); errors = []
    if not isinstance(data, dict): return {'valid': False, 'errors': ['ledger must be an object']}, 1
    if not isinstance(data.get('evidence_scope'), str) or not data['evidence_scope'].strip(): errors.append('evidence_scope required')
    items = data.get('claims'); seen = set()
    if not isinstance(items, list): items = []; errors.append('claims must be an array')
    for i, item in enumerate(items):
        if not isinstance(item, dict): errors.append('claim %d is not an object' % i); continue
        identifier = item.get('id')
        if not isinstance(identifier, str) or not identifier.strip() or identifier in seen: errors.append('claim %d needs a unique string id' % i)
        elif identifier: seen.add(identifier)
        if not isinstance(item.get('claim'), str) or not item['claim'].strip(): errors.append('claim %d needs text' % i)
        if item.get('status') not in ('supported', 'unsupported', 'uncertain', 'non-factual'): errors.append('claim %d invalid status' % i)
        if item.get('remedy') not in ('keep', 'remove', 'qualify', 'verify', 'source'): errors.append('claim %d invalid remedy' % i)
        if not isinstance(item.get('evidence'), str): errors.append('claim %d needs evidence string' % i)
        elif item.get('status') == 'supported' and not item['evidence'].strip(): errors.append('claim %d supported requires evidence locator' % i)
    return {'valid': not errors, 'errors': errors, 'limit': 'Schema validation only; source support must be inspected'}, 0 if not errors else 1


def punctuation(args):
    src, text = read(args.file, True); spans, visible, issues = protected(text)
    if issues: raise ValueError('Ambiguous protected material; select prose manually')
    # The dash and the spaces around it are replaced together: "word — next" becomes "word, next".
    matches = list(re.finditer(r'[ \t]*(?:[—―]|(?<=\s)–(?=\s))[ \t]*', visible))
    result = text
    for m in reversed(matches):
        right = text[m.end():]
        if not right or right[:1] in '\r\n':
            joint = '.' if result[:m.start()][-1:].isalnum() else ''
        else:
            joint = '. ' if right[:1].isupper() else ', '
        result = result[:m.start()] + joint + result[m.end():]
    if args.output:
        out = path_ok(args.output, True)
        if out.suffix.lower() not in PROSE: raise ValueError('Output must be a prose file')
        with out.open('xb') as f: f.write(result.encode('utf-8'))
    return {'mode': 'output' if args.output else 'preview', 'changes': len(matches),
            'output': str(args.output) if args.output else None,
            'diff': ''.join(difflib.unified_diff(text.splitlines(True), result.splitlines(True), fromfile=src.name, tofile=src.name)),
            'limit': 'Punctuation proposal needs sentence-level review; original input is never overwritten'}


def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest='command', required=True)
    d = sub.add_parser('discover'); d.add_argument('--host', required=True, choices=['codex', 'claude-code']); d.add_argument('--workspace', required=True); d.add_argument('--home')
    i = sub.add_parser('init'); i.add_argument('--home', required=True); i.add_argument('--add-missing', action='store_true'); i.add_argument('--confirmed', action='store_true')
    g = sub.add_parser('guide'); g.add_argument('--home', required=True); g.add_argument('--guide', choices=['VOICE.md', 'STYLE.md'], required=True); g.add_argument('--proposed', required=True); g.add_argument('--expected-sha256'); g.add_argument('--confirmed', action='store_true')
    v = sub.add_parser('protect'); v.add_argument('before'); v.add_argument('after'); v.add_argument('--exact', action='append', default=[])
    for name in ('scan', 'profile', 'claims', 'count', 'punctuation', 'business'):
        q = sub.add_parser(name); q.add_argument('file')
        if name == 'scan': q.add_argument('--profile', choices=['blog', 'technical-blog', 'docs', 'casual', 'linkedin', 'investor-email'], default='blog')
        if name == 'punctuation': q.add_argument('--output')
    args = p.parse_args(); code = 0
    try:
        funcs = {'discover': discover, 'init': initialize, 'guide': guide, 'protect': protection,
                 'scan': scan, 'claims': claims, 'punctuation': punctuation}
        if args.command in funcs: result = funcs[args.command](args)
        else:
            _, text = read(args.file, True)
            if args.command in ('count', 'profile'): result = stats(text)
            else:
                terms = ('recommendation', 'decision', 'risk', 'assumption', 'open question', 'next')
                result = {'signals': {term: len(re.findall(r'\b' + re.escape(term) + r'\b', text, re.I)) for term in terms},
                          'result': 'diagnostics_only', 'limit': 'Headings and action sections are not universal requirements; inspect reader intent and evidence'}
        if isinstance(result, tuple): result, code = result
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)); return code
    except (OSError, ValueError, UnicodeError) as exc:
        print(json.dumps({'error': str(exc), 'result': 'blocked_or_invalid'}, ensure_ascii=False)); return 2


if __name__ == '__main__':
    sys.exit(main())
