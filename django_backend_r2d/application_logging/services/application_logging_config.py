import logging.config
from application_logging.services.ApplicationLogFormatter import ApplicationLogFormatter
import os 


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
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'application_logs',
        },
        'file': {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': "application.logs",
        'formatter': 'application_logs',
    },
    },
    'loggers': {
        'application_logging': {
            'handlers': ['console','file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

"""Invoke this function to initialize application logging"""
def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
