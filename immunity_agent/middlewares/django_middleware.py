"""
Промежуточное ПО для интеграции агента Immunity IAST с фреймворком Django.

Этот модуль предоставляет промежуточное программное обеспечение (middleware) для фреймворка Django,
которое позволяет интегрировать агент Immunity IAST для мониторинга и анализа запросов и ответов.
"""

import sys
import json
from typing import Any

from django.conf import settings
import pkg_resources
from immunity_agent.api.client import Client
from immunity_agent.control_flow import ControlFlowBuilder
from immunity_agent.logger import logger_config
from immunity_agent.request.django_request import DjangoRequest
from immunity_agent.response.django_response import DjangoResponse

logger = logger_config("Immunity Django middleware")


class ImmunityDjangoMiddleware:  # pylint: disable=too-few-public-methods
    """
    Промежуточное ПО для инструментирования фреймворка Django.

    Этот класс реализует промежуточное ПО для фреймворка Django,
    которое интегрирует агент Immunity IAST для мониторинга и анализа
    запросов и ответов.

    :param get_response: Функция, возвращающая ответ на запрос.
    :type get_response: Callable[[HttpRequest], HttpResponse]
    """

    def __init__(self, get_response: callable):
        """
        Конструктор класса.

        Устанавливает функцию получения ответа и создает экземпляр клиента API.

        :param get_response: Функция, возвращающая ответ на запрос.
        :type get_response: Callable[[HttpRequest], HttpResponse]
        """
        self.get_response = get_response
        self.api_client = Client()
        self.project = self.api_client.project
        self.control_flow = None
        logger.info("Агент Immunity IAST активирован.")

        self.api_client.upload_config(json.dumps(self._extract_settings()), self.project, "django")
        self.api_client.upload_dependencies(json.dumps({d.key: d.version for d in pkg_resources.working_set}), self.project)

    def __call__(self, request: Any) -> Any:
        """
        Переопределяем метод вызова.

        Этот метод перехватывает запросы и ответы, собирает информацию о них и передает её в API.

        :param request: Объект запроса.
        :type request: HttpRequest
        :return: Ответ.
        :rtype: HttpResponse
        """
        # flowchart: start
        logger.info(f"Отслеживаю запрос {request.path}") # flowchart: start
        self.control_flow = ControlFlowBuilder(project_root=str(settings.BASE_DIR))
        sys.settrace(self.control_flow.trace_calls)

        response = self.get_response(request)

        sys.settrace(None)

        self.api_client.upload_context(
            request.path,
            self.project,
            DjangoRequest.serialize(request),
            self.control_flow.serialize(),
            DjangoResponse.serialize(response),
        )
        # flowchart: end

        return response

    def _extract_settings(self):
        """
        Динамически извлекает настройки из Django-проекта.
        :return: Словарь с настройками.
        """
        settings_dict = {
            setting: getattr(settings, setting)
            for setting in dir(settings)
            if setting.isupper()
        }

        # Форматируем в строку
        settings_dict = {key: str(value) for key, value in settings_dict.items()}
        return settings_dict
