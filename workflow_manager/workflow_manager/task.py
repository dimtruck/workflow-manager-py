'''Responsible for a single workflow.

This is a task for the workflow.  It's an abstract class and
must be inherited

Every task can specify a list of successful and failure tasks

Status has to implement execute method and return a tuple with the
first value being success or failure of the task and the second
a dict of values task wants to pass to subsequent task

Manager will then flow through the task flow

Example:

my_task = Task('task 1')
second_task = Task('task 2')
third_task = Task('task 3')
fourth_task = Task('task 4')
fifth_task = Task('task 5')

my_task.on_success(second_task)
my_task.on_failure(fourth_task)

second_task.on_success(third_task, fourth_task)

third_task.on_failure(fourth_task, fifth_task)

task 1 on success calls task 2 on failure calls task 4
task 2 on success calls tasks 3 and 4 successively, on failure does nothing
task 3 on success does nothing on failure calls task 4 and task 5 in succession
task 4 does nothing regardless of result
task 5 does nothing regradless of result
'''
import copy
import json


class Task(object):

    def __init__(self, name='task'):
        self._name = name
        self._success_list = []
        self._failure_list = []

    @classmethod
    def success_state(self):
        return True

    @classmethod
    def failure_state(self):
        return False

    @property
    def name(self):
        return self._name

    def on_success(self, *tasks):
        for task in tasks:
            self._success_list.append(task)

    def on_failure(self, *tasks):
        for task in tasks:
            self._failure_list.append(task)

    def success_flow(self):
        return copy.deepcopy(self._success_list)

    def failure_flow(self):
        return copy.deepcopy(self._failure_list)

    def execute(self, **kwargs):
        raise NotImplementedError()

    def to_dict(self):
        return {
            'name': self.name,
            'success_flow': [task.to_dict() for task in self._success_list],
            'failure_flow': [task.to_dict() for task in self._failure_list]
            }

    def __str__(self):
        return json.dumps(self.to_dict())
