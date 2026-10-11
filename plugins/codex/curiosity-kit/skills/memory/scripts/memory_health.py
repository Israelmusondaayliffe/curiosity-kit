#!/usr/bin/env python3
"""Read-only prerequisite checks. Never certifies capture, injection, or MCP tools."""
import argparse
from contextlib import closing
import http.client
import json
import os
from pathlib import Path
import sqlite3
import sys
import tomllib

TABLES = ('sdk_sessions', 'observations', 'user_prompts', 'session_summaries',
          'tool_uses', 'work_state_entries')
SETTING_KEYS = ('CLAUDE_MEM_RUNTIME', 'CLAUDE_MEM_PROVIDER', 'CLAUDE_MEM_MODEL',
                'CLAUDE_MEM_WORKER_PORT')
LIMITS = ['Readiness covers only the requested prerequisite checks.',
          'MCP tools, capture, injection, and fresh-session behavior are unverified.',
          'Stored row counts are historical, not evidence of fresh capture.']


def load_object(path, toml=False):
    with path.open('rb') as stream:
        value = tomllib.load(stream) if toml else json.load(stream)
    if not isinstance(value, dict):
        raise ValueError('Expected a configuration object')
    return value


def probe(port, route):
    if route not in ('/api/health', '/api/version'):
        return 'unknown', {'reason': 'Unsupported diagnostic route'}
    # http.client never follows redirects; neither host nor route comes from config.
    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=2)
    try:
        connection.request('GET', route)
        response = connection.getresponse()
        if response.status != 200:
            return 'fail', {'http_status': response.status}
        body = response.read(65537)
        if len(body) > 65536:
            return 'unknown', {'reason': 'Response exceeds the diagnostic size limit'}
        value = json.loads(body)
        if not isinstance(value, dict):
            return 'unknown', {'reason': 'Expected a JSON object'}
        # Do not echo arbitrary health bodies, nested values, or error contents.
        safe = {key: value[key] for key in ('health', 'status', 'version')
                if isinstance(value.get(key), (str, int, float, bool))}
        if route == '/api/health':
            status = value.get('status', value.get('health'))
            if status is True or status in ('ok', 'healthy'):
                return 'pass', safe
            if status is False or status in ('error', 'failed', 'unhealthy'):
                return 'fail', safe
            return 'unknown', safe
        return ('pass' if isinstance(value.get('version'), str) and value['version']
                else 'unknown'), safe
    except (OSError, http.client.HTTPException):
        return 'fail', {'reason': 'Local endpoint unavailable'}
    except (ValueError, UnicodeError):
        return 'unknown', {'reason': 'Local endpoint returned invalid JSON'}
    finally:
        connection.close()


