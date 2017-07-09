import example_task
from workflow_manager.manager import Manager
from workflow_manager.task import Task


def test_init():
    assert Manager().show_flow() is None


def test_init_with_task():
    task_one = example_task.SuccessTask('task 1')
    assert Manager(task_one).show_flow().to_dict() == task_one.to_dict()


def test_register_task():
    manager = Manager()
    task = example_task.SuccessTask('task 1')
    manager.register_initial_task(task)
    assert Manager(task).show_flow().to_dict() == task.to_dict()


def test_workflow_with_two_items():
    task_one = example_task.SuccessTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_one.on_success(task_two)

    manager = Manager()
    manager.register_initial_task(task_one)

    assert manager.show_flow().to_dict() == {
            'name': 'task 1',
            'success_flow': [
                {
                    'name': 'task 2',
                    'success_flow': [],
                    'failure_flow': []
                }
            ],
            'failure_flow': []
        }


def test_workflow_with_three_items_success_failure():
    task_one = example_task.SuccessTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_three = example_task.FailureTask('task 3')
    task_one.on_success(task_two)
    task_one.on_failure(task_three)
    task_two.on_failure(task_three)

    manager = Manager()
    manager.register_initial_task(task_one)

    assert manager.show_flow().to_dict() == {
        'name': 'task 1',
        'success_flow': [
            {
                'failure_flow': [
                    {
                        'failure_flow': [],
                        'name': 'task 3',
                        'success_flow': []
                    }
                ],
                'name': 'task 2',
                'success_flow': []
            }
        ],
        'failure_flow': [
            {
                'failure_flow': [],
                'name': 'task 3',
                'success_flow': []
            }
        ]
    }


def test_workflow_walking_through_successful_flow_two_nodes():
    '''
    Given:
    task 1 -> success -> task 2
    task 1 -> failure -> task 3
    task 2 -> failure -> task 3

    When:
    task 1 succeeds
    task 2 succeeds

    Then workflow is:
    task 1 -> task 2
    '''
    task_one = example_task.SuccessTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_three = example_task.FailureTask('task 3')
    task_one.on_success(task_two)
    task_one.on_failure(task_three)
    task_two.on_failure(task_three)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 2', 'parameters': (
            ['param', 'from', 'task', 'task 1',
             'to', 'next', 'task'],)}
        ]


def test_workflow_walking_through_failure_flow_two_nodes_second_fail():
    '''
    Given:
    task 1 -> success -> task 2
    task 1 -> failure -> task 4
    task 2 -> success -> task 3
    task 2 -> failure -> task 4

    When:
    task 1 succeeds
    task 2 fails

    Then workflow is:
    task 1 -> task 2 -> task 4
    '''
    task_one = example_task.SuccessTask('task 1')
    task_two = example_task.FailureTask('task 2')
    task_three = example_task.SuccessTask('task 3')
    task_four = example_task.FailureTask('task 4')

    task_one.on_success(task_two)
    task_one.on_failure(task_four)
    task_two.on_success(task_three)
    task_two.on_failure(task_four)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 2', 'parameters': (
            ['param', 'from', 'task',
             'task 1', 'to', 'next', 'task'],)},
        {'name': 'task 4', 'parameters': ([
            'failure message from ', 'task 2'],)}
    ]


def test_workflow_walking_through_failure_flow_two_nodes_first_fail():
    '''
    Given:
    task 1 -> success -> task 2
    task 1 -> failure -> task 4
    task 2 -> success -> task 3
    task 2 -> failure -> task 4

    When:
    task 1 fails

    Then workflow is:
    task 1 -> task 4
    '''
    task_one = example_task.FailureTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_three = example_task.SuccessTask('task 3')
    task_four = example_task.SuccessTask('task 4')

    task_one.on_success(task_two)
    task_one.on_failure(task_four)
    task_two.on_success(task_three)
    task_two.on_failure(task_four)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    print(manager.show_executed_flow())

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 4', 'parameters': ([
            'failure message from ', 'task 1'],)}
    ]


def test_workflow_walking_through_successful_flow_list():
    '''
    Given:
    task 1 -> success -> task 2, task 3
    task 1 -> failure -> task 4
    task 2 -> success -> task 5
    task 2 -> failure -> task 6
    task 3 -> success -> task 5
    task 3 -> failure -> task 6
    task 4 -> failure -> task 6
    task 4 -> success -> task 6

    When:
    test 1 succeeds
    test 2 succeeds
    test 3 succeeds
    test 5 succeeds

    Then workflow is:
    task 1 -> task 2 -> task 5 -> task 3 -> task 5
    '''
    task_one = example_task.SuccessTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_three = example_task.SuccessTask('task 3')
    task_four = example_task.SuccessTask('task 4')
    task_five = example_task.SuccessTask('task 5')
    task_six = example_task.SuccessTask('task 6')

    task_one.on_success(task_two, task_three)
    task_one.on_failure(task_four)
    task_two.on_success(task_five)
    task_two.on_failure(task_six)
    task_three.on_success(task_five)
    task_three.on_failure(task_six)
    task_four.on_success(task_six)
    task_four.on_failure(task_six)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 2', 'parameters': (
            ['param', 'from', 'task',
             'task 1', 'to', 'next', 'task'],)},
        {'name': 'task 5', 'parameters': (
            ['param', 'from', 'task',
             'task 2', 'to', 'next', 'task'],)},
        {'name': 'task 3', 'parameters': (
            ['param', 'from', 'task',
             'task 5', 'to', 'next', 'task'],)},
        {'name': 'task 5', 'parameters': (
            ['param', 'from', 'task', 'task 3',
             'to', 'next', 'task'],)}
        ]


