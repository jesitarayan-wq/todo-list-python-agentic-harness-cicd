diff --git a/tests/test_todo.py b/tests/test_todo.py
index 3c13ab7..b3b1653 100644
--- a/tests/test_todo.py
+++ b/tests/test_todo.py
@@ -216,3 +216,9 @@ def test_retrieve_task_with_pk_must_returns_task():
         response = client.get('/tasks/%s' % inserted_id)
         data = json.loads(response.data.decode('utf-8'))
         assert data['_id']['$oid'] == inserted_id
+
+
+def test_retrieve_task_with_invalid_pk_must_returns_400():
+    with app.test_client() as client:
+        response = client.get('/tasks/not-a-valid-id')
+        assert response.status_code == 400
diff --git a/todo.py b/todo.py
index 8779666..d586be8 100644
--- a/todo.py
+++ b/todo.py
@@ -1,6 +1,7 @@
 # coding=utf-8
 from flask import Flask, jsonify, request, abort
 from task import TaskDAO, PRIORITIES
+from bson.objectid import ObjectId
 import pymongo
 
 app = Flask('todoapp')
@@ -17,6 +18,8 @@ def list():
 @app.route('/tasks/<pk>', methods=['GET', 'PUT'])
 def get(pk):
     if request.method == 'GET':
+        if not ObjectId.is_valid(pk):
+            return "Invalid id format", 400
         return jsonify(tasks_dao.read(pk))
 
 
