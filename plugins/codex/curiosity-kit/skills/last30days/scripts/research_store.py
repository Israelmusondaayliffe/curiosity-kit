#!/usr/bin/env python3
"""Bounded, offline research records. Python 3.9+; no network or subprocesses.

Integrity checks validate declared structure, never truth or permission to share.
"""
import argparse
import copy
import datetime as dt
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

SCHEMA = 'last30days.run/v1'
MAX_BYTES = 8 * 1024 * 1024
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$')
VIS = {'public', 'private', 'unknown'}
LANES = {'ok', 'partial', 'no_results', 'failed', 'unavailable', 'not_attempted', 'excluded'}

class StoreError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)

def fail(message, code='invalid_record'):
    raise StoreError(code, message)

def obj(value, required, optional=(), where='record'):
    if not isinstance(value, dict):
        fail(where + ': expected object')
    missing, extra = set(required) - set(value), set(value) - set(required) - set(optional)
    if missing or extra:
        fail('%s: missing=%s unknown=%s' % (where, sorted(missing), sorted(extra)))

def string(value, where, nullable=False):
    if value is None and nullable:
        return
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 and c not in '\n\r\t' for c in value):
        fail(where + ': expected nonempty text without control characters')

def ident(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        fail('unsafe or invalid ID', 'invalid_id')
    return value

def enum(value, allowed, where):
    if not isinstance(value, str) or value not in allowed:
        fail(where + ': expected one of ' + ', '.join(sorted(allowed)))

def sequence(value, where):
    if not isinstance(value, list):
        fail(where + ': expected array')
    return value

def unique(values, where):
    if len(values) != len(set(values)):
        fail(where + ': duplicate IDs or values')

def timestamp(value, where, nullable=False):
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', value):
        fail(where + ': expected RFC3339 timestamp with timezone')
    try:
        normalized = re.sub(r'\.(\d+)', lambda m: '.' + (m.group(1) + '000000')[:6], value)
        result = dt.datetime.fromisoformat(normalized.replace('Z', '+00:00'))
        if result.tzinfo is None:
            raise ValueError()
        return result
    except ValueError:
        fail(where + ': impossible timestamp')

def day(value):
    try:
        if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError()
        return dt.date.fromisoformat(value)
    except ValueError:
        fail('expected valid YYYY-MM-DD date')

def window_bounds(w):
    if w['boundary'] == 'inclusive':
        zone = ZoneInfo(w['timezone'])
        return (dt.datetime.combine(day(w['start']), dt.time.min, zone),
                dt.datetime.combine(day(w['end']) + dt.timedelta(days=1), dt.time.min, zone))
    return timestamp(w['start'], 'window.start'), timestamp(w['end'], 'window.end')

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(value).hexdigest()

def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            fail('duplicate JSON key: ' + key, 'invalid_json')
        result[key] = value
    return result

def decode(data):
    try:
        return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda _: fail('nonfinite JSON number', 'invalid_json'))
    except (UnicodeError, ValueError, RecursionError) as exc:
        fail('invalid UTF-8 JSON: ' + str(exc), 'invalid_json')

def safe_path(value):
    p = Path(os.path.abspath(os.fspath(value)))
    # Canonicalize only the fixed macOS system aliases; never arbitrary links.
    if sys.platform == 'darwin' and len(p.parts) > 1 and p.parts[1] in {'tmp', 'var'}:
        alias = Path('/') / p.parts[1]
        target = '/private/' + p.parts[1]
        if alias.is_symlink() and os.readlink(alias) in {target, target.lstrip('/')}:
            p = Path(target).joinpath(*p.parts[2:])
    # Refuse all remaining symlinks, including the supplied root and store internals.
    for part in [p] + list(p.parents):
        if part.is_symlink():
            fail('symlink paths are not supported', 'unsafe_path')
    return p

