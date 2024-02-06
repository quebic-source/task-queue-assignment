import queue
import threading

from app.config import config_loader
from app.utils import get_logger
from app.task_status_tracker import TaskStatusTrackerFactory, QUEUED_STATUS, SUCCESS_STATUS, FAILED_STATUS

logging = get_logger('task_queue')


class TaskQueue:
    """
    A TaskQueue class for managing tasks using a queue and worker threads.
    It supports enqueuing tasks, dequeuing tasks for processing, and tracking task status through a queue broker.
    """

    def __init__(self):
        """
        Initializes the TaskQueue with a queue for tasks, a specified number of worker threads,
        and a queue broker for managing task statuses.
        """
        self.task_queue = queue.Queue()
        self.num_workers = config_loader.get_app_config().get("num_workers")
        self.task_status_tracker = TaskStatusTrackerFactory.get_tracker()

    def enqueue(self, task, *args):
        """
        Enqueues a task along with its arguments into the task queue and logs the operation.

        :param task: The task function to be enqueued.
        :param args: Arguments to be passed to the task function.
        """
        self.task_queue.put((task, args))
        task_name = task.__name__
        logging.info(f"Task queued: {task_name}")
        self.task_status_tracker.set_status(task_name, QUEUED_STATUS)

    def dequeue(self):
        """
        Dequeues a task from the task queue for processing.

        :return: The dequeued task and its arguments.
        """
        return self.task_queue.get()

    def worker(self):
        """
        Worker thread method that processes tasks from the queue until stopped.
        """
        while True:
            try:
                task, args = self.dequeue()
                task_name = task.__name__
                logging.info(f"Task processing: {task_name}")
                task(*args)
                self.task_status_tracker.set_status(task_name, SUCCESS_STATUS)
                logging.info(f"Task completed: {task_name}")
            except Exception as e:
                logging.error(f"Task failed task: {task_name}, error: {e}")
                self.task_status_tracker.set_status(task_name, FAILED_STATUS)

            self.task_queue.task_done()

    def start_workers(self):
        """
        Starts the worker threads based on the specified number of workers.
        """
        for _ in range(self.num_workers):
            thread = threading.Thread(target=self.worker, daemon=True)
            thread.start()

    def join(self):
        """
        Blocks the calling thread until all tasks in the queue have been processed.
        This ensures that the program waits for all queued tasks to complete before exiting.
        """
        self.task_queue.join()

    def get_task_status(self, task_name):
        """
        Retrieves the status of a specific task from the queue broker.

        :param task_name: The name of the task for which the status is requested.
        :return: The status of the task as managed by the queue broker.
        """
        return self.task_status_tracker.get_status(task_name)
