"""
Модуль для работы с конфигурацией агента интерактивного анализа.

Этот модуль предоставляет класс Config, который позволяет загружать,
сохранять и управлять данными конфигурации. Конфигурационные данные
хранятся в файле JSON.
"""

import json
from typing import Any, Dict, Optional

from immunity_agent.logger import logger_config

logger = logger_config("Immunity settings unit")


class Config:
    """
    Класс для управления конфигурацией агента.

    Этот класс отвечает за загрузку, сохранение и управление данными конфигурации.
    Конфигурационные данные хранятся в файле JSON.
    """

    def __init__(self):
        """
        Конструктор класса Config.

        Устанавливает имя файла конфигурации и загружает данные из этого файла.
        Если файл отсутствует, создается пустой словарь данных.
        """
        self.filename = "immunity_agent/config.json"
        self.data: Dict[str, Any] = self.load()

    def load(self) -> Dict[str, Any]:
        """
        Загружает данные конфигурации из файла.

        :return: Словарь с данными конфигурации.
        :raises FileNotFoundError: Если файл конфигурации не найден.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as e:
            logger.error(e)
            return {}

    def save(self) -> None:
        """
        Сохраняет текущие данные конфигурации в файл.
        """
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Получает значение по ключу из данных конфигурации.

        :param key: Ключ, по которому нужно получить значение.
        :param default: Значение по умолчанию, которое будет возвращено, если ключ не найден.
        :return: Значение, соответствующее ключу, либо значение по умолчанию.
        """
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Устанавливает новое значение для ключа в данных конфигурации и сохраняет изменения в файл.

        :param key: Ключ, для которого устанавливается значение.
        :param value: Новое значение для указанного ключа.
        """
        self.data[key] = value
        self.save()
