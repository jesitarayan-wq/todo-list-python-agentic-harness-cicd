diff --git a/.memory/project/MEMORY_INDEX.md b/.memory/project/MEMORY_INDEX.md
index 499c603..fa44f2b 100644
--- a/.memory/project/MEMORY_INDEX.md
+++ b/.memory/project/MEMORY_INDEX.md
@@ -1,6 +1,6 @@
 # Project Memory Index
 
-Last updated: 2026-10-01 (decision-003 reconfirmed, review date extended)
+Last updated: 2026-10-19 (decision-004 updated: update()/PUT implemented)
 
 ## Active entries
 
@@ -13,7 +13,7 @@ Last updated: 2026-10-01 (decision-003 reconfirmed, review date extended)
 - `decisions/decision-003.md` — Records adding root-level `pytest.ini` with `pythonpath = .` so tests in `/tests` can import `task`/`todo` under plain `pytest` invocation, not just `python -m pytest`. Recorded 2026-09-29, reconfirmed 2026-10-01.
  Review by 2026-12-30.
 
-- `decisions/decision-004.md` — Records that the priority feature (storage, defaulting, validation) is functionally complete across task.py/todo.py and both test files; backfill and update()/PUT remain deferred (not implemented, not formally scoped in decision-001). Recorded 2026-09-29.
+- `decisions/decision-004.md` — Records that the priority feature (storage, defaulting, validation) is functionally complete across task.py/todo.py and both test files; update()/PUT implemented 2026-10-19 (partial updates, route-level validation); backfill remains deferred. Recorded 2026-09-29, updated 2026-10-19.
  Review by 2026-12-28.
 
 - `../knowledge/coding-standards.md` — Coding standards
diff --git a/.memory/project/decisions/decision-004.md b/.memory/project/decisions/decision-004.md
index 0e251d6..9299fb6 100644
--- a/.memory/project/decisions/decision-004.md
+++ b/.memory/project/decisions/decision-004.md
@@ -1,6 +1,7 @@
 # Decision 004 - Priority Feature Functionally Complete
 
 **Date:** 2026-09-29
+**Updated:** 2026-10-19 (update()/PUT implemented)
 **Review by:** 2026-12-28
 **Status:** Active
 
@@ -10,8 +11,9 @@
 
 **Alternatives rejected:** N/A -- this is a status record, not a choice between alternatives.
 
-**Deferred (intentionally out of scope):**
+**Update 2026-10-19 -- implemented:** `TaskDAO.update(object_id, data)` and `PUT /tasks/<pk>` are now implemented and no longer deferred. Behavior: partial (PATCH-like) updates; only `title`, `description`, `priority`, `done` are whitelisted in the DAO; priority is not defaulted on update; validation lives in the route (non-empty title/description, priority in 1/2/3 excluding booleans and null, `done` must be bool, empty body/malformed id -> 400, unknown id -> 404). Covered by tests in `tests/test_task.py` and `tests/test_todo.py` (mongomock-backed).
+
+**Still deferred (intentionally out of scope):**
 - Backfilling `priority` onto existing documents created before this field existed.
-- Implementing `TaskDAO.update()` and the `PUT /tasks/<pk>` route (both currently `pass`/unimplemented), which would allow changing priority after creation.
 
-Note: [[decision-001]] itself only records the integer-vs-string storage rationale and does not explicitly discuss backfilling or `update()`/PUT -- these two items are deferred by omission (they were never implemented, and `TaskDAO.update()`/`PUT /tasks/<pk>` remain `pass`/no-op stubs in the current code), not by an explicit statement in decision-001. Neither is required for priority to function on creation, listing, and validation.
+Note: [[decision-001]] itself only records the integer-vs-string storage rationale and does not explicitly discuss backfilling; backfill is deferred by omission, not by an explicit statement in decision-001. It is not required for priority to function on creation, listing, updating, and validation.
diff --git a/task.py b/task.py
index ea14581..1ad31ff 100644
--- a/task.py
+++ b/task.py
@@ -6,6 +6,7 @@ from bson.objectid import ObjectId
 
 PRIORITIES = (1, 2, 3)
 DEFAULT_PRIORITY = 2
+UPDATABLE_FIELDS = ('title', 'description', 'priority', 'done')
 
 
 class TaskDAO:
@@ -38,8 +39,17 @@ class TaskDAO:
         task = self.task_collection.find_one({ '_id': ObjectId(object_id)})
         return self.to_json(task)
 
