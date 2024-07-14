import logging
import watchtower

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
cloudwatch_handler = watchtower.CloudWatchLogHandler(log_group='your-log-group', stream_name='your-log-stream')
logger.addHandler(cloudwatch_handler)

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.error("This is an error message")