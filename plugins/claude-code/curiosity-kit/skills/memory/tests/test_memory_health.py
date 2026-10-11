"""Deterministic isolated fixtures; no engine, models, or live worker required."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'memory_health.py'
spec = importlib.util.spec_from_file_location('memory_health', SCRIPT)
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root / 'config.toml'
        self.config.write_text('[features]\nhooks = true\n[plugins."claude-mem@claude-mem-local"]\nenabled = true\n')
        (self.root / 'settings.json').write_text('{}')
        self.args = argparse.Namespace(platform='codex', config=str(self.config),
            plugin_id=None, data_dir=str(self.root), port=None, skip_worker=False, json=True)
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def make_db(self, missing=()):
        db = sqlite3.connect(self.root / 'claude-mem.db')
        for table in health.TABLES:
            if table not in missing:
                db.execute('CREATE TABLE ' + table + ' (id INTEGER, text TEXT)')
        db.commit()
        db.close()

    def run_check(self):
        with patch.object(health, 'probe', side_effect=[('pass', {'status': 'ok'}), ('pass', {'version': 'old'})]):
            return health.diagnose(self.args)

    def test_ready_fixture_not_capture_certification(self):
        self.make_db()
        result = self.run_check()
        self.assertEqual(result['exit_code'], 0)
        self.assertTrue(any('unverified' in text for text in result['scope_limits']))
        self.assertEqual(set(p.name for p in self.root.iterdir()), {'config.toml', 'settings.json', 'claude-mem.db'})

    def test_missing_db_never_created(self):
        self.assertEqual(self.run_check()['exit_code'], 1)
        self.assertFalse((self.root / 'claude-mem.db').exists())

    def test_unrelated_plugin_does_not_enable_target(self):
        self.make_db()
        self.config.write_text('[features]\nhooks=true\n[plugins."other"]\nenabled=true\n[plugins."claude-mem@claude-mem-local"]\nenabled=false\n')
        self.assertEqual(self.run_check()['exit_code'], 1)

    def test_commented_hooks_not_enabled(self):
        self.make_db()
        self.config.write_text('# hooks = true\n[plugins."claude-mem@claude-mem-local"]\nenabled=true\n')
        result = self.run_check()
        self.assertEqual(next(x['status'] for x in result['checks'] if x['check'] == 'host_hooks'), 'fail')

    def test_malformed_host_config_incomplete(self):
        self.make_db()
        self.config.write_text('not = valid TOML')
        self.assertEqual(self.run_check()['exit_code'], 2)

    def test_skip_worker_incomplete(self):
        self.make_db()
        self.args.skip_worker = True
        with patch.object(health, 'probe') as probe:
            self.assertEqual(health.diagnose(self.args)['exit_code'], 2)
            probe.assert_not_called()

    def test_version_never_substitutes_for_work_state_table(self):
        self.make_db(missing=('work_state_entries',))
        with patch.object(health, 'probe', return_value=('pass', {'version': '9999'})):
            result = health.diagnose(self.args)
        self.assertEqual(result['exit_code'], 1)
        self.assertEqual(next(x['missing_tables'] for x in result['checks'] if x['check'] == 'database'), ['work_state_entries'])

    def test_server_runtime_not_worker_failure(self):
        (self.root / 'settings.json').write_text('{"CLAUDE_MEM_RUNTIME":"server"}')
        with patch.object(health, 'probe') as probe:
            result = health.diagnose(self.args)
            probe.assert_not_called()
        self.assertEqual(result['exit_code'], 2)
        self.assertFalse((self.root / 'claude-mem.db').exists())

    def test_port_precedence(self):
        self.make_db()
        (self.root / 'settings.json').write_text('{"CLAUDE_MEM_WORKER_PORT":4001}')
        with patch.dict(os.environ, {'CLAUDE_MEM_WORKER_PORT': '4002'}):
            with patch.object(health, 'probe', return_value=('pass', {})) as probe:
                health.diagnose(self.args)
                self.assertEqual(probe.call_args_list[0].args[0], 4002)
                self.args.port = '4003'
                health.diagnose(self.args)
                self.assertEqual(probe.call_args.args[0], 4003)

    def test_invalid_port_incomplete_without_probe(self):
        self.make_db()
        self.args.port = 'https://outside.invalid'
        with patch.object(health, 'probe') as probe:
            self.assertEqual(health.diagnose(self.args)['exit_code'], 2)
            probe.assert_not_called()

    def test_malformed_settings_incomplete(self):
        self.make_db()
        (self.root / 'settings.json').write_text('[]')
        self.assertEqual(self.run_check()['exit_code'], 2)

    def test_explicit_invalid_runtime_never_defaults_to_worker(self):
        self.make_db()
        for value in (False, [], 0, None, {}, True):
            with self.subTest(runtime=value):
                (self.root / 'settings.json').write_text(json.dumps({'CLAUDE_MEM_RUNTIME': value}))
                with patch.object(health, 'probe') as probe:
                    self.assertEqual(health.diagnose(self.args)['exit_code'], 2)
                    probe.assert_not_called()

    def test_runtime_environment_overrides_settings(self):
        self.make_db()
        (self.root / 'settings.json').write_text('{"CLAUDE_MEM_RUNTIME":"server"}')
        with patch.dict(os.environ, {'CLAUDE_MEM_RUNTIME': 'worker'}):
            self.assertEqual(self.run_check()['exit_code'], 0)

    def test_claude_boolean_exactness(self):
        self.make_db()
        self.args.platform = 'claude'
        self.config.write_text('{"enabledPlugins":{"claude-mem@thedotmack":"true","other":true}}')
        self.assertEqual(self.run_check()['exit_code'], 1)
        self.config.write_text('{"enabledPlugins":{"claude-mem@thedotmack":true}}')
        self.assertEqual(self.run_check()['exit_code'], 0)

    def test_wal_unknown_no_sidecar_creation(self):
        self.make_db()
        db = sqlite3.connect(self.root / 'claude-mem.db')
        db.execute('PRAGMA journal_mode=WAL')
        db.close()
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(self.run_check()['exit_code'], 2)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_json_cli(self):
        self.make_db()
        with patch.object(health, 'probe', return_value=('pass', {'status': 'ok'})), contextlib.redirect_stdout(io.StringIO()) as output:
            code = health.main(['--platform', 'codex', '--config', str(self.config), '--data-dir', str(self.root), '--json'])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())['readiness'], 'pass')


class EndpointTests(unittest.TestCase):
    def test_health_redacts_payload(self):
        with patch.object(health.http.client, 'HTTPConnection') as factory:
            connection = factory.return_value
            response = connection.getresponse.return_value
            response.status = 200
            response.read.return_value = b'{"status":"ok","version":"1","api_key":"secret","memories":["private"]}'
            status, details = health.probe(37700, '/api/health')
        self.assertEqual(status, 'pass')
        self.assertEqual(details, {'status': 'ok', 'version': '1'})
        factory.assert_called_once_with('127.0.0.1', 37700, timeout=2)
        connection.request.assert_called_once_with('GET', '/api/health')

    def test_non_diagnostic_route_never_requested(self):
        with patch.object(health.http.client, 'HTTPConnection') as factory:
            status, _ = health.probe(37700, 'https://outside.invalid')
            factory.assert_not_called()
        self.assertEqual(status, 'unknown')

    def test_redirect_never_followed(self):
        with patch.object(health.http.client, 'HTTPConnection') as factory:
            connection = factory.return_value
            connection.getresponse.return_value.status = 302
            status, details = health.probe(37700, '/api/health')
        self.assertEqual(status, 'fail')
        self.assertEqual(details, {'http_status': 302})
        self.assertEqual(connection.request.call_count, 1)


if __name__ == '__main__':
    unittest.main()