-    def update(self):
-        pass
+    def update(self, object_id, data):
+        # Only whitelisted fields present in data are set; no defaulting here.
+        fields = {key: data[key] for key in UPDATABLE_FIELDS if key in data}
+
+        if fields:
+            self.task_collection.update_one(
+                {'_id': ObjectId(object_id)},
+                {'$set': fields}
+            )
+
+        return self.read(object_id)
 
     def delete(self):
         pass
diff --git a/tests/test_task.py b/tests/test_task.py
index 82a78da..a750002 100644
--- a/tests/test_task.py
+++ b/tests/test_task.py
@@ -117,3 +117,89 @@ def test_list_sorts_by_done_before_priority(dao):
     tasks = dao.list()
 
     assert [task['title'] for task in tasks] == ['Undone Low Task', 'Done High Task']
+
+
+def _create_task(dao):
+    return dao.create({'title': 'Old Title', 'description': 'Old Description', 'priority': 1})
+
+
+def test_update_changes_title(dao):
+    created = _create_task(dao)
+
+    task = dao.update(created['_id']['$oid'], {'title': 'New Title'})
+
+    assert task['title'] == 'New Title'
+
+
+def test_update_changes_description(dao):
+    created = _create_task(dao)
+
+    task = dao.update(created['_id']['$oid'], {'description': 'New Description'})
+
+    assert task['description'] == 'New Description'
+
+
+def test_update_changes_priority(dao):
+    created = _create_task(dao)
+
+    task = dao.update(created['_id']['$oid'], {'priority': 3})
+
+    assert task['priority'] == 3
+
+
+def test_update_changes_done(dao):
+    created = _create_task(dao)
+
+    task = dao.update(created['_id']['$oid'], {'done': True})
+
+    assert task['done'] is True
+
+
+def test_update_partial_leaves_other_fields_untouched(dao):
+    created = _create_task(dao)
+
+    task = dao.update(created['_id']['$oid'], {'title': 'New Title'})
+
+    assert task['description'] == 'Old Description'
+    assert task['priority'] == 1
+    assert task['done'] is False
+
+
+def test_update_does_not_reset_priority_to_default_when_omitted(dao):
+    created = _create_task(dao)
+
+    task = dao.update(created['_id']['$oid'], {'description': 'New Description'})
+
+    assert task['priority'] == 1
+
+
+def test_update_ignores_non_whitelisted_keys(dao):
+    created = _create_task(dao)
+    original_id = created['_id']['$oid']
+
+    task = dao.update(original_id, {
+        '_id': '5f9f1b9b9b9b9b9b9b9b9b9b',
+        'foo': 'bar',
+        'title': 'New Title'
+    })
+
+    assert task['_id']['$oid'] == original_id
+    assert 'foo' not in task
+    assert task['title'] == 'New Title'
+
+
+def test_update_returns_none_for_unknown_id(dao):
+    task = dao.update('5f9f1b9b9b9b9b9b9b9b9b9b', {'title': 'New Title'})
+
+    assert task is None
+
+
+def test_update_persists_changes(dao):
+    created = _create_task(dao)
+    object_id = created['_id']['$oid']
+
+    dao.update(object_id, {'title': 'New Title', 'done': True})
+    task = dao.read(object_id)
+
+    assert task['title'] == 'New Title'
+    assert task['done'] is True
diff --git a/tests/test_todo.py b/tests/test_todo.py
index 3c13ab7..6e22413 100644
--- a/tests/test_todo.py
+++ b/tests/test_todo.py
@@ -1,5 +1,12 @@
 # coding=utf-8
+import json
+
+import mongomock
+import pytest
+
+import todo
 from todo import app
+from task import TaskDAO
 
 
 def test_list_tasks_must_return_status_200():
@@ -216,3 +223,96 @@ def test_retrieve_task_with_pk_must_returns_task():
         response = client.get('/tasks/%s' % inserted_id)
         data = json.loads(response.data.decode('utf-8'))
         assert data['_id']['$oid'] == inserted_id
