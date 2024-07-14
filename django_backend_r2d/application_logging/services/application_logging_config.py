import logging.config
from application_logging.services.ApplicationLogFormatter import ApplicationLogFormatter
import os 
import watchtower
import socket 
import datetime

"""
Application logging configuration. The log template is defined in ApplicationLogFormatter.py
Application logs support different log levels e.g., DEBUG, INFO, WARN, ERROR.
Sample Log Created:
{
    "message": "WSGI Initialized",
    "time_stamp": "2024-05-12 16:55:19",
    "level": "INFO",
    "application_name": "django_backend_r2d",
    "function": "Log message created directly in wsgi.py", (Will be function name if called within a function)
    "file_name": "wsgi.py"
}
"""

def get_log_level():
    """
    Get the log level from the environment variable. Default is ERROR.
    """
    return os.getenv("LOG_LEVEL", "ERROR")
                     
# Retrieve the container ID 
def get_short_container_id():
    try:
        with open('/proc/self/cgroup', 'r') as f:
            for line in f:
                if 'docker' in line:
                    return line.strip().split('/')[-1][:8]  # Use only the first 8 characters
    except Exception as e:
        return socket.gethostname()[:8]  # Fallback to the first 8 characters of hostname if not running in Docker

def get_log_group_name():
    return f"{os.getenv('APP_ENVIRONMENT')}/{os.getenv('CLOUDWATCH_LOG_GROUP_NAME', 'default-log-group')}"

def get_log_stream_name():
    service_name = os.getenv('CLOUDWATCH_LOG_STREAM_NAME', 'unknown-service')
    short_container_id = get_short_container_id()
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    return f"{service_name}/{short_container_id}_{timestamp}"


cloudwatch_handler = {
    'level': get_log_level(),
    'class': 'watchtower.CloudWatchLogHandler',
    'formatter': 'application_logs',
    'log_group': get_log_group_name(),
    'stream_name': get_log_stream_name(),
    'create_log_group': True,
    'send_interval': 5,
    'max_batch_size': 256 * 1024,
    'max_batch_count': 500,
    'use_queues': True,
}

# Set the use_queue to False in development environment, use_queue is True by default and runs into conflicts with Django runserver
if os.getenv("APP_ENVIRONMENT") == "local" or os.getenv("APP_ENVIRONMENT") == "development":
    # In development, avoid using CloudWatch handler or set use_queue to False
    cloudwatch_handler['use_queues'] = False
        
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'application_logs': {
            '()': ApplicationLogFormatter,
        },
    },
    'handlers': {
        'console': {
            'level': get_log_level(),
            'class': 'logging.StreamHandler',
            'formatter': 'application_logs',
        },
        'file': {
            'level': get_log_level(),
            'class': 'logging.FileHandler',
            'filename': "application.logs",
            'formatter': 'application_logs',
        },
        'cloudwatch': cloudwatch_handler,
    },
    'loggers': {
        'application_logging': {
            'handlers': ['console', 'file', 'cloudwatch'],
            'level': get_log_level(),
            'propagate': True,
        },
    },
}

LOGGING_CONFIGURED = False

def setup_logging():
    global LOGGING_CONFIGURED
    if LOGGING_CONFIGURED:
        return  # Prevent multiple setups
    print("Setting up logging configuration...")
    logging.config.dictConfig(LOGGING_CONFIG)
    watchtower_logger = logging.getLogger("watchtower")
    watchtower_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    watchtower_logger.addHandler(console_handler)
    LOGGING_CONFIGURED = True
    print("Logging configuration set up successfully.")

def flush_cloudwatch_handler():
    logger = logging.getLogger('application_logging')
    for handler in logger.handlers:
        if isinstance(handler, watchtower.CloudWatchLogHandler):
            handler.flush()