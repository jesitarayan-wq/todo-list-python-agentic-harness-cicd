diff --git a/tests/test_task.py b/tests/test_task.py
index 82a78da..68d9b8c 100644
--- a/tests/test_task.py
+++ b/tests/test_task.py
@@ -37,6 +37,15 @@ def test_create_keeps_the_given_priority(dao):
     assert task['priority'] == 1
 
 
+def test_create_stores_integer_priority(dao):
+    dao.create({'title': 'The Best Title', 'description': 'The Best Description', 'priority': 3})
+
+    stored = dao.task_collection.find_one({'title': 'The Best Title'})
+    assert isinstance(stored['priority'], int)
+    assert not isinstance(stored['priority'], bool)
+    assert stored['priority'] == 3
+
+
 def test_create_returns_task_with_an_id(dao):
     task = dao.create({'title': 'The Best Title', 'description': 'The Best Description'})
 
diff --git a/tests/test_todo.py b/tests/test_todo.py
index 3c13ab7..eeef722 100644
--- a/tests/test_todo.py
+++ b/tests/test_todo.py
@@ -126,6 +126,88 @@ def test_create_task_with_given_priority_must_returns_that_priority():
         assert data['priority'] == 1
 
 
+def test_create_task_with_integer_priorities_must_still_work():
+    with app.test_client() as client:
+        import json
+        for value in (1, 2, 3):
+            response = client.post(
+                '/tasks',
+                data=json.dumps(
+                    {
+                        'title': 'The Best Title',
+                        'description': 'The Best Description',
+                        'priority': value
+                    }
+                ),
+                content_type='application/json'
+            )
+
+            assert response.status_code == 201
+            data = json.loads(response.data.decode('utf-8'))
+            assert data['priority'] == value
+
+
+def test_create_task_with_string_priority_must_returns_integer_priority():
+    with app.test_client() as client:
+        import json
+        for name, expected in (('high', 1), ('medium', 2), ('low', 3)):
+            response = client.post(
+                '/tasks',
+                data=json.dumps(
+                    {
+                        'title': 'The Best Title',
+                        'description': 'The Best Description',
+                        'priority': name
+                    }
+                ),
+                content_type='application/json'
+            )
+
+            assert response.status_code == 201
+            data = json.loads(response.data.decode('utf-8'))
+            assert data['priority'] == expected
+            assert isinstance(data['priority'], int)
+
+
+def test_create_task_with_string_priority_must_ignore_case_and_surrounding_whitespace():
+    with app.test_client() as client:
+        import json
+        for name, expected in (('HIGH', 1), (' low ', 3)):
+            response = client.post(
+                '/tasks',
+                data=json.dumps(
+                    {
+                        'title': 'The Best Title',
+                        'description': 'The Best Description',
+                        'priority': name
+                    }
+                ),
+                content_type='application/json'
+            )
+
+            assert response.status_code == 201
+            data = json.loads(response.data.decode('utf-8'))
+            assert data['priority'] == expected
+
+
+def test_create_task_with_unknown_string_priority_must_returns_400():
+    with app.test_client() as client:
+        import json
+        for name in ('urgent', '', '1'):
+            response = client.post(
+                '/tasks',
+                data=json.dumps(
+                    {
+                        'title': 'The Best Title',
+                        'description': 'The Best Description',
+                        'priority': name
+                    }
+                ),
+                content_type='application/json'
+            )
+            assert response.status_code == 400
+
+
 def test_create_task_with_out_of_range_priority_must_returns_400():
     with app.test_client() as client:
         import json
@@ -152,7 +234,7 @@ def test_create_task_with_non_numeric_priority_must_returns_400():
                 {
                     'title': 'The Best Title',
                     'description': 'The Best Description',
-                    'priority': 'high'
+                    'priority': 'urgent'
                 }
             ),
             content_type='application/json'
diff --git a/todo.py b/todo.py
index 8779666..73d6254 100644
--- a/todo.py
+++ b/todo.py
@@ -8,6 +8,8 @@ client = pymongo.MongoClient('mongodb://localhost')
 database = client.todo_list
 tasks_dao = TaskDAO(database)
 
+PRIORITY_NAMES = {'high': 1, 'medium': 2, 'low': 3}
+
 
 @app.route('/tasks')
 def list():
@@ -31,8 +33,14 @@ def create():
         if not title or not description:
             return "The fields 'title' and 'description' are required", 400
 
+        if isinstance(priority, str):
+            priority = PRIORITY_NAMES.get(priority.strip().lower(), priority)
+
         if priority is not None and (isinstance(priority, bool) or priority not in PRIORITIES):
-            return "The field 'priority' must be 1 (high), 2 (medium) or 3 (low)", 400
+            return "The field 'priority' must be 1 (high), 2 (medium) or 3 (low), or the string 'high', 'medium' or 'low'", 400
+
+        if priority is not None:
+            data = {**data, 'priority': priority}
 
         task = tasks_dao.create(data)
 
