import redis
from app.config import config_loader

QUEUED_STATUS = 'queued'
SUCCESS_STATUS = 'success'
FAILED_STATUS = 'failed'


class TaskStatusTracker:
    """
    Base class for a task status tracker
    """

    def __init__(self):
        pass

    def set_status(self, task_name, status):
        raise NotImplementedError()

    def get_status(self, task_name):
        raise NotImplementedError()


class DefaultTaskStatusTracker(TaskStatusTracker):
    """
    Implement a default task status tracker that stores task statuses in a python dictionary.
    """

    def __init__(self):
        super().__init__()
        self.tasks_status = {}

    def set_status(self, task_name, status):
        # Update the status of the task in the dictionary.
        self.tasks_status[task_name] = status

    def get_status(self, task_name):
        # Retrieve the status of the task from the dictionary, returning None if the task is not found.
        return self.tasks_status.get(task_name)


class RedisTaskStatusTracker(TaskStatusTracker):
    """
    Implement a task status tracker that uses Redis to store task statuses.
    """

    def __init__(self):
        super().__init__()
        redis_config = config_loader.get_redis_config()
        self.redis_client = redis.Redis(
            host=redis_config.get('host'),
            port=redis_config.get('port'),
        )

    def set_status(self, task_name, status):
        # Set the status of the task in Redis
        self.redis_client.set(f"task_status:{task_name}", status)

    def get_status(self, task_name):
        # Retrieve the status of the task from Redis
        return self.redis_client.get(f"task_status:{task_name}")


class TaskStatusTrackerFactory:
    """
    A factory class to abstract the creation of task status tracker instances.
    """

    @staticmethod
    def get_tracker():
        broker_type = config_loader.get_app_config().get('queue_broker_type')
        if broker_type == 'redis':
            return RedisTaskStatusTracker()
        else:
            return DefaultTaskStatusTracker()