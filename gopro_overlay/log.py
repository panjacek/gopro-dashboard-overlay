import sys
import logging

logger = logging.getLogger(__name__)


def log(s):
    # print(s, file=sys.stderr)
    logger.info(s)


def fatal(s, error=True):
    logger.critical(s)
    # log(s)
    exitcode = 1 if error else 0
    exit(exitcode)
