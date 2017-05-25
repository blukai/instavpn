import logging

def setup_logging():
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # add ch to logger
    logger.addHandler(ch)