def test_workflow_walking_through_successful_flow_list_optimized():
    '''
    Given:
    task 1 -> success -> task 2, task 3
    task 1 -> failure -> task 4
    task 2 -> success -> task 3
    task 2 -> failure -> task 6

    When:
    test 1 succeeds
    test 2 succeeds
    test 3 succeeds

    Then workflow is:
    task 1 -> task 2 -> task 3
    '''
    task_one = example_task.SuccessTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_three = example_task.SuccessTask('task 3')
    task_four = example_task.SuccessTask('task 4')
    task_five = example_task.SuccessTask('task 5')
    task_six = example_task.SuccessTask('task 6')

    task_one.on_success(task_two, task_three)
    task_one.on_failure(task_four)
    task_two.on_success(task_three)
    task_two.on_failure(task_six)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 2', 'parameters': (
            ['param', 'from', 'task', 'task 1',
             'to', 'next', 'task'],)},
        {'name': 'task 3', 'parameters': (
            ['param', 'from', 'task', 'task 2',
             'to', 'next', 'task'],)}
        ]


def test_workflow_walking_through_failure_flow_list():
    '''
    Given:
    task 1 -> success -> task 2, task 3
    task 1 -> failure -> task 4, task 6
    task 2 -> success -> task 5
    task 2 -> failure -> task 6
    task 3 -> success -> task 5
    task 3 -> failure -> task 6
    task 4 -> failure -> task 6
    task 4 -> success -> task 6

    When:
    test 1 fails
    test 4 succeeds

    Then workflow is:
    task 1 -> task 4 -> task 6
    '''
    task_one = example_task.FailureTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_three = example_task.SuccessTask('task 3')
    task_four = example_task.SuccessTask('task 4')
    task_five = example_task.SuccessTask('task 5')
    task_six = example_task.SuccessTask('task 6')

    task_one.on_success(task_two, task_three)
    task_one.on_failure(task_four, task_six)
    task_two.on_success(task_five)
    task_two.on_failure(task_six)
    task_three.on_success(task_five)
    task_three.on_failure(task_six)
    task_four.on_success(task_six)
    task_four.on_failure(task_six)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 4', 'parameters': (
            ['failure message from ', 'task 1'],)},
        {'name': 'task 6', 'parameters': (
            ['param', 'from', 'task', 'task 4',
             'to', 'next', 'task'],)}
        ]


def test_workflow_walking_through_failure_flow_list_different_flow():
    '''
    Given:
    task 1 -> success -> task 2, task 3
    task 1 -> failure -> task 4, task 6
    task 2 -> success -> task 5
    task 2 -> failure -> task 6
    task 3 -> success -> task 5
    task 3 -> failure -> task 6
    task 4 -> failure -> task 6
    task 4 -> success -> task 7

    When:
    test 1 fails
    test 4 succeeds

    Then workflow is:
    task 1 -> task 4 -> task 6
    '''
    task_one = example_task.FailureTask('task 1')
    task_two = example_task.SuccessTask('task 2')
    task_three = example_task.SuccessTask('task 3')
    task_four = example_task.SuccessTask('task 4')
    task_five = example_task.SuccessTask('task 5')
    task_six = example_task.SuccessTask('task 6')
    task_seven = example_task.SuccessTask('task 7')

    task_one.on_success(task_two, task_three)
    task_one.on_failure(task_four, task_six)
    task_two.on_success(task_five)
    task_two.on_failure(task_six)
    task_three.on_success(task_five)
    task_three.on_failure(task_six)
    task_four.on_success(task_seven)
    task_four.on_failure(task_six)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 4', 'parameters': (
            ['failure message from ', 'task 1'],)},
        {'name': 'task 7', 'parameters': (
            ['param', 'from', 'task', 'task 4', 'to', 'next', 'task'],)},
        {'name': 'task 6', 'parameters': (
            ['param', 'from', 'task', 'task 7', 'to', 'next', 'task'],)}
        ]


def test_workflow_walking_through_short_circuit_fail():
    '''
    Given:
    task 1 -> success -> task 2, task 3
    task 1 -> failure -> task 4
    task 2 -> success -> task 5
    task 2 -> failure -> task 6
    task 3 -> success -> task 5
    task 3 -> failure -> task 6
    task 4 -> failure -> task 6
    task 4 -> success -> task 6

    When:
    test 1 succeeds
    test 2 fails

    Then workflow is:
    task 1 -> task 2 -> task 6
    '''
    task_one = example_task.SuccessTask('task 1')
    task_two = example_task.FailureTask('task 2')
    task_three = example_task.SuccessTask('task 3')
    task_four = example_task.SuccessTask('task 4')
    task_five = example_task.SuccessTask('task 5')
    task_six = example_task.SuccessTask('task 6')

    task_one.on_success(task_two, task_three)
    task_one.on_failure(task_four)
    task_two.on_success(task_five)
    task_two.on_failure(task_six)
    task_three.on_success(task_five)
    task_three.on_failure(task_six)
    task_four.on_success(task_six)
    task_four.on_failure(task_six)

    manager = Manager()
    manager.register_initial_task(task_one)

    manager.run()

    assert manager.show_executed_flow() == [
        {'name': 'task 1', 'parameters': ()},
        {'name': 'task 2', 'parameters': (
            ['param', 'from', 'task', 'task 1', 'to', 'next', 'task'],)},
        {'name': 'task 6', 'parameters': (
            ['failure message from ', 'task 2'],)}
        ]
