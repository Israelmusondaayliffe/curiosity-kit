"""Focused provenance and existing package-validator regression checks."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import package


class ProvenanceTests(unittest.TestCase):
    def test_failed_status_is_unknown(self):
        replies = [subprocess.CompletedProcess([], 0, "abc123\n", ""),
                   subprocess.CompletedProcess([], 128, "", "status failed")]
        with patch.object(package.subprocess, "run", side_effect=replies):
            self.assertEqual(package.source_provenance(Path("unused")), ("abc123", None))

    def test_clean_and_dirty_status(self):
        for output, expected in [("", False), (" M example\n", True)]:
            replies = [subprocess.CompletedProcess([], 0, "abc123\n", ""),
                       subprocess.CompletedProcess([], 0, output, "")]
            with self.subTest(output=output), patch.object(package.subprocess, "run", side_effect=replies):
                self.assertEqual(package.source_provenance(Path("unused")), ("abc123", expected))

    def test_missing_git_is_unknown(self):
        with patch.object(package.subprocess, "run", side_effect=FileNotFoundError):
            self.assertEqual(package.source_provenance(Path("unused")), (None, None))

    def test_first_read_preserves_index_and_local_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)

            def git(*args):
                return subprocess.run(["git", "-c", "core.hooksPath=" + os.devnull,
                                       "-c", "user.name=Package Test", "-c", "user.email=test@example.invalid",
                                       "-C", str(repo), *args], check=True, capture_output=True, env=env)

            git("-c", "init.templateDir=", "init")
            tracked = repo / "tracked.txt"
            tracked.write_text("base\n")
            git("add", "tracked.txt")
            git("commit", "-m", "fixture")
            tracked.write_text("staged\n")
            git("add", "tracked.txt")
            tracked.write_text("unstaged\n")
            (repo / "untracked.txt").write_text("untracked\n")
            monitor = repo / "monitor.sh"
            monitor.write_text('#!/bin/sh\ntouch "' + str(repo / "monitor-ran") + '"\n')
            monitor.chmod(0o755)
            git("config", "core.fsmonitor", str(monitor))
            git("config", "core.untrackedCache", "true")
            before = {str(p.relative_to(repo)): p.read_bytes()
                      for p in repo.rglob("*") if p.is_file()}
            expected_revision = git("rev-parse", "HEAD").stdout.decode().strip()
            with patch.dict(os.environ, env):
                revision, dirty = package.source_provenance(repo)
            after = {str(p.relative_to(repo)): p.read_bytes()
                     for p in repo.rglob("*") if p.is_file()}
            self.assertEqual((revision, dirty), (expected_revision, True))
            self.assertEqual(before, after, "Git provenance changed fixture files, index or HEAD")
            self.assertFalse((repo / "monitor-ran").exists())


class PackageGateTests(unittest.TestCase):
    def test_existing_validator_controls_build_exit_status(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "source"
            for host in package.HOSTS:
                adapter = repo / "adapters" / host
                adapter.mkdir(parents=True)
                (adapter / "plugin.json").write_text(json.dumps({
                    "name": "curiosity-kit", "version": "0.1.0", "skills": "./skills/"}))
            (repo / "adapters" / "codex" / "skill-metadata.json").write_text(json.dumps({
                "sample": {"display_name": "Sample", "short_description": "A fixture",
                           "default_prompt": "Use sample", "allow_implicit_invocation": True}}))
            (repo / "LICENSE").write_text("Fixture license\n")
            skill = repo / "skills" / "sample"
            skill.mkdir(parents=True)
            entry = skill / "SKILL.md"
            valid = "---\nname: sample\ndescription: A fixture for package validation.\n---\n\nRead this method.\n"
            entry.write_text(valid)
            for body, expected in [(valid, 0), (valid + "[Required](references/missing.md)\n", 1)]:
                entry.write_text(body)
                out = Path(temp) / ("valid" if expected == 0 else "invalid")
                with patch.object(package, "REPO", repo), patch.object(package, "source_provenance", return_value=(None, None)), \
                     patch("sys.argv", ["package.py", "--out", str(out)]), patch("builtins.print"):
                    self.assertEqual(package.main(), expected)
                report = json.loads((out / "build-manifest.json").read_text())
                self.assertEqual(len(report["packages"]), 4)
                self.assertEqual({p["host"] for p in report["packages"]}, set(package.HOSTS))
                self.assertTrue(all(p["ok"] == (expected == 0) for p in report["packages"]))


if __name__ == "__main__":
    unittest.main()
