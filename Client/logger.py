import logging


def get_logger(name):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler = logging.FileHandler('client_dfs.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
