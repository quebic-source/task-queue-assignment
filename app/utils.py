import logging
from app.config import config_loader


def get_logger(module_name):
    """
    Setup and get a logger for a specific module.
    :param module_name:
    :return:
    """

    log_level = config_loader.get_app_config().get('log_level')

    # Convert log level from string to logging.* constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    logger = logging.getLogger(module_name)
    logger.setLevel(numeric_level)

    ch = logging.StreamHandler()
    ch.setLevel(numeric_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
