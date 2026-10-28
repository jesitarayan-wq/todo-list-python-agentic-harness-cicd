import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_handoff_deterministic import validate

SCHEMA = {"required": ["task_id", "summary", "owner"]}


def test_holdout_basic_handoff():
    document = {"task_id": "T-1001", "summary": "Add retry logic", "owner": "planner"}
    assert validate(document, SCHEMA) == []


def test_holdout_handoff_with_long_summary():
    document = {"task_id": "T-1002", "summary": "x" * 500, "owner": "reviewer"}
    assert validate(document, SCHEMA) == []


def test_holdout_handoff_with_numeric_owner_id_as_string():
    document = {"task_id": "T-1003", "summary": "Fix flaky test", "owner": "tester"}
    assert validate(document, SCHEMA) == []


def test_extra_fields_are_allowed():
    document = {
        "task_id": "T-1004",
        "summary": "Refactor parser",
        "owner": "implementer",
        "priority": "high",
    }
    assert validate(document, SCHEMA) == []


def test_empty_required_field_is_rejected():
    document = {"task_id": "T-1005", "summary": "", "owner": "planner"}
    problems = validate(document, SCHEMA)
    assert "required field is empty: summary" in problems


def test_whitespace_required_field_is_rejected():
    document = {"task_id": "T-1005", "summary": "   ", "owner": "planner"}
    problems = validate(document, SCHEMA)
    assert "required field is empty: summary" in problems


def test_missing_required_field_is_rejected():
    document = {"task_id": "T-1006", "owner": "reviewer"}
    problems = validate(document, SCHEMA)
    assert "missing required field: summary" in problems


# ---- Tests for this project's handoff schema (implementer handoff) ----
import json

PROJECT_SCHEMA = json.loads(
    (Path(__file__).resolve().parent.parent / "schemas" / "handoff.json").read_text(encoding="utf-8")
)


def _handoff(**overrides):
    doc = {
        "task_id": "HO-02",
        "role": "implementer",
        "summary": "Add ObjectId validation to GET /tasks/<pk>",
        "modified_files": [{"path": "todo.py", "description": "return 400 on invalid ObjectId"}],
    }
    doc.update(overrides)
    return doc


def test_project_handoff_ho02_valid():
    assert validate(_handoff(), PROJECT_SCHEMA) == []


def test_project_handoff_ho04_two_files_valid():
    doc = _handoff(task_id="HO-04", modified_files=[
        {"path": "task.py", "description": "implement TaskDAO.update"},
        {"path": "todo.py", "description": "implement PUT route"}])
    assert validate(doc, PROJECT_SCHEMA) == []


def test_project_handoff_ho07_with_lesson_id_valid():
    doc = _handoff(task_id="HO-07", lesson_entry_id="lesson-001")
    assert validate(doc, PROJECT_SCHEMA) == []


def test_project_empty_description_rejected():
    doc = _handoff(modified_files=[{"path": "todo.py", "description": ""}])
    assert "modified_files[0] missing or empty: description" in validate(doc, PROJECT_SCHEMA)


def test_project_whitespace_description_rejected():
    doc = _handoff(modified_files=[{"path": "todo.py", "description": "   "}])
    assert "modified_files[0] missing or empty: description" in validate(doc, PROJECT_SCHEMA)


def test_project_empty_file_list_rejected():
    assert "modified_files must be a non-empty list" in validate(_handoff(modified_files=[]), PROJECT_SCHEMA)


def test_project_missing_file_list_rejected():
    doc = _handoff()
    del doc["modified_files"]
    assert "missing required field: modified_files" in validate(doc, PROJECT_SCHEMA)


def test_project_missing_path_rejected():
    doc = _handoff(modified_files=[{"description": "change"}])
    assert "modified_files[0] missing or empty: path" in validate(doc, PROJECT_SCHEMA)
