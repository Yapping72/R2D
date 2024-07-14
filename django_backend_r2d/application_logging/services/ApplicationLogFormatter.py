from pythonjsonlogger import jsonlogger
import logging
import inspect
import sys
import os

class ApplicationLogFormatter(jsonlogger.JsonFormatter):
    """
    A custom log formatter that formats logging messages into a structured JSON format.
    
    Usage: 
        import logging
        logger = logging.getLogger('application_logging')
        logger.info("Message") 
        logger.info("Message", extra={"key": "value"}) # To add custom fields to the log record
    Attributes:
        None explicitly declared beyond superclass.

    Methods:
        formatTime(record, datefmt=None): Overrides to provide custom time formatting.
        add_fields(log_record, record, message_dict): Overrides to add custom fields.
    
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
    def formatTime(self, record, datefmt=None):
        # Define custom date format: YYYY-MM-DD HH:MM:SS followed by microseconds
        datefmt = "%Y-%m-%d %H:%M:%S.%f"
        return super().formatTime(record, datefmt=datefmt)[:-3]  # Removing the last three digits to exclude partial microseconds

    
    def add_fields(self, log_record, record, message_dict):
        """
        Add custom fields to the log record before it is output.

        Args:
            log_record (dict): The log record to which fields are added.
            record (logging.LogRecord): The original log record.
            message_dict (dict): A dictionary of key-value pairs that will be passed to the logger.

        Modifies:
            log_record: Adds several custom fields such as 'time_stamp', 'level', and 'application_name'.
        """
        super().add_fields(log_record, record, message_dict)

        log_record['time_stamp'] = self.formatTime(record)
        log_record['level'] = record.levelname  # Adding log level

        frame = inspect.currentframe().f_back
        while frame:
            code = frame.f_code
            filename = code.co_filename
            function_name = code.co_name
            # Skip frames related to logging, jsonlogger, celery, watchtower, and __init__
            if 'logging' not in filename and 'jsonlogger' not in filename and 'celery' not in filename and 'watchtower' not in filename and function_name not in ['emit', '__init__']:
                module = inspect.getmodule(frame)

                if module and hasattr(module, '__name__'):
                    if 'django' in module.__name__:
                        log_record['application_name'] = module.__name__.split('.')[0]
                    else:
                        log_record['application_name'] = os.path.basename(filename).replace('.py', '')
                
                log_record['function'] = function_name
                log_record['file_name'] = os.path.basename(filename)
                
                if "<module>" in log_record['function']:
                    log_record['function'] = f"Log message created directly in {log_record['file_name']}"
                break
            frame = frame.f_back

        if 'application_name' not in log_record:
            log_record['application_name'] = '__unknown__'
        if 'function' not in log_record:
            log_record['function'] = '__unknown_function__'
        if 'file_name' not in log_record:
            log_record['file_name'] = '__unknown_file__'

        if record.exc_info:
            log_record['stack_trace'] = self.formatException(record.exc_info)
            log_record.pop('exc_info', None)
        else:
            log_record.pop('stack_trace', None)

        # Add custom fields from the log record, excluding internal attributes
        for key, value in record.__dict__.items():
            if key not in log_record and key not in [
                'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename', 'funcName', 'levelname', 
                'levelno', 'lineno', 'module', 'msecs', 'msecs', 'msg', 'name', 'pathname', 'process', 
                'processName', 'relativeCreated', 'thread', 'threadName', 'stack_info'
            ]:
                log_record[key] = value