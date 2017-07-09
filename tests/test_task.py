import example_task
from workflow_manager.manager import Manager
from workflow_manager.task import Task
import pytest


def test_init_with_name():
    assert Task('test 1').name == 'test 1'


def test_init():
    assert Task().name == 'task'


def test_execute_on_interface():
    with pytest.raises(NotImplementedError):
        Task().execute()


def test_to_string():
    assert str(Task('task 1')) == '{"name": "task 1", ' \
                                  '"success_flow": [], ' \
                                  '"failure_flow": []}'
