import logging

loggers = {}

LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'


class AgentLogger(object):
    def __init__(self, log):
        self._log = log

    def debug(self, msg, *args, **kwargs):
        return self._log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return self._log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self._log.warning(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        return self._log.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self._log.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        return self._log.exception(msg, *args, exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return self._log.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        return self._log.log(level, msg, *args, **kwargs)


def logger_config(logging_name):
    """
    Получение логгера по названию
    :param logging_name: Название логгера
    :return: Объект логгера
    """

    global loggers

    if loggers.get(logging_name):
        return loggers.get(logging_name)

    logger = logging.getLogger(logging_name)
    logger.handlers.clear()

    level = logging.INFO

    logger.setLevel(level)

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console)

    loggers[logging_name] = logger
    return AgentLogger(logger)
