# Workflow manager

Python implementation of task-based workflow manager.

This package enables an easy wrap of any functionality that has dependencies on other functionality within your codebase.

A simple use case would be a step by step wizard that has multiple success and failure scenarios.  This package enables instantiation of all task rules in the wizard and then a simple manager wrapper to execute the workflow in one call.

The package also provides an ability to view the history of the workflow for debugging purposes.

## How

Given the following business tasks:

```
task one
task two
task three
task four
task five
task six
```

And the following business rules:

```
if task one succeeds, task two and task three will execute in sequence
if task one fails, task five will execute
if task two succeeds, task four will execute
if task two fails, task five will execute
if task three fails, task six will execute
if task four fails, task six will execute
if task five succeeds, task six will execute
```

This module will set up a workflow that, based on status of the task, will execute the proper dependencies in the correct order.

The module will also short circuit any calls on failure scenarios but will execute all failure dependencies required to completely clean up your workflow.

For concrete examples, check out `tests/test_workflow.py`.

## Setup

`pip install workflow_manager`

Create your task, inhertit from `workflow_manager.task.Task` class, and overwrite the `execute` method with your own logic:

```python
from workflow_manager.task import Task

class CustomTask(Task):

    def __init__(self):
        super().__init__('my custom task')

    def execute(self, **kwargs):
        # your logic here
        if success:
            return (Task.success_state(), 'result', 'in', 'a', 'list')
        else:
            return (Task.failure_state(), 'this failed because of reasons')


class AnotherTask(Task):

    def __init__(self):
        super().__init__('some other task')

    def execute(self, **kwargs):
        # your logic here
        if success:
            return (Task.success_state(), 'result', 'in', 'a', 'list')
        else:
            return (Task.failure_state(), 'this failed because of reasons')
```

Then, add your business rules.

```python
customTask = CustomTask()
anotherTask = AnotherTask()
customTask.on_success(anotherTask, someOtherTask)
customTask.on_failure(cleanupTask)
anotherTask.on_success(keepItGoingTask)
anotherTask.on_failure(cleanupTask)
```

You can validate your workflow by printing your initial task (the one that will initiate the workflow):

```python

str(customTask) # prints the entire workflow as json
customTask.to_dict() # returns a dictionary of the workflow
```

Finally, simply register the initial task (the one that will initiate the workflow), and call `run` fuction:

```python
from workflow_manager.manager import Manager


manager = Manager()
manager.register_initial_task(customTask)

manager.run()
```

If you want to see what happened after the workflow ends, you can call `show_executed_flow` method, which will return a list of tasks and the parameters.

`manager.show_executed_flow()`