def database_check(path):
    if not path.is_file():
        return 'fail', {'reason': 'Existing database not found; nothing created'}
    try:
        with path.open('rb') as stream:
            header = stream.read(100)
        if header[:16] != b'SQLite format 3\x00':
            return 'fail', {'reason': 'Not a SQLite database'}
        if header[18:20] != b'\x01\x01' or any(
                Path(str(path) + suffix).exists() for suffix in ('-wal', '-shm', '-journal')):
            return 'unknown', {'reason': 'WAL or journal state cannot be inspected safely without possible sidecar changes'}
        uri = path.resolve().as_uri() + '?mode=ro'
        with closing(sqlite3.connect(uri, uri=True, timeout=1)) as database:
            database.execute('PRAGMA query_only=ON')
            names = {row[0] for row in database.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            missing = sorted(set(TABLES) - names)
            if missing:
                return 'fail', {'missing_tables': missing}
            counts = {name: database.execute('SELECT count(*) FROM "' + name + '"').fetchone()[0]
                      for name in TABLES}
        return 'pass', {'historical_counts': counts}
    except (OSError, sqlite3.Error):
        return 'unknown', {'reason': 'Database could not be inspected read-only'}


def diagnose(args):
    checks = []
    def add(name, status, **details):
        checks.append({'check': name, 'status': status, **details})

    config = Path(args.config).expanduser() if args.config else (
        Path.home() / ('.codex/config.toml' if args.platform == 'codex' else '.claude/settings.json'))
    plugin_id = args.plugin_id or ('claude-mem@claude-mem-local' if args.platform == 'codex'
                                   else 'claude-mem@thedotmack')
    try:
        host = load_object(config, toml=args.platform == 'codex')
        if args.platform == 'codex':
            plugins = host.get('plugins', {})
            plugin = plugins.get(plugin_id, {}) if isinstance(plugins, dict) else {}
            enabled = isinstance(plugin, dict) and plugin.get('enabled') is True
            features = host.get('features', {})
            hooks = isinstance(features, dict) and features.get('hooks') is True
            add('host_hooks', 'pass' if hooks else 'fail')
        else:
            plugins = host.get('enabledPlugins', {})
            enabled = isinstance(plugins, dict) and plugins.get(plugin_id) is True
        add('target_plugin', 'pass' if enabled else 'fail', plugin_id=plugin_id)
    except (OSError, ValueError, UnicodeError):
        add('host_config', 'unknown', reason='Host configuration missing, unreadable, or malformed')

    data_dir = Path(args.data_dir).expanduser()
    settings = {}
    try:
        settings = load_object(data_dir / 'settings.json')
        add('settings', 'pass')
    except (OSError, ValueError, UnicodeError):
        add('settings', 'unknown', reason='Settings missing, unreadable, or malformed')
    effective = {key: os.environ.get(key, settings.get(key)) for key in SETTING_KEYS}
    # Only selected non-credential settings are eligible for output.
    selected = {key: value for key, value in effective.items()
                if isinstance(value, (str, int, float, bool))}
    runtime = effective.get('CLAUDE_MEM_RUNTIME')
    if ('CLAUDE_MEM_RUNTIME' not in os.environ and 'CLAUDE_MEM_RUNTIME' not in settings) or runtime == '':
        runtime = 'worker'
    add('runtime', 'pass' if runtime == 'worker' else 'unknown',
        selected_settings=selected, reason=('Worker runtime' if runtime == 'worker'
                                           else 'Non-worker runtime is unsupported by this local diagnostic'))
    port_value = args.port if args.port is not None else effective.get('CLAUDE_MEM_WORKER_PORT')
    if port_value is None or port_value == '':
        port_value = 37700 + (os.getuid() % 100 if hasattr(os, 'getuid') else 0)
    try:
        if isinstance(port_value, bool) or not str(port_value).isdigit():
            raise ValueError()
        port = int(port_value)
        if not 1 <= port <= 65535:
            raise ValueError()
    except (ValueError, TypeError):
        port = None
        add('worker_port', 'unknown', reason='Invalid worker port')
    if runtime != 'worker':
        add('database', 'skipped', reason='Non-worker runtime')
        add('worker_health', 'skipped', reason='Non-worker runtime')
        add('worker_version', 'skipped', reason='Non-worker runtime')
    else:
        status, details = database_check(data_dir / 'claude-mem.db')
        add('database', status, **details)
        if args.skip_worker or port is None:
            add('worker_health', 'unknown', reason='Probe explicitly skipped' if args.skip_worker else 'Invalid port')
            add('worker_version', 'skipped', reason='Worker probe not performed')
        else:
            for name, route in (('worker_health', '/api/health'), ('worker_version', '/api/version')):
                status, details = probe(port, route)
                add(name, status, observed=details)
    statuses = {check['status'] for check in checks}
    code = 1 if 'fail' in statuses else 2 if statuses & {'unknown', 'skipped'} else 0
    return {'readiness': 'pass' if code == 0 else 'fail' if code == 1 else 'incomplete',
            'exit_code': code, 'platform': args.platform, 'checks': checks, 'scope_limits': LIMITS}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', required=True, choices=('claude', 'codex'))
    parser.add_argument('--data-dir', default=os.environ.get('CLAUDE_MEM_DATA_DIR', str(Path.home() / '.claude-mem')))
    parser.add_argument('--config', help='Explicit host config path (JSON for Claude; TOML for Codex)')
    parser.add_argument('--plugin-id', help='Exact plugin key when a different alias is intentionally installed')
    parser.add_argument('--port', help='Local worker port, overriding environment and settings')
    parser.add_argument('--skip-worker', action='store_true', help='Skip HTTP checks; readiness remains incomplete')
    parser.add_argument('--json', action='store_true')
    result = diagnose(parser.parse_args(argv))
    if '--json' in (sys.argv[1:] if argv is None else argv):
        print(json.dumps(result, indent=2))
    else:
        print('Readiness: ' + result['readiness'])
        for check in result['checks']:
            print(check['status'] + ': ' + check['check'] + ' ' + json.dumps({
                key: value for key, value in check.items() if key not in ('check', 'status')}))
        for limit in result['scope_limits']:
            print(limit)
    return result['exit_code']


if __name__ == '__main__':
    sys.exit(main())