def read_bytes(value):
    p = safe_path(value)
    try:
        fd = os.open(str(p), os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
        with os.fdopen(fd, 'rb') as f:
            if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
                fail('input is not a regular file', 'unsafe_path')
            data = f.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            fail('input exceeds 8 MiB', 'size_limit')
        return data
    except FileNotFoundError:
        fail('requested file is missing', 'missing_file')
    except OSError as exc:
        fail('cannot read input: ' + exc.strerror, 'unreadable')

def load(value):
    return decode(read_bytes(value))

def safe_url(value, public=False):
    string(value, 'url')
    if any(c.isspace() for c in value) or any(ord(c) < 32 for c in value):
        fail('unsafe URL', 'unsafe_url')
    parsed = urlsplit(value)
    schemes = {'http', 'https'} if public else {'http', 'https', 'corpus', 'urn'}
    if parsed.scheme not in schemes or parsed.username or parsed.password:
        fail('unsupported or credential-bearing URL', 'unsafe_url')
    if parsed.scheme in {'http', 'https'} and not parsed.hostname:
        fail('URL requires a hostname', 'unsafe_url')
    return value

def scope_check(scope):
    obj(scope, ['entity', 'queries', 'window', 'lanes', 'selection'], where='scope')
    string(scope['entity'], 'scope.entity')
    for q in sequence(scope['queries'], 'queries'):
        string(q, 'query')
    unique(scope['queries'], 'queries')
    if not scope['queries']:
        fail('queries must not be empty')
    w = scope['window']
    obj(w, ['start', 'end', 'timezone', 'boundary'], where='window')
    enum(w['boundary'], {'inclusive', 'half-open'}, 'window.boundary')
    string(w['timezone'], 'window.timezone')
    try:
        ZoneInfo(w['timezone'])
    except (ZoneInfoNotFoundError, ValueError):
        fail('unknown or unavailable timezone')
    start, end = window_bounds(w)
    if start >= end:
        fail('window start must precede end')
    for lane in sequence(scope['lanes'], 'lanes'):
        obj(lane, ['id', 'status', 'detail'], where='lane')
        ident(lane['id'])
        enum(lane['status'], LANES, 'lane.status')
        string(lane['detail'], 'lane.detail')
    unique([x['id'] for x in scope['lanes']], 'lanes')
    obj(scope['selection'], ['cap', 'method'], where='selection')
    cap = scope['selection']['cap']
    if cap is not None and (type(cap) is not int or cap < 0):
        fail('selection.cap must be null or nonnegative integer')
    string(scope['selection']['method'], 'selection.method')

def numeric(value, where):
    if type(value) not in (float, int) or not math.isfinite(value):
        fail(where + ': expected finite number')

def datum_check(d):
    obj(d, ['kind', 'key', 'value', 'unit', 'denominator', 'observed_at'], ['modality'], where='datum')
    if 'modality' in d:
        enum(d['modality'], {'asserted', 'quoted', 'hypothetical', 'question', 'negated'}, 'datum.modality')
    enum(d['kind'], {'number', 'probability', 'percentage', 'status', 'date'}, 'datum.kind')
    for k in ('key', 'unit'):
        string(d[k], 'datum.' + k)
    string(d['denominator'], 'datum.denominator', True)
    timestamp(d['observed_at'], 'datum.observed_at')
    if d['kind'] in {'number', 'probability', 'percentage'}:
        numeric(d['value'], 'datum.value')
        if d['kind'] == 'probability' and not 0 <= d['value'] <= 1:
            fail('probability outside 0..1')
        if d['kind'] == 'percentage' and not 0 <= d['value'] <= 100:
            fail('percentage outside 0..100')
    elif d['kind'] == 'date':
        day(d['value'])
    else:
        string(d['value'], 'datum.value')

def text_integrity(value):
    if isinstance(value, str):
        if any((ord(c) < 32 and c not in '\n\r\t') or 0xD800 <= ord(c) <= 0xDFFF or ord(c) in (0xFFFE, 0xFFFF, 0x7F) for c in value):
            fail('text contains unsupported control or Unicode scalar')
    elif isinstance(value, dict):
        for key, item in value.items():
            text_integrity(key); text_integrity(item)
    elif isinstance(value, list):
        for item in value:
            text_integrity(item)

def validate(record):
    text_integrity(record)
    obj(record, ['schema', 'id', 'created_at', 'scope', 'sources', 'claims', 'findings'], ['public_metadata', 'derivation'], 'run')
    if record['schema'] != SCHEMA:
        fail('unsupported run schema')
    ident(record['id'])
    created = timestamp(record['created_at'], 'created_at')
    scope_check(record['scope'])
    lanes = {x['id']: x['status'] for x in record['scope']['lanes']}
    source_ids = []
    for s in sequence(record['sources'], 'sources'):
        obj(s, ['id', 'lane', 'url', 'title', 'body', 'visibility', 'origin_id', 'published_at', 'retrieved_at', 'read_status', 'date_basis', 'engagement', 'locators'], ['author', 'community', 'event_at', 'content_hash', 'original_published_at', 'eligibility', 'origin_url', 'origin_note'], 'source')
        source_ids.append(ident(s['id']))
        if s['lane'] not in lanes or lanes[s['lane']] in {'excluded', 'not_attempted', 'no_results', 'unavailable', 'failed'}:
            fail('source lane missing or incompatible with collected items')
        safe_url(s['url'])
        for k in ('title', 'origin_id'):
            string(s[k], 'source.' + k)
        if s['body'] is not None and not isinstance(s['body'], str):
            fail('source.body must be text or null')
        enum(s['visibility'], VIS, 'source.visibility')
        enum(s['read_status'], {'full', 'partial', 'metadata_only', 'unreadable'}, 'read_status')
        enum(s['date_basis'], {'publication', 'event', 'updated', 'unknown', 'historical_context', 'future_publication'}, 'date_basis')
        pub = timestamp(s['published_at'], 'published_at', True)
        retrieved = timestamp(s['retrieved_at'], 'retrieved_at')
        if retrieved > created:
            fail('source retrieval is after run creation')
        if pub and pub > created and s['date_basis'] != 'future_publication':
            fail('future publication must be explicitly labelled future_publication')
        if s['body'] is None and s['read_status'] in {'full', 'partial'}:
            fail('read source requires supplied body')
        if 'content_hash' in s:
            if s['body'] is None or s['content_hash'] != digest(s['body'].encode('utf-8')):
                fail('content_hash does not match supplied body')
        for k in ('author', 'community'):
            if k in s:
                string(s[k], 'source.' + k, True)
        if 'original_published_at' in s:
            timestamp(s['original_published_at'], 'original_published_at', True)
        if 'origin_url' in s:
            safe_url(s['origin_url'])
        if 'origin_note' in s:
            string(s['origin_note'], 'origin_note')
        if 'eligibility' in s:
            enum(s['eligibility'], {'eligible', 'historical_context', 'undated', 'future_publication', 'entity_mismatch', 'out_of_window', 'unreviewed'}, 'eligibility')
        if 'event_at' in s:
            timestamp(s['event_at'], 'event_at', True)
        for e in sequence(s['engagement'], 'engagement'):
            obj(e, ['metric', 'value', 'unit', 'denominator', 'observed_at'], where='engagement')
            numeric(e['value'], 'engagement.value')
            for k in ('metric', 'unit'):
                string(e[k], k)
            string(e['denominator'], 'denominator', True)
            timestamp(e['observed_at'], 'engagement.observed_at')
        for loc in sequence(s['locators'], 'locators'):
            obj(loc, ['kind', 'url', 'label', 'author', 'text'], where='locator')
            for k in ('kind', 'label'):
                string(loc[k], k)
            safe_url(loc['url'])
            string(loc['author'], 'locator.author', True)
            string(loc['text'], 'locator.text', True)
    unique(source_ids, 'sources')
    cap = record['scope']['selection']['cap']
    if cap is not None and len(source_ids) > cap:
        fail('source count exceeds declared cap')
    def refs(values, allowed, where, nonempty=False):
        sequence(values, where)
        for value in values:
            ident(value)
        unique(values, where)
        if not set(values) <= set(allowed) or (nonempty and not values):
            fail(where + ': dangling or empty evidence references')
    claim_ids = []
    for c in sequence(record['claims'], 'claims'):
        obj(c, ['id', 'text', 'source_ids', 'visibility', 'review_status'], ['datum'], 'claim')
        claim_ids.append(ident(c['id']))
        string(c['text'], 'claim.text')
        refs(c['source_ids'], source_ids, 'claim.source_ids', True)
        enum(c['visibility'], VIS, 'claim.visibility')
        enum(c['review_status'], {'supported', 'contradicted', 'uncertain', 'unreviewed'}, 'review_status')
        if 'datum' in c:
            datum_check(c['datum'])
            if timestamp(c['datum']['observed_at'], 'datum.observed_at') > created:
                fail('datum observation is after run creation')
    unique(claim_ids, 'claims')
    finding_ids = []
    for f in sequence(record['findings'], 'findings'):
        obj(f, ['id', 'text', 'source_ids', 'claim_ids', 'visibility'], where='finding')
        finding_ids.append(ident(f['id']))
        string(f['text'], 'finding.text')
        refs(f['source_ids'], source_ids, 'finding.source_ids', True)
        refs(f['claim_ids'], claim_ids, 'finding.claim_ids')
        enum(f['visibility'], VIS, 'finding.visibility')
    unique(finding_ids, 'findings')
    if 'public_metadata' in record:
        obj(record['public_metadata'], ['reviewed', 'title', 'entity'], ['coverage', 'window'], where='public_metadata')
        if 'coverage' in record['public_metadata']:
            for caveat in sequence(record['public_metadata']['coverage'], 'public_metadata.coverage'):
                string(caveat, 'public caveat')
        if 'window' in record['public_metadata'] and record['public_metadata']['window'] != record['scope']['window']:
            fail('public window must match exact research scope window')
        if type(record['public_metadata']['reviewed']) is not bool:
            fail('public_metadata.reviewed must be boolean')
        for k in ('title', 'entity'):
            string(record['public_metadata'][k], 'public_metadata.' + k)
    if 'derivation' in record:
        d = record['derivation']
        obj(d, ['parent_run_id', 'source_ids', 'claim_ids', 'finding_ids', 'operation'], where='derivation')
        ident(d['parent_run_id'])
        if d['parent_run_id'] == record['id']:
            fail('run cannot derive from itself')
        string(d['operation'], 'derivation.operation')
        for k in ('source_ids', 'claim_ids', 'finding_ids'):
            sequence(d[k], 'derivation.' + k)
            for value in d[k]:
                ident(value)
            unique(d[k], 'derivation.' + k)
    return record

def derivation_check(root, r):
    if 'derivation' not in r:
        return
    d = r['derivation']
    parent = get_run(root, d['parent_run_id'])
    for key, collection in [('source_ids', 'sources'), ('claim_ids', 'claims'), ('finding_ids', 'findings')]:
        if not set(d[key]) <= {x['id'] for x in parent[collection]}:
            fail('derivation references absent parent items', 'invalid_derivation')

def root_path(root, write=False):
    p = safe_path(root)
    if not p.exists():
        if not write:
            fail('store does not exist', 'missing_store')
        p.mkdir(mode=0o700, parents=True)
    if not p.is_dir():
        fail('store root is not a directory', 'invalid_store')
    return p

def folder(root, kind, write=False):
    p = safe_path(root_path(root, write) / kind)
    if not p.exists():
        if write:
            p.mkdir(mode=0o700)
        else:
            return p
    if not p.is_dir():
        fail('store component is not a directory', 'invalid_store')
    return p

def atomic_new(path, data):
    p = safe_path(path)
    parent = safe_path(p.parent)
    if not parent.is_dir():
        fail('output parent directory must already exist', 'missing_directory')
    temp = None
    try:
        fd, temp = tempfile.mkstemp(prefix='.pending-', dir=str(parent))
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.link(temp, p)  # Atomic create-if-absent; never replace a prior artifact.
        dfd = os.open(str(parent), os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except FileExistsError:
        fail('destination already exists; choose a new output or identity', 'conflict')
    finally:
        if temp is not None:
            os.unlink(temp)

def save_record(root, kind, record):
    payload = canonical(record) + b'\n'
    if len(payload) > MAX_BYTES:
        fail('serialized record exceeds 8 MiB including JSON escaping and metadata', 'size_limit')
    path = folder(root, kind, True) / (ident(record['id']) + '.json')
    if path.exists():
        if read_bytes(path) == payload:
            return {'id': record['id'], 'status': 'unchanged'}
        fail('same ID already has different content', 'conflict')
    try:
        atomic_new(path, payload)
    except StoreError as exc:
        if exc.code == 'conflict' and read_bytes(path) == payload:
            return {'id': record['id'], 'status': 'unchanged'}
        raise
    return {'id': record['id'], 'status': 'created'}

def get_run(root, run_id):
    p = folder(root, 'runs') / (ident(run_id) + '.json')
    r = validate(load(p))
    if r['id'] != run_id:
        fail('stored filename and run ID differ', 'corrupt_store')
    return r

def all_records(root, kind):
    p = folder(root, kind)
    if not p.exists():
        return []
    result = []
    for file in sorted(p.iterdir()):
        if file.name.startswith('.pending-'):
            continue  # Interrupted temporary writes cannot become valid records.
        if file.suffix != '.json':
            fail('unrecognized store file', 'corrupt_store')
        r = load(file)
        if kind == 'runs':
            validate(r)
        else:
            artifact_check(r, kind)
        if r['id'] != file.stem:
            fail('stored filename and record ID differ', 'corrupt_store')
        result.append(r)
    return result

def artifact_check(r, kind):
    required = ['schema', 'id', 'created_at', 'visibility', 'original_path', 'sha256', 'content', 'published_at', 'entity', 'window', 'freshness']
    if kind == 'corpus':
        required += ['document_id', 'modified_at']
    obj(r, required, where=kind)
    if r['schema'] != 'last30days.' + ('corpus' if kind == 'corpus' else 'legacy') + '/v1':
        fail('unsupported artifact schema', 'corrupt_store')
    ident(r['id'])
    timestamp(r['created_at'], 'artifact.created_at')
    enum(r['visibility'], {'private'}, 'artifact.visibility')
    string(r['original_path'], 'artifact.original_path')
    if not isinstance(r['content'], str) or not isinstance(r['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', r['sha256']) or r['freshness'] != 'unknown':
        fail('invalid artifact content/hash/freshness', 'corrupt_store')
    if r['published_at'] is not None or r['entity'] is not None or r['window'] is not None:
        fail('legacy/corpus metadata must remain unknown', 'corrupt_store')
    try:
        raw = r['content'].encode('utf-8')
        if digest(raw) != r['sha256']:
            fail('artifact content hash mismatch', 'corrupt_store')
    except (ValueError, UnicodeError):
        fail('artifact encoding invalid', 'corrupt_store')
    if kind == 'corpus':
        timestamp(r['modified_at'], 'modified_at')

def import_file(root, filename, record_id=None, corpus=False):
    path = safe_path(filename)
    if path.suffix.lower() not in {'.md', '.txt', '.json'}:
        fail('only explicit .md/.txt/.json or extracted text files supported', 'unsupported_format')
    raw = read_bytes(path)
    try:
        content = raw.decode('utf-8')
    except UnicodeError:
        fail('import requires UTF-8 text', 'invalid_text')
    kind = 'corpus' if corpus else 'legacy'
    h = digest(raw)
    doc = digest(str(path).encode())
    rid = record_id or (kind + '-' + digest((doc + h).encode())[:32])
    existing = safe_path(Path(root) / kind / (ident(rid) + '.json'))
    if existing.exists():
        old = load(existing)
        artifact_check(old, kind)
        if old['sha256'] == h and old['original_path'] == str(path):
            return {'id': rid, 'status': 'unchanged'}
        fail('import ID conflicts with existing artifact', 'conflict')
    record = {'schema': 'last30days.' + kind + '/v1', 'id': rid, 'created_at': now(), 'visibility': 'private', 'original_path': str(path), 'sha256': h, 'content': content, 'published_at': None, 'entity': None, 'window': None, 'freshness': 'unknown'}
    if corpus:
        record.update(document_id=doc, modified_at=dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat())
    return save_record(root, kind, record)

def search(root, query, entity=None, start=None, end=None, source=None, corpus=False):
    terms = query.casefold().split()
    if not terms:
        fail('search requires nonempty query')
    if start:
        day(start)
    if end:
        day(end)
    if start and end and day(start) > day(end):
        fail('search start exceeds end')
    rows = []
    kinds = ['corpus'] if corpus else ['runs', 'legacy']
    for kind in kinds:
        for r in all_records(root, kind):
            if kind == 'runs':
                if entity and entity.casefold() != r['scope']['entity'].casefold():
                    continue
                inherited_visibility = derivation_visibility(root, r)
                for s in r['sources']:
                    if source and s['lane'] != source:
                        continue
                    published = timestamp(s['published_at'], 'published_at').astimezone(ZoneInfo(r['scope']['window']['timezone'])).date().isoformat() if s['published_at'] else None
                    if (start or end) and (not published or (start and published < start) or (end and published > end)):
                        continue
                    text = s['title'] + '\n' + (s['body'] or '')
                    if all(t in text.casefold() for t in terms):
                        rows.append({'run_id': r['id'], 'item_id': s['id'], 'locator': 'urn:last30days:run:' + r['id'] + ':' + s['id'], 'url': s['url'], 'entity': r['scope']['entity'], 'published_at': s['published_at'], 'retrieved_at': s['retrieved_at'], 'date_basis': s['date_basis'], 'visibility': merge_visibility([s['visibility'], inherited_visibility]), 'excerpt': excerpt(text, terms), 'kind': 'historical_run'})
            elif not any([entity, start, end, source]) and all(t in r['content'].casefold() for t in terms):
                rows.append({'artifact_id': r['id'], 'locator': 'urn:last30days:' + kind + ':' + r['id'], 'original_path': r['original_path'], 'visibility': 'private', 'published_at': None, 'excerpt': excerpt(r['content'], terms), 'kind': kind})
    return {'status': 'ok' if rows else 'empty', 'results': rows}

def excerpt(text, terms):
    pos = min([text.casefold().find(t) for t in terms])
    return text[max(0, pos - 80):max(0, pos - 80) + 500]

def watch_state(root):
    p = folder(root, 'watch')
    if not p.exists():
        return {'schema': 'last30days.watch/v1', 'revision': 0, 'topics': {}}
    files = sorted(f for f in p.iterdir() if not f.name.startswith('.pending-'))
    state = {'schema': 'last30days.watch/v1', 'revision': 0, 'topics': {}}
    for index, file in enumerate(files, 1):
        if file.name != '%010d.json' % index:
            fail('watch revision history is incomplete or invalid', 'corrupt_store')
        item = load(file)
        obj(item, ['schema', 'revision', 'topics'], where='watch')
        if item['schema'] != 'last30days.watch/v1' or type(item['revision']) is not int or item['revision'] != index or not isinstance(item['topics'], dict):
            fail('invalid watch snapshot', 'corrupt_store')
        for name, t in item['topics'].items():
            ident(name)
            obj(t, ['name', 'scope', 'status', 'schedule_request', 'scheduler_status', 'runs'], where='watch topic')
            if t['name'] != name or t['scheduler_status'] != 'unconfigured':
                fail('invalid watch identity or scheduler state', 'corrupt_store')
            scope_check(t['scope'])
            enum(t['status'], {'active', 'paused', 'archived'}, 'watch.status')
            string(t['schedule_request'], 'schedule_request', True)
            for binding in sequence(t['runs'], 'watch.runs'):
                obj(binding, ['run_id', 'relationship', 'recorded_at'], where='binding')
                ident(binding['run_id'])
                string(binding['relationship'], 'relationship', True)
                timestamp(binding['recorded_at'], 'recorded_at')
        state = item
    return state

def comparison_scope(r):
    s = r['scope'] if 'scope' in r else r
    w = s['window']
    return {'entity': s['entity'], 'queries': s['queries'], 'selection': s['selection'], 'lanes': sorted((x['id'], x['status']) for x in s['lanes']), 'window': {'timezone': w['timezone'], 'boundary': w['boundary'], 'duration_seconds': (window_bounds(w)[1] - window_bounds(w)[0]).total_seconds()}}

def watch(args):
    if args.action == 'list':
        state = watch_state(args.root)
        return {'revision': state['revision'], 'topics': [t for t in state['topics'].values() if args.archived or t['status'] != 'archived'], 'scheduler_status': 'unconfigured'}
    root_path(args.root, True)
    state = watch_state(args.root)
    if args.expected_revision is not None and state['revision'] != args.expected_revision:
        fail('expected watch revision is stale', 'stale_revision')
    name = ident(args.name)
    if hasattr(args, 'schedule'):
        string(args.schedule, 'schedule_request', True)
    if hasattr(args, 'relationship'):
        string(args.relationship, 'relationship', True)
    topics = state['topics']
    if args.action == 'add':
        scope = load(args.scope)
        scope_check(scope)
        new = {'name': name, 'scope': scope, 'status': 'active', 'schedule_request': args.schedule, 'scheduler_status': 'unconfigured', 'runs': []}
        if name in topics:
            if topics[name] == new:
                return {'revision': state['revision'], 'topic': topics[name], 'status': 'unchanged'}
            fail('watch name already exists; use update', 'conflict')
        topics[name] = new
    else:
        if args.expected_revision is None:
            fail('mutation requires --expected-revision', 'revision_required')
        if name not in topics:
            fail('watch topic not found', 'missing_topic')
        t = topics[name]
        if args.action == 'update':
            s = load(args.scope)
            scope_check(s)
            t['scope'] = s
            if args.schedule is not None:
                t['schedule_request'] = args.schedule
        elif args.action in {'pause', 'archive', 'restore'}:
            t['status'] = {'pause': 'paused', 'archive': 'archived', 'restore': 'active'}[args.action]
        elif args.action == 'record':
            r = get_run(args.root, args.run_id)
            if (comparison_scope(r) != comparison_scope(t['scope']) or r['scope']['window'] != t['scope']['window']) and not args.relationship:
                fail('run scope differs; supply explicit --relationship', 'scope_mismatch')
            if any(b['run_id'] == r['id'] for b in t['runs']):
                return {'revision': state['revision'], 'topic': t, 'status': 'unchanged'}
            t['runs'].append({'run_id': r['id'], 'relationship': args.relationship, 'recorded_at': now()})
    state['revision'] += 1
    destination = folder(args.root, 'watch', True) / ('%010d.json' % state['revision'])
    try:
        atomic_new(destination, canonical(state) + b'\n')
    except StoreError as exc:
        if exc.code == 'conflict':
            fail('concurrent watch update; reload revision and retry', 'stale_revision')
        raise
    return {'revision': state['revision'], 'topic': topics[name], 'status': 'updated', 'scheduler_status': 'unconfigured'}

def delta(a, b):
    compatible = comparison_scope(a) == comparison_scope(b)
    healthy = all(x['status'] in {'ok', 'no_results', 'excluded'} for r in (a, b) for x in r['scope']['lanes'])
    if not compatible or not healthy:
        return {'before': a['id'], 'after': b['id'], 'comparable': False, 'status': 'unverifiable', 'reason': 'query/entity/selection/window rules/lane outcomes differ or coverage is incomplete', 'categories': {'unverifiable': sorted({s['id'] for s in a['sources'] + b['sources']})}}
    def keyed(r):
        keys = {}
        for s in r['sources']:
            key = (s['lane'], s['url'], s['origin_id'])
            if key in keys:
                fail('ambiguous repeated observation identity', 'incomparable')
            keys[key] = s
        return keys
    left, right = keyed(a), keyed(b)
    groups = {k: [] for k in ['added', 'continuing', 'changed', 'not_observed', 'aged_out', 'unverifiable']}
    for key in sorted(set(left) | set(right)):
        old, new = left.get(key), right.get(key)
        row = {'url': key[1], 'before_source_id': old['id'] if old else None, 'after_source_id': new['id'] if new else None}
        if old is None:
            category = 'added'
        elif new is None:
            observed = timestamp(old.get('original_published_at') or old['published_at'], 'publication', True)
            a_start, a_end = window_bounds(a['scope']['window'])
            b_start, b_end = window_bounds(b['scope']['window'])
            category = 'aged_out' if observed and a_start <= observed < a_end and observed < b_start else 'not_observed'
        elif old['body'] is None or new['body'] is None:
            category = 'unverifiable'
        else:
            changed = any(old[k] != new[k] for k in ('body', 'title', 'engagement', 'published_at'))
            category = 'changed' if changed else 'continuing'
        groups[category].append(row)
    return {'before': a['id'], 'after': b['id'], 'comparable': True, 'status': 'compared', 'categories': groups, 'limitation': 'Observation differences only; not-observed is not disappearance, and changed is not a factual reversal.'}

def freshness(a, b, claim_id=None, source_id=None):
    results = []
    selected = [c for c in a['claims'] if (claim_id is None or c['id'] == claim_id) and (source_id is None or source_id in c['source_ids'])]
    if source_id and source_id not in {s['id'] for s in a['sources']}:
        fail('source selection not found', 'missing_source')
    if claim_id and not selected:
        fail('claim/source selection not found', 'missing_claim')
    sources_a, sources_b = ({s['id']: s for s in r['sources']} for r in (a, b))
    for c in selected:
        d = c.get('datum')
        matches = [x for x in b['claims'] if d and x.get('datum') and all(x['datum'][k] == d[k] for k in ('kind', 'key', 'unit', 'denominator'))]
        result = {'claim_id': c['id'], 'updated_claim_id': None, 'status': 'unverifiable', 'visibility': 'unknown', 'before_sources': c['source_ids'], 'after_sources': [], 'reason': 'No unique comparable reviewed typed datum'}
        if len(matches) == 1:
            new = matches[0]
            result.update(updated_claim_id=new['id'], after_sources=new['source_ids'])
            deps = [sources_a[x] for x in c['source_ids']] + [sources_b[x] for x in new['source_ids']]
            labels = [x['visibility'] for x in deps] + [c['visibility'], new['visibility']]
            result['visibility'] = 'private' if 'private' in labels else 'unknown' if 'unknown' in labels else 'public'
            origins_a = {(sources_a[x]['url'], sources_a[x]['origin_id']) for x in c['source_ids']}
            origins_b = {(sources_b[x]['url'], sources_b[x]['origin_id']) for x in new['source_ids']}
            good = a['scope']['entity'] == b['scope']['entity'] and origins_a == origins_b and c['review_status'] == new['review_status'] == 'supported' and all(x['read_status'] in {'full', 'partial'} for x in deps) and new['datum'].get('modality', 'asserted') == d.get('modality', 'asserted') == 'asserted' and timestamp(new['datum']['observed_at'], 'observed_at') > timestamp(d['observed_at'], 'observed_at')
            if good:
                result.update(status='unchanged' if d['value'] == new['datum']['value'] else 'changed', before_value=d['value'], after_value=new['datum']['value'], kind=d['kind'], key=d['key'], unit=d['unit'], denominator=d['denominator'], observed_at=new['datum']['observed_at'], reason='Exact saved typed observations compared; no live verification')
        results.append(result)
    return {'before': a['id'], 'after': b['id'], 'checked_at': now(), 'results': results, 'limitation': 'No retrieval performed. Unchanged values or bytes do not verify every external fact.'}

def derivation_visibility(root, r, seen=None):
    seen = set() if seen is None else seen
    if r['id'] in seen:
        fail('cyclic derivation', 'corrupt_store')
    seen.add(r['id'])
    if 'derivation' not in r:
        return 'public'
    d = r['derivation']; parent = get_run(root, d['parent_run_id'])
    sources = {x['id']: x for x in parent['sources']}
    claims = {x['id']: x for x in parent['claims']}
    source_ids, claim_ids = set(d['source_ids']), set(d['claim_ids'])
    labels = []
    for f in parent['findings']:
        if f['id'] in d['finding_ids']:
            labels.append(f['visibility']); source_ids.update(f['source_ids']); claim_ids.update(f['claim_ids'])
    for key in claim_ids:
        c = claims[key]; labels.append(c['visibility']); source_ids.update(c['source_ids'])
    labels += [sources[x]['visibility'] for x in source_ids]
    labels.append(derivation_visibility(root, parent, seen))
    return 'private' if 'private' in labels else 'unknown' if 'unknown' in labels else 'public'

def project(r, visibility):
    if visibility == 'private':
        return copy.deepcopy(r)
    meta = r.get('public_metadata')
    if not meta or meta['reviewed'] is not True:
        fail('public projection requires explicitly reviewed public_metadata', 'public_projection_blocked')
    sources = []
    for s in r['sources']:
        if s['visibility'] == 'public':
            safe_url(s['url'], True)
            if 'origin_url' in s:
                safe_url(s['origin_url'], True)
            for loc in s['locators']:
                safe_url(loc['url'], True)
            sources.append(copy.deepcopy(s))
    source_ids = {s['id'] for s in sources}
    claims = [copy.deepcopy(c) for c in r['claims'] if c['visibility'] == 'public' and set(c['source_ids']) <= source_ids]
    claim_ids = {c['id'] for c in claims}
    findings = [copy.deepcopy(f) for f in r['findings'] if f['visibility'] == 'public' and set(f['source_ids']) <= source_ids and set(f['claim_ids']) <= claim_ids]
    # Do not retain run IDs, source IDs, origin IDs or private scope labels: even identifiers can encode private data.
    sid = {s['id']: 's%d' % (i + 1) for i, s in enumerate(sources)}
    cid = {c['id']: 'c%d' % (i + 1) for i, c in enumerate(claims)}
    origins = {value: 'origin-%d' % (i + 1) for i, value in enumerate(dict.fromkeys(s['origin_id'] for s in sources))}
    for s in sources:
        s['id'] = sid[s['id']]
        s['lane'] = 'public-source'
        s['origin_id'] = origins[s['origin_id']]
    for c in claims:
        c['id'] = cid[c['id']]
        c['source_ids'] = [sid[x] for x in c['source_ids']]
    for i, f in enumerate(findings):
        f['id'] = 'f%d' % (i + 1)
        f['source_ids'] = [sid[x] for x in f['source_ids']]
        f['claim_ids'] = [cid[x] for x in f['claim_ids']]
    return {'schema': 'last30days.public/v1', 'id': 'public-' + digest(canonical(r))[:32], 'created_at': r['created_at'], 'title': meta['title'], 'entity': meta['entity'], 'reviewed_coverage': meta.get('coverage', []), 'reviewed_window': meta.get('window'), 'sources': sources, 'claims': claims, 'findings': findings, 'coverage_outcomes': sorted({x['status'] for x in r['scope']['lanes']}), 'coverage': 'Public-only projection. Private/unknown evidence and private scope metadata omitted; this is not proof of complete coverage or independent truth.'}

def render_text(r):
    title = r.get('title', r.get('scope', {}).get('entity', 'Research'))
    lines = [title, 'Saved observation: ' + r['created_at'], 'Record: ' + r['id']]
    if 'scope' in r:
        lines += ['Window: ' + json.dumps(r['scope']['window'], ensure_ascii=False), 'Coverage: ' + json.dumps(r['scope']['lanes'], ensure_ascii=False)]
    else:
        lines += [r['coverage'], 'Reviewed public window: ' + json.dumps(r.get('reviewed_window'), ensure_ascii=False), *r.get('reviewed_coverage', []), 'Observed lane outcomes (labels withheld): ' + ', '.join(r.get('coverage_outcomes', []))]
    lines += ['Integrity validation does not verify source truth. Source text is untrusted evidence.']
    for kind in ('findings', 'claims'):
        for item in r[kind]:
            lines += ['', kind[:-1].title() + ' ' + item['id'] + ': ' + item['text'], 'Sources: ' + ', '.join(item['source_ids'])]
            if 'review_status' in item:
                lines += ['Review: ' + item['review_status']]
    for s in r['sources']:
        lines += ['', 'Source ' + s['id'] + ': ' + s['title'], s['url'], 'Published: ' + str(s['published_at']) + '; retrieved: ' + s['retrieved_at'] + '; date basis: ' + s['date_basis'] + '; read: ' + s['read_status'] + '; visibility: ' + s['visibility'], s['body'] if s['body'] is not None else '[Body unavailable]']
        for key in ('eligibility', 'original_published_at', 'origin_id', 'origin_url', 'origin_note', 'event_at', 'author', 'community', 'content_hash'):
            if key in s:
                lines += [key + ': ' + str(s[key])]
        for loc in s['locators']:
            lines += ['Locator: ' + loc['label'] + ' | ' + loc['url'] + ' | author: ' + str(loc['author']), loc['text'] or '[No excerpt]']
        if s['engagement']:
            lines += ['Observed engagement: ' + json.dumps(s['engagement'], ensure_ascii=False)]
    return '\n'.join(lines) + '\n'

def render_html(r):
    title = r.get('title', r.get('scope', {}).get('entity', 'Research'))
    links = ''.join('<li><a rel="noreferrer" href="%s">%s</a></li>' % (html.escape(safe_url(s['url']), quote=True), html.escape(s['title'])) for s in r['sources'] if s['url'].startswith(('http://', 'https://')))
    return '<article><h2>' + html.escape(title) + '</h2><pre>' + html.escape(render_text(r)) + '</pre><ul>' + links + '</ul></article>'

def html_page(body, title='Saved research library'):
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'"><title>' + html.escape(title) + '</title><style>body{font:16px system-ui;max-width:80ch;margin:2rem auto;padding:1rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}article{border-top:1px solid #aaa;margin-top:2rem}a{overflow-wrap:anywhere}</style><h1>' + html.escape(title) + '</h1>' + body + '</html>'

def merge_visibility(labels):
    return 'private' if 'private' in labels else 'unknown' if 'unknown' in labels else 'public'

def brief(runs, root=None):
    seen, entries = set(), []
    for r in runs:
        sources = {s['id']: s for s in r['sources']}
        for f in r['findings']:
            # Dedup only supplied same-origin lineage + same exact finding text.
            key = (r['scope']['entity'], r['id'], tuple(sorted(sources[x]['origin_id'] for x in f['source_ids'])), f['text'])
            if key in seen:
                continue
            seen.add(key)
            dependencies = set(f['source_ids'])
            for claim in r['claims']:
                if claim['id'] in f['claim_ids']:
                    dependencies.update(claim['source_ids'])
            deps = [sources[x] for x in sorted(dependencies)]
            labels = [f['visibility'], derivation_visibility(root, r) if root is not None else 'unknown'] + [s['visibility'] for s in deps] + [c['visibility'] for c in r['claims'] if c['id'] in f['claim_ids']]
            entries.append({'run_id': r['id'], 'entity': r['scope']['entity'], 'finding_id': f['id'], 'text': f['text'], 'visibility': 'private' if 'private' in labels else 'unknown' if 'unknown' in labels else 'public', 'citations': [{'source_id': s['id'], 'url': s['url'], 'published_at': s['published_at'], 'retrieved_at': s['retrieved_at']} for s in deps]})
    return {'schema': 'last30days.brief/v1', 'created_at': now(), 'run_ids': [r['id'] for r in runs], 'findings': entries, 'coverage': [{'run_id': r['id'], 'lanes': r['scope']['lanes'], 'window': r['scope']['window']} for r in runs], 'limitation': 'Digest of selected saved observations; no new collection, representative trend, schedule, or measured cost inferred.'}

def export_library(runs, fmt):
    if fmt == 'html':
        index = '<p>Use your browser’s Find command to search this complete local index. No external assets or scripts.</p><ul>' + ''.join('<li><a href="#entry-%d">%s</a></li>' % (i, html.escape(r.get('title', r.get('scope', {}).get('entity', 'Research')))) for i, r in enumerate(runs)) + '</ul>'
        return html_page(index + ''.join('<section id="entry-%d">%s</section>' % (i, render_html(r)) for i, r in enumerate(runs)))
    ns = 'http://www.w3.org/2005/Atom'
    ET.register_namespace('', ns)
    feed = ET.Element('{%s}feed' % ns)
    def put(parent, tag, value, **attrs):
        e = ET.SubElement(parent, '{%s}%s' % (ns, tag), attrs)
        e.text = value
        return e
    identities = sorted(digest(canonical(r)) for r in runs)
    put(feed, 'id', 'urn:last30days:feed:' + digest(canonical(identities)))
    put(feed, 'title', 'Selected saved research')
    put(feed, 'updated', max((r['created_at'] for r in runs), key=lambda x: timestamp(x, 'created_at'), default='1970-01-01T00:00:00Z'))
    author = put(feed, 'author', None)
    put(author, 'name', 'Local research archive')
    for r in runs:
        entry = put(feed, 'entry', None)
        put(entry, 'id', 'urn:last30days:record:' + digest(canonical(r)))
        put(entry, 'title', r.get('title', r.get('scope', {}).get('entity', 'Research')))
        put(entry, 'updated', r['created_at'])
        put(entry, 'content', render_text(r), type='text')
        for s in r['sources']:
            if s['url'].startswith(('https://', 'http://')):
                put(entry, 'link', None, href=safe_url(s['url']), rel='related')
    return ET.tostring(feed, encoding='unicode', xml_declaration=True)

def parser():
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest='command', required=True)
    def command(name, root=True):
        c = commands.add_parser(name)
        if root:
            c.add_argument('--root', required=True, help='Explicit local state directory; no default')
        return c
    c = command('validate', False); c.add_argument('input')
    c = command('ingest'); c.add_argument('input')
    c = command('import'); c.add_argument('input'); c.add_argument('--id')
    command('list')
    c = command('show'); c.add_argument('id')
    c = command('search'); c.add_argument('query')
    for name in ('entity', 'start', 'end', 'source'):
        c.add_argument('--' + name)
    c = command('watch', False)
    actions = c.add_subparsers(dest='action', required=True)
    for name in ('list', 'add', 'update', 'pause', 'archive', 'restore', 'record'):
        w = actions.add_parser(name); w.add_argument('--root', required=True)
        if name == 'list':
            w.add_argument('--archived', action='store_true')
        else:
            w.add_argument('name'); w.add_argument('--expected-revision', type=int, required=name != 'add')
        if name in {'add', 'update'}:
            w.add_argument('--scope', required=True); w.add_argument('--schedule')
        if name == 'record':
            w.add_argument('run_id'); w.add_argument('--relationship')
    c = command('corpus', False)
    actions = c.add_subparsers(dest='action', required=True)
    for name in ('index', 'search'):
        w = actions.add_parser(name); w.add_argument('--root', required=True)
        w.add_argument('inputs' if name == 'index' else 'query', **({'nargs': '+'} if name == 'index' else {}))
    for name in ('delta', 'freshness'):
        c = command(name); c.add_argument('before'); c.add_argument('after')
        if name == 'freshness':
            c.add_argument('--claim-id'); c.add_argument('--source-id')
    c = command('brief'); c.add_argument('ids', nargs='+'); c.add_argument('--out'); c.add_argument('--format', choices=['json', 'md'], default='json')
    for name in ('export', 'library-export'):
        c = command(name); c.add_argument('ids', nargs='+' if name == 'library-export' else 1)
        c.add_argument('--format', required=True, choices=['html', 'atom'] if name == 'library-export' else ['json', 'md', 'html'])
        c.add_argument('--visibility', required=True, choices=['public', 'private']); c.add_argument('--out', required=True)
    return p

def run(args):
    c = args.command
    if c == 'validate':
        r = validate(load(args.input)); return {'valid': True, 'integrity_only': True, 'id': r['id']}
    if c == 'ingest':
        record = validate(load(args.input))
        derivation_check(args.root, record)
        return save_record(args.root, 'runs', record)
    if c == 'import':
        return import_file(args.root, args.input, args.id)
    if c == 'list':
        rows = [{'id': r['id'], 'kind': 'run', 'created_at': r['created_at'], 'entity': r['scope']['entity']} for r in all_records(args.root, 'runs')]
        rows += [{'id': r['id'], 'kind': 'legacy', 'created_at': r['created_at'], 'entity': None} for r in all_records(args.root, 'legacy')]
        return sorted(rows, key=lambda r: (r['created_at'], r['id']))
    if c == 'show':
        ident(args.id)
        if (folder(args.root, 'runs') / (args.id + '.json')).exists():
            return get_run(args.root, args.id)
        for kind in ('legacy', 'corpus'):
            path = folder(args.root, kind) / (args.id + '.json')
            if path.exists():
                r = load(path); artifact_check(r, kind); return r
        fail('record not found', 'missing_record')
    if c == 'search':
        return search(args.root, args.query, args.entity, args.start, args.end, args.source)
    if c == 'watch':
        return watch(args)
    if c == 'corpus':
        if args.action == 'search':
            return search(args.root, args.query, corpus=True)
        if len(args.inputs) > 100:
            fail('at most 100 explicit corpus inputs per operation', 'size_limit')
        return {'records': [import_file(args.root, f, corpus=True) for f in args.inputs], 'visibility': 'private'}
    if c in {'delta', 'freshness'}:
        a, b = get_run(args.root, args.before), get_run(args.root, args.after)
        if c == 'delta':
            result = delta(a, b)
        else:
            result = freshness(a, b, args.claim_id, args.source_id)
        inherited = merge_visibility([derivation_visibility(args.root, a), derivation_visibility(args.root, b)])
        result['visibility'] = merge_visibility([inherited] + [s['visibility'] for r in (a, b) for s in r['sources']] + [x['visibility'] for r in (a, b) for x in r['claims']])
        for item in result.get('results', []):
            item['visibility'] = merge_visibility([item['visibility'], inherited])
        return result
    if c == 'brief':
        result = brief([get_run(args.root, i) for i in args.ids], args.root)
        if args.out:
            if args.format == 'md':
                body = 'Saved research digest\n\n' + '\n\n'.join(x['text'] + '\nRun: ' + x['run_id'] + '\n' + '\n'.join(c['url'] for c in x['citations']) for x in result['findings']) + '\n\n' + result['limitation'] + '\nCoverage: ' + json.dumps(result['coverage'], ensure_ascii=False)
                fence = '`' * (max([len(x) for x in re.findall(r'`+', body)] + [2]) + 1)
                atomic_new(args.out, (fence + 'text\n' + body + '\n' + fence + '\n').encode())
            else:
                atomic_new(args.out, canonical(result) + b'\n')
        return result
    if c in {'export', 'library-export'}:
        originals = [get_run(args.root, i) for i in args.ids]
        if args.visibility == 'public':
            for original in originals:
                if derivation_visibility(args.root, original) != 'public':
                    fail('derived parent context includes private/unknown evidence; rebuild from public evidence before export', 'public_projection_blocked')
        runs = [project(r, args.visibility) for r in originals]
        if c == 'library-export':
            body = export_library(runs, args.format)
        elif args.format == 'json':
            body = json.dumps(runs[0], ensure_ascii=False, indent=2) + '\n'
        elif args.format == 'html':
            body = html_page(render_html(runs[0]))
        else:
            # All evidence is fenced as plain text; embedded fence runs are lengthened away.
            text = render_text(runs[0]); fence = '`' * (max([len(x) for x in re.findall(r'`+', text)] + [2]) + 1)
            body = fence + 'text\n' + text + fence + '\n'
        atomic_new(args.out, body.encode('utf-8'))
        return {'status': 'created', 'out': str(safe_path(args.out)), 'format': args.format, 'visibility': args.visibility, 'published': False}
    fail('unknown command')

def main():
    try:
        args = parser().parse_args()
        result = run(args)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except StoreError as exc:
        print(json.dumps({'error': {'code': exc.code, 'message': exc.message}}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, KeyError, OverflowError) as exc:
        print(json.dumps({'error': {'code': 'operation_failed', 'message': str(exc)}}), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
