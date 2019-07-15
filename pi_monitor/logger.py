import logging


def get_logger():
    logger = logging.getLogger("pi-monitor")
    return logger


def set_logger(log_level, log_file=None):
    logger = logging.getLogger("pi-monitor")
    log_level = _get_log_level(log_level)

    # always create a stream (stdio) handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # optionally create a file handler as well
    # TODO: make sure log_file is valid and writable
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                      '%(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(log_level)
    return logger


def _get_log_level(log_level: str) -> int:
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    if log_level.lower() not in levels:
        raise ValueError(f"unknown logging level: {log_level}")

    level = levels[log_level.lower()]

    return level
