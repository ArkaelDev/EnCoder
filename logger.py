import logging
import sys

# get logger
logger = logging.getLogger()

# create formatter. this determinees the output format of the log.

formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

# create handlers. where the logs are going
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')

# set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handlers lo the logger
logger.handlers = [stream_handler, file_handler]

# set logger level
logger.setLevel(logging.INFO)


#This is not suppose to be a 100% useful and clear logger, it's just a test.