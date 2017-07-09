'''Responsible for managing the workflow.

Allows for registration of tasks.  Each task is responsible for a flow.

The manager will walk through the task list and based on result of the
task will take proper path

Example:

Given we have the following tasks:

task 1 on success calls task 2 on failure ends the flow
task 2 on success calls tasks 3 and 4 successively, on failure calls task 5
task 3 on success does nothing on failure calls task 5
task 4 on success calls task 5 on failure calls task 6
task 5 on success does nothing on failure calls task 6 and task 7 in succession
task 6 does nothing regardless of result
task 7 does nothing regradless of result

We will register each task object into the flow and call Manager.run() method.
Depending on result, the flow will take the right path.
'''
import copy
import json
from workflow_manager.task import Task


class Manager(object):

    def __init__(self, initial_task=None):
        ''' Constructor for manager.
        If an initial task is passed in, use that; else, the client can
        register initial task with the manager.
        '''
        if initial_task:
            self._task = initial_task
        else:
            self._task = None
        self._flow_path = []

    def register_initial_task(self, task):
        self._task = task

    def show_flow(self):
        return copy.deepcopy(self._task)

    def show_executed_flow(self):
        # show the flow here
        return copy.deepcopy(self._flow_path)

    def run(self):
        ''' Run the flow.

            Execution algorithm:
            1. take node and execute it = return result,*params
            2. if result == success
            3.  success_node = node.success_flow.pop
            4.  result,*params = success_node.execute
            5. elif result == failure
            3.  failure_node = node.failure_flow.pop
            4.  result,*params = failure_node.execute
        '''
        temp_task = self._task
        # default to success
        self._execute_run(temp_task, Task.success_state())

    def _execute_run(self, current_task, result, *params):
        failure_result = result == Task.failure_state()
        self._flow_path.append({
            'name': current_task.name,
            'parameters': params
        })
        result, *params = current_task.execute()
        if result == Task.success_state():
            success_flow = current_task.success_flow()
            while len(success_flow) > 0:
                success_task = success_flow.pop(0)
                # optimization.  check if success_task == previous task.  Skip!
                if (len(self._flow_path) > 0 and
                   self._flow_path[-1]['name'] == success_task.name):
                    continue
                result, params = self._execute_run(
                    success_task, result, params)
                if result == Task.failure_state():
                    break
        else:
            failure_result = True
            failure_flow = current_task.failure_flow()
            while len(failure_flow) > 0:
                failure_task = failure_flow.pop(0)
                # optimization.  check if failure_task == previous task.  Skip!
                if (len(self._flow_path) > 0 and
                   self._flow_path[-1]['name'] == failure_task.name):
                    continue
                result, params = self._execute_run(
                    failure_task, result, params)
        # we always return failure status if it failed even once during
        # our workflow to short circuit the flow
        if failure_result:
            return Task.failure_state(), params
        else:
            return result, params
