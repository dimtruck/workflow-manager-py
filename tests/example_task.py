from workflow_manager.task import Task


class SuccessTask(Task):

    def __init__(self, name):
        super().__init__(name)

    def execute(self, **kwargs):
        return (Task.success_state(), 'param', 'from',
                'task', self.name, 'to', 'next', 'task')


class FailureTask(Task):

    def __init__(self, name):
        super().__init__(name)

    def execute(self, **kwargs):
        return Task.failure_state(), 'failure message from ', self.name