+
+
+# --- PUT /tasks/<pk> (uses a mongomock-backed DAO, no live database) ---
+
+UNKNOWN_ID = '5f9f1b9b9b9b9b9b9b9b9b9b'
+
+
+@pytest.fixture
+def mock_dao(monkeypatch):
+    dao = TaskDAO(mongomock.MongoClient().todo_list)
+    monkeypatch.setattr(todo, 'tasks_dao', dao)
+    return dao
+
+
+@pytest.fixture
+def task_id(mock_dao):
+    task = mock_dao.create({
+        'title': 'Old Title',
+        'description': 'Old Description',
+        'priority': 1
+    })
+    return task['_id']['$oid']
+
+
+def _put(pk, payload):
+    with app.test_client() as client:
+        return client.put(
+            '/tasks/%s' % pk,
+            data=json.dumps(payload),
+            content_type='application/json'
+        )
+
+
+def test_update_task_returns_200_and_updated_task(task_id):
+    response = _put(task_id, {'title': 'New Title', 'priority': 3, 'done': True})
+
+    assert response.status_code == 200
+    data = json.loads(response.data.decode('utf-8'))
+    assert data['_id']['$oid'] == task_id
+    assert data['title'] == 'New Title'
+    assert data['description'] == 'Old Description'
+    assert data['priority'] == 3
+    assert data['done'] is True
+
+
+def test_update_task_with_unknown_id_must_returns_404(mock_dao):
+    response = _put(UNKNOWN_ID, {'title': 'New Title'})
+
+    assert response.status_code == 404
+
+
+def test_update_task_with_malformed_id_must_returns_400(mock_dao):
+    response = _put('not-an-object-id', {'title': 'New Title'})
+
+    assert response.status_code == 400
+
+
+def test_update_task_with_out_of_range_priority_must_returns_400(task_id):
+    assert _put(task_id, {'priority': 4}).status_code == 400
+
+
+def test_update_task_with_non_numeric_priority_must_returns_400(task_id):
+    assert _put(task_id, {'priority': 'high'}).status_code == 400
+
+
+def test_update_task_with_boolean_priority_must_returns_400(task_id):
+    assert _put(task_id, {'priority': True}).status_code == 400
+
+
+def test_update_task_with_null_priority_must_returns_400(task_id):
+    assert _put(task_id, {'priority': None}).status_code == 400
+
+
+def test_update_task_with_empty_title_must_returns_400(task_id):
+    assert _put(task_id, {'title': ''}).status_code == 400
+
+
+def test_update_task_with_empty_description_must_returns_400(task_id):
+    assert _put(task_id, {'description': ''}).status_code == 400
+
+
+def test_update_task_with_non_boolean_done_must_returns_400(task_id):
+    assert _put(task_id, {'done': 'yes'}).status_code == 400
+
+
+def test_update_task_with_empty_body_must_returns_400(task_id):
+    assert _put(task_id, {}).status_code == 400
+
+
+def test_update_task_with_invalid_changes_leaves_task_unchanged(mock_dao, task_id):
+    _put(task_id, {'title': 'New Title', 'priority': 4})
+
+    assert mock_dao.read(task_id)['title'] == 'Old Title'
diff --git a/todo.py b/todo.py
index 8779666..96eb892 100644
--- a/todo.py
+++ b/todo.py
@@ -1,5 +1,6 @@
 # coding=utf-8
 from flask import Flask, jsonify, request, abort
+from bson.objectid import ObjectId
 from task import TaskDAO, PRIORITIES
 import pymongo
 
@@ -19,6 +20,37 @@ def get(pk):
     if request.method == 'GET':
         return jsonify(tasks_dao.read(pk))
 
+    if request.method == 'PUT':
+        if not ObjectId.is_valid(pk):
+            return "The task id is invalid", 400
+
+        data = request.get_json(silent=True)
+
+        if not isinstance(data, dict):
+            return "A JSON object body is required", 400
+
+        for field in ('title', 'description'):
+            if field in data and (not isinstance(data[field], str) or not data[field]):
+                return "The field '%s' must be a non-empty string" % field, 400
+
+        if 'priority' in data:
+            priority = data['priority']
+            if isinstance(priority, bool) or priority not in PRIORITIES:
+                return "The field 'priority' must be 1 (high), 2 (medium) or 3 (low)", 400
+
+        if 'done' in data and not isinstance(data['done'], bool):
+            return "The field 'done' must be true or false", 400
+
+        if not any(key in data for key in ('title', 'description', 'priority', 'done')):
+            return "At least one of 'title', 'description', 'priority' or 'done' is required", 400
+
+        task = tasks_dao.update(pk, data)
+
+        if task is None:
+            return "Task not found", 404
+
+        return jsonify(task), 200
+
 
 @app.route('/tasks', methods=['POST'])
 def create():
