import os

os.environ["ENVIRONMENT"] = "testing"

import unittest
from app.task_queue import TaskQueue
from app.task_status_tracker import QUEUED_STATUS, SUCCESS_STATUS, FAILED_STATUS


def mock_task_1(arg1, arg2):
    pass


def mock_task_2(arg1, arg2):
    pass


def mock_task_3(arg1, arg2):
    raise Exception('Error Task 3')


class TestTaskQueue(unittest.TestCase):
    def setUp(self):
        # Initialize a TaskQueue instance before each test.
        self.task_queue = TaskQueue()

    def test_enqueue_dequeue_task(self):
        # Test if enqueuing and then dequeuing a task returns the correct task and its arguments.
        self.task_queue.enqueue(mock_task_1, 'arg1', 'arg2')

        (task, args) = self.task_queue.dequeue()

        self.assertEqual(task.__name__, mock_task_1.__name__)

    def test_queued_task_status(self):
        # Test if the status of an enqueued task is correctly set to QUEUED_STATUS.
        self.task_queue.enqueue(mock_task_1, 'arg1', 'arg2')

        self.assertEqual(self.task_queue.get_task_status(mock_task_1.__name__), QUEUED_STATUS)

    def test_success_task_status(self):
        # Test if executing a task successfully updates its status to SUCCESS_STATUS.
        self.task_queue.enqueue(mock_task_1, 'arg1', 'arg2')

        self.task_queue.start_workers()
        self.task_queue.join()

        self.assertEqual(self.task_queue.get_task_status(mock_task_1.__name__), SUCCESS_STATUS)

    def test_failed_task_status(self):
        # Test if a task that raises an exception has its status correctly set to FAILED_STATUS.
        self.task_queue.enqueue(mock_task_3, 'arg1', 'arg2')

        self.task_queue.start_workers()
        self.task_queue.join()

        self.assertEqual(self.task_queue.get_task_status(mock_task_3.__name__), FAILED_STATUS)

    def test_multiple_workers(self):
        # Test if multiple tasks can be processed concurrently and have their statuses correctly set to SUCCESS_STATUS.
        self.task_queue.enqueue(mock_task_1, 'arg1', 'arg2')
        self.task_queue.enqueue(mock_task_2, 'arg1', 'arg2')

        self.task_queue.start_workers()
        self.task_queue.join()

        self.assertEqual(self.task_queue.get_task_status(mock_task_1.__name__), SUCCESS_STATUS)
        self.assertEqual(self.task_queue.get_task_status(mock_task_2.__name__), SUCCESS_STATUS)


if __name__ == '__main__':
    unittest.main()
