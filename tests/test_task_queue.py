import os

os.environ["ENVIRONMENT"] = "testing"

import unittest
from app.task_queue import TaskQueue
from app.task_status_tracker import SUCCESS_STATUS, FAILED_STATUS


def mock_task_1(arg1, arg2):
    pass


def mock_task_2(arg1, arg2):
    pass


def mock_task_3(arg1, arg2):
    raise Exception('Error 1')


class TestTaskQueue(unittest.TestCase):
    def setUp(self):
        self.task_queue = TaskQueue()

    def test_enqueue_dequeue_task(self):
        self.task_queue.enqueue(mock_task_1, 'arg1', 'arg2')

        (task, args) = self.task_queue.dequeue()

        self.assertEqual(task.__name__, mock_task_1.__name__)

    def test_worker(self):
        self.task_queue.enqueue(mock_task_1, 'arg1', 'arg2')
        self.task_queue.enqueue(mock_task_2, 'arg1', 'arg2')
        self.task_queue.enqueue(mock_task_3, 'arg1', 'arg2')
        self.task_queue.start_workers()
        self.task_queue.join()

        self.assertEqual(self.task_queue.get_task_status(mock_task_1.__name__), SUCCESS_STATUS)
        self.assertEqual(self.task_queue.get_task_status(mock_task_2.__name__), SUCCESS_STATUS)
        self.assertEqual(self.task_queue.get_task_status(mock_task_3.__name__), FAILED_STATUS)


if __name__ == '__main__':
    unittest.main()
