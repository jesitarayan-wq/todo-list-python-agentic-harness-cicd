"""Static checks of the network modes in scripts/run-agent.sh and the egress allow-list."""
import re
from pathlib import Path

_R = Path(__file__).resolve().parents[1]
SCRIPT = (_R / "scripts" / "run-agent.sh").read_text(encoding="utf-8")
START = (_R / "scripts" / "start-egress-proxy.sh").read_text(encoding="utf-8")
ALLOW = (_R / "config" / "egress-allow-list.txt").read_text(encoding="utf-8")


def test_open_mode_is_still_the_default():
    assert 'NETWORK_MODE="${AGENT_NETWORK:-open}"' in SCRIPT


def test_restricted_mode_uses_the_internal_network_and_the_proxy():
    assert "--network agent-internal" in SCRIPT
    assert "HTTPS_PROXY=http://egress-proxy:3128" in SCRIPT
    assert "NO_PROXY=localhost,127.0.0.1" in SCRIPT


def test_restricted_mode_refuses_to_start_without_the_proxy():
    assert "Restricted network mode needs the egress proxy" in SCRIPT
    assert "exit 1" in SCRIPT.split("restricted)")[1].split(";;")[0]


def test_only_open_mode_publishes_ports():
    open_block, rest = SCRIPT.split("restricted)", 1)
    assert "-p 8501:8501" in open_block
    assert "-p 8501" not in rest


def test_unknown_network_modes_are_rejected():
    assert "Unknown AGENT_NETWORK" in SCRIPT


def test_workspace_modes_by_role_are_unchanged():
    modes = {}
    for roles, mode in re.findall(r'^\s+([a-z\-|]+)\)\s*\n\s*WORKSPACE_MODE="(rw|ro)"', SCRIPT, re.M):
        for role in roles.split("|"):
            modes[role] = mode
    assert modes["implementer"] == "rw" and modes["orchestrator"] == "rw"
    for role in ["security-reviewer", "planner", "tester", "project-manager", "dependency-auditor", "test-coverage-analyzer"]:
        assert modes[role] == "ro"


def test_the_proxy_is_the_only_container_attached_to_both_networks():
    assert "network create --internal agent-internal" in START
    assert "docker network connect agent-internal egress-proxy" in START


def test_the_allow_list_is_specific():
    rules = [line.split("#", 1)[0].strip() for line in ALLOW.splitlines()]
    rules = [r for r in rules if r]
    assert "api.anthropic.com" in rules
    assert all(r not in {"*", "*.*", "*.com"} for r in rules)
