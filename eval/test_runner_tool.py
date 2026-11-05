"""Tests for the real test_runner tool in mcp/coursetools_server.py."""
import importlib.util
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("COURSETOOLS_ROOT", str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "coursetools_under_test", ROOT / "mcp" / "coursetools_server.py"
)
SERVER = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SERVER)


class _Result:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_tester_gets_a_real_pytest_result():
    out = SERVER.test_runner("tester")
    assert out.startswith("PASS (pytest exit code 0)")
    assert "passed" in out


def test_unknown_suite_is_refused():
    with pytest.raises(ValueError):
        SERVER.test_runner("tester", "other")


def test_other_roles_are_denied():
    for role in ["implementer", "planner", "security-reviewer", "orchestrator",
                 "project-manager", "dependency-auditor"]:
        with pytest.raises(PermissionError):
            SERVER.test_runner(role)


def test_failing_tests_are_reported_as_fail(monkeypatch):
    monkeypatch.setattr(SERVER.subprocess, "run", lambda *a, **k: _Result(1, "1 failed"))
    assert SERVER.test_runner("tester").startswith("FAIL (pytest exit code 1)")


def test_collection_error_is_never_reported_as_pass(monkeypatch):
    monkeypatch.setattr(SERVER.subprocess, "run", lambda *a, **k: _Result(2, "", "ModuleNotFoundError"))
    out = SERVER.test_runner("tester")
    assert out.startswith("NOT RUN")
    assert not out.startswith("PASS")


def test_timeout_is_not_run(monkeypatch):
    def boom(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="pytest", timeout=120)
    monkeypatch.setattr(SERVER.subprocess, "run", boom)
    assert SERVER.test_runner("tester").startswith("NOT RUN")


def test_missing_pytest_is_not_run(monkeypatch):
    def boom(*args, **kwargs):
        raise OSError("no such file")
    monkeypatch.setattr(SERVER.subprocess, "run", boom)
    assert SERVER.test_runner("tester").startswith("NOT RUN")
