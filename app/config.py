import configparser
import os


class ConfigLoader:
    """
    Define a class for loading and handling configuration settings
    """

    def __init__(self, config_file):
        # Initialize the parser and load the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_app_config(self):
        """Application configuration."""
        return {
            'num_workers': self.config.getint('APP', 'num_workers', fallback=4),
            'log_level': self.config.get('APP', 'log_level', fallback='INFO'),
            'queue_broker_type': self.config.get('APP', 'queue_broker_type', fallback='default')
        }

    def get_redis_config(self):
        """Redis configuration."""
        return {
            'host': self.config.get('REDIS', 'redis_host', fallback='localhost'),
            'port': self.config.getint('REDIS', 'redis_port', fallback=6379),
            'password': self.config.get('REDIS', 'redis_password', fallback=None),
        }


# Determine the environment (e.g., testing, development, production) from an environment variable
environment = os.getenv('ENVIRONMENT', 'development')
config_file_path = f"config/{environment}.conf"
config_loader = ConfigLoader(config_file_path)

