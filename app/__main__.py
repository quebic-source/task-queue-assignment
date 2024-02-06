import time

from app.utils import get_logger
from app.task_queue import TaskQueue

logging = get_logger('main')


def task_a(data):
    time.sleep(3) # Simulate a time-consuming operation.
    return f"Processed {data}"


def task_b(data):
    time.sleep(3) # Simulate a time-consuming operation.
    return f"Processed {data}"


if __name__ == '__main__':
    start_time = time.time()

    try:
        task_queue = TaskQueue()
        task_queue.enqueue(task_a, 'process-1')
        task_queue.enqueue(task_b, 'process-2')
        task_queue.start_workers()
        task_queue.join()
    except Exception as e:
        # Fallback handle
        logging.exception("App execution failed")

    total_time = time.time() - start_time
    logging.info(f"Took:{total_time:.4f} seconds")
