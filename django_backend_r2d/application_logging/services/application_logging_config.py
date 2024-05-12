import logging.config
from application_logging.services.ApplicationLogFormatter import ApplicationLogFormatter
import os 


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'application_logs': {
            '()': ApplicationLogFormatter, # Custom log formatter that contains log template
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
