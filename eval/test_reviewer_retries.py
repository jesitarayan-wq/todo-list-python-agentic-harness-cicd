"""Tests for the retries and the per-run budget in scripts/run-reviewer.py."""
import importlib.util
import io
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("reviewer_under_test", ROOT / "scripts" / "run-reviewer.py")
REVIEWER = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(REVIEWER)


def http_error(code):
    return urllib.error.HTTPError("https://example.invalid", code, "error", {}, io.BytesIO(b"{}"))


class FakeSend:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def __call__(self, prompt, api_key, model):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


@pytest.fixture(autouse=True)
def fake_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")


def run(outcomes, **kwargs):
    send = FakeSend(outcomes)
    sleeps = []
    result = REVIEWER.call_with_retries("prompt", send=send, sleep=sleeps.append, **kwargs)
    return result, send, sleeps


def test_first_attempt_success_makes_one_call():
    result, send, sleeps = run(["ok"])
    assert result == "ok"
    assert send.calls == 1
    assert sleeps == []


def test_a_server_error_is_retried_and_recorded():
    result, send, sleeps = run([http_error(529), "ok"], backoff=2)
    assert "ok" in result
    assert "attempt 1 failed (HTTP 529)" in result
    assert "attempt 2 succeeded" in result
    assert send.calls == 2
    assert sleeps == [2]


def test_a_client_error_is_not_retried():
    result, send, sleeps = run([http_error(401), "ok"])
    assert send.calls == 1
    assert sleeps == []
    assert result.startswith("## Advisory Code Review")
    assert "attempt 1 failed (HTTP 401)" in result


def test_it_gives_up_after_the_maximum_number_of_attempts():
    result, send, sleeps = run([http_error(503), http_error(503), http_error(503)], max_attempts=3, backoff=2)
    assert send.calls == 3
    assert sleeps == [2, 4]
    assert "No review was produced" in result


def test_the_budget_stops_further_attempts():
    result, send, sleeps = run([http_error(503), "ok"], budget=1500, backoff=2)
    assert send.calls == 1
    assert "attempt 2 was not made" in result
    assert "budget" in result


def test_timeouts_and_network_errors_are_retried():
    result, send, sleeps = run([TimeoutError("slow"), urllib.error.URLError("down"), "ok"], backoff=1)
    assert "ok" in result
    assert send.calls == 3
    assert sleeps == [1, 2]


def test_no_key_means_no_call(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    send = FakeSend([])
    result = REVIEWER.call_with_retries("prompt", send=send, sleep=lambda s: None)
    assert "No review was performed" in result
    assert send.calls == 0


def test_which_errors_are_retryable():
    assert REVIEWER.is_retryable(http_error(429))
    assert REVIEWER.is_retryable(TimeoutError())
    assert not REVIEWER.is_retryable(http_error(404))
    assert not REVIEWER.is_retryable(ValueError("bad"))
