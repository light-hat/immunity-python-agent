"""
Модуль agent_logger.py

Этот модуль предоставляет класс AgentLogger, предназначенный для ведения логов
в рамках системы интерактивного анализа. Класс AgentLogger позволяет записывать
сообщения различных уровней важности (debug, info, warning, error, critical),
используя объект логирования из стандартной библиотеки Python.

Основные возможности:
- Ведение логов на разных уровнях важности.
- Поддержка форматированных строк и дополнительных аргументов.
- Возможность записи исключений с трассировкой стека.
"""

import logging

loggers = {}

LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s] %(message)s"


class AgentLogger:
    """
    Класс логгера агента интерактивного анализа.

    Этот класс используется для регистрации сообщений различного уровня важности,
    таких как отладочные сообщения, информационные, предупреждения, ошибки и критические ошибки.
    """

    def __init__(self, log: logging.Logger) -> None:
        """
        Конструктор класса.

        :param log: Объект логирования, который будет использоваться для записи сообщений.
        :type log: logging.Logger
        """
        self._log = log

    def debug(self, msg: str, *args, **kwargs) -> None:
        """
        Запись отладочного сообщения.

        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        """
        Запись информационного сообщения.

        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        """
        Запись предупреждающего сообщения.

        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.warning(msg, *args, **kwargs)

    def warn(self, msg: str, *args, **kwargs) -> None:
        """
        Запись предупреждающего сообщения (синоним метода warning).

        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.warn(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        """
        Запись сообщения об ошибке.

        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, exc_info: bool = True, **kwargs) -> None:
        """
        Запись исключения с трассировкой стека.

        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param exc_info: Флаг, определяющий необходимость включения информации о текущем исключении.
        :type exc_info: bool
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        """
        Запись критического сообщения.

        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.critical(msg, *args, **kwargs)

    def log(self, level: int, msg: str, *args, **kwargs) -> None:
        """
        Запись сообщения с указанным уровнем важности.

        :param level: Уровень важности сообщения.
        :type level: int
        :param msg: Сообщение, которое нужно записать.
        :type msg: str
        :param args: Дополнительные аргументы для форматирования строки.
        :param kwargs: Ключевые слова для форматирования строки.
        """
        return self._log.log(level, msg, *args, **kwargs)


def logger_config(logging_name: str) -> AgentLogger:
    """
    Получение логгера по названию.

    :param logging_name: Название логгера.
    :type logging_name: str
    :return: Объект логгера.
    :rtype: AgentLogger
    """

    global loggers  # pylint: disable=global-variable-not-assigned

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
