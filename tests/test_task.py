# coding=utf-8
import mongomock
import pytest

from task import TaskDAO


@pytest.fixture
def dao():
    client = mongomock.MongoClient()
    database = client.todo_list
    return TaskDAO(database)


def test_create_returns_task_with_given_title_and_description(dao):
    task = dao.create({'title': 'The Best Title', 'description': 'The Best Description'})

    assert task['title'] == 'The Best Title'
    assert task['description'] == 'The Best Description'


def test_create_returns_task_that_is_not_done(dao):
    task = dao.create({'title': 'The Best Title', 'description': 'The Best Description'})

    assert task['done'] is False


def test_create_defaults_priority_to_medium(dao):
    task = dao.create({'title': 'The Best Title', 'description': 'The Best Description'})

    assert task['priority'] == 2


def test_create_keeps_the_given_priority(dao):
    task = dao.create({'title': 'The Best Title', 'description': 'The Best Description', 'priority': 1})

    assert task['priority'] == 1


def test_create_returns_task_with_an_id(dao):
    task = dao.create({'title': 'The Best Title', 'description': 'The Best Description'})

    assert '_id' in task


def test_create_persists_task_in_collection(dao):
    dao.create({'title': 'The Best Title', 'description': 'The Best Description'})

    assert dao.task_collection.count_documents({}) == 1


def test_read_returns_the_created_task(dao):
    created = dao.create({'title': 'The Best Title', 'description': 'The Best Description'})

    task = dao.read(created['_id']['$oid'])

    assert task['_id'] == created['_id']
    assert task['title'] == 'The Best Title'
    assert task['description'] == 'The Best Description'


def test_read_returns_none_for_unknown_id(dao):
    task = dao.read('5f9f1b9b9b9b9b9b9b9b9b9b')

    assert task is None


def test_list_returns_empty_list_when_no_tasks_exist(dao):
    tasks = dao.list()

    assert tasks == []


def test_list_returns_all_created_tasks(dao):
    dao.create({'title': 'First Title', 'description': 'First Description'})
    dao.create({'title': 'Second Title', 'description': 'Second Description'})

    tasks = dao.list()

    assert len(tasks) == 2
    titles = {task['title'] for task in tasks}
    assert titles == {'First Title', 'Second Title'}


def test_list_sorts_tasks_by_done_ascending(dao):
    done_task = dao.create({'title': 'Done Task', 'description': 'Description'})
    dao.task_collection.update_one(
        {'_id': dao.task_collection.find_one({'title': 'Done Task'})['_id']},
        {'$set': {'done': True}}
    )
    dao.create({'title': 'Not Done Task', 'description': 'Description'})

    tasks = dao.list()

    assert [task['done'] for task in tasks] == [False, True]
    assert tasks[1]['title'] == done_task['title']


def test_list_sorts_undone_tasks_by_priority_ascending(dao):
    dao.create({'title': 'Low Task', 'description': 'Description', 'priority': 3})
    dao.create({'title': 'High Task', 'description': 'Description', 'priority': 1})
    dao.create({'title': 'Medium Task', 'description': 'Description', 'priority': 2})

    tasks = dao.list()

    assert [task['title'] for task in tasks] == ['High Task', 'Medium Task', 'Low Task']


def test_list_sorts_by_done_before_priority(dao):
    dao.create({'title': 'Done High Task', 'description': 'Description', 'priority': 1})
    dao.task_collection.update_one(
        {'title': 'Done High Task'},
        {'$set': {'done': True}}
    )
    dao.create({'title': 'Undone Low Task', 'description': 'Description', 'priority': 3})

    tasks = dao.list()

    assert [task['title'] for task in tasks] == ['Undone Low Task', 'Done High Task']
