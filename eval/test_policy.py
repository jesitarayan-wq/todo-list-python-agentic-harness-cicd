from pathlib import Path
import re


ROOT = Path(".")


def test_governance_policy_exists():
    assert (ROOT / "docs" / "governance-policy.md").exists(), (
        "Missing docs/governance-policy.md"
    )


def test_ci_step_design_exists():
    assert (ROOT / "docs" / "ci-step-design.md").exists(), (
        "Missing docs/ci-step-design.md"
    )


def test_workflow_exists_at_repo_root():
    assert (ROOT / ".github" / "workflows" / "ci.yml").exists(), (
        "Workflow must live at .github/workflows/ci.yml"
    )


def test_workflow_does_not_hardcode_anthropic_key():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    forbidden_patterns = [
        r"sk-ant-[A-Za-z0-9_\-]+",
        r"ANTHROPIC_API_KEY\s*=\s*sk-",
    ]

    for pattern in forbidden_patterns:
        assert not re.search(pattern, workflow), (
            "Do not hardcode Anthropic keys in the workflow. "
            "Use ${{ secrets.ANTHROPIC_API_KEY }}."
        )


def test_policy_gate_is_not_continue_on_error():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    policy_section_start = workflow.find("policy-gate:")
    assert policy_section_start != -1, "Missing policy-gate job"

    next_job_start = workflow.find("\n  governed-file-gate:", policy_section_start)
    section = workflow[policy_section_start:next_job_start]

    assert "continue-on-error: true" not in section, (
        "policy-gate must remain a real gate, not advisory."
    )


# ---- Policy vs configuration checks (Module 4) ----
import json
import re
from pathlib import Path

import pytest

_R = Path(__file__).resolve().parent.parent
_POLICY = (_R / "docs" / "governance-policy.md").read_text(encoding="utf-8")
_SECTIONS = {}
for _m in re.finditer(r"^## Role: (\S+)\n(.*?)(?=^## Role: |\Z)", _POLICY, re.S | re.M):
    _SECTIONS[_m.group(1)] = _m.group(2)
ROLES = sorted(_SECTIONS)


def _policy_ops(role, server):
    rows = re.findall(r"^\| (\w+) \| " + server + r" \| (YES|NO) \|", _SECTIONS[role], re.M)
    return {op for op, g in rows if g == "YES"}


def _policy_skills_granted(role):
    block = re.search(r"### Skill activation scope(.*?)(?=^### |\Z)", _SECTIONS[role], re.S | re.M)
    granted = set()
    for names, g in re.findall(r"^\| ([^|]+) \| (YES|NO) \|", block.group(1), re.M):
        if g == "YES":
            granted |= {n.strip() for n in names.split(",")}
    return granted


STORAGE = json.loads((_R / "mcp-servers/storage/allow-list.json").read_text())
RETRIEVAL = json.loads((_R / "mcp-servers/retrieval/allow-list.json").read_text())["retrieve"]


@pytest.mark.parametrize("role", ROLES)
def test_storage_allowlist_matches_policy(role):
    from_json = {op for op, roles in STORAGE.items() if role in roles}
    assert from_json == _policy_ops(role, "storage"), (
        f"{role}: allow-list={sorted(from_json)} policy={sorted(_policy_ops(role, 'storage'))}")


@pytest.mark.parametrize("role", ROLES)
def test_no_storage_overgrant(role):
    extra = {op for op, roles in STORAGE.items() if role in roles} - _policy_ops(role, "storage")
    assert not extra, f"{role} holds operations the policy never gave it: {sorted(extra)}"


@pytest.mark.parametrize("role", ROLES)
def test_retrieval_allowlist_matches_policy(role):
    granted = bool(RETRIEVAL.get(role, {}).get("granted"))
    want = "retrieve" in _policy_ops(role, "retrieval")
    assert granted == want, f"{role}: allow-list granted={granted}, policy={want}"


@pytest.mark.parametrize("skill_file", sorted(list((_R / "skills").glob("*/SKILL.md")) + list((_R / ".claude" / "skills").glob("*/SKILL.md"))))
def test_skill_scope_matches_policy(skill_file):
    skill = skill_file.parent.name
    text = skill_file.read_text(encoding="utf-8")
    m = re.search(r"^Denied roles: (.+)$", text, re.M)
    assert m, f"{skill}: no 'Denied roles:' line in Activation Scope"
    denied = {r.strip() for r in m.group(1).split(",")}
    expected = {r for r in ROLES if skill not in _policy_skills_granted(r)}
    assert denied == expected, f"{skill}: skill file denies {sorted(denied)}, policy denies {sorted(expected)}"


def test_container_workspace_matches_policy():
    script = (_R / "scripts" / "run-agent.sh").read_text(encoding="utf-8")
    modes = {}
    for roles, mode in re.findall(r'^\s+([a-z\-|]+)\)\s*\n\s*WORKSPACE_MODE="(rw|ro)"', script, re.M):
        for r in roles.split("|"):
            modes[r] = mode
    for role in ROLES:
        line = re.search(r"\*\*Container permissions:\*\* workspace (read-write|read-only)", _SECTIONS[role])
        assert line, f"{role}: no Container permissions line in policy"
        want = "rw" if line.group(1) == "read-write" else "ro"
        assert modes.get(role) == want, f"{role}: script={modes.get(role)} policy={want}"
