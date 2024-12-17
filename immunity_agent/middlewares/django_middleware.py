"""
Промежуточное ПО для интеграции агента Immunity IAST с фреймворком Django.

Этот модуль предоставляет промежуточное программное обеспечение (middleware) для фреймворка Django,
которое позволяет интегрировать агент Immunity IAST для мониторинга и анализа запросов и ответов.
"""

import sys
from typing import Any

from django.conf import settings

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

    def __call__(self, request: Any) -> Any:
        """
        Переопределяем метод вызова.

        Этот метод перехватывает запросы и ответы, собирает информацию о них и передает её в API.

        :param request: Объект запроса.
        :type request: HttpRequest
        :return: Ответ.
        :rtype: HttpResponse
        """
        logger.info(f"Отслеживаю запрос {request.path}")
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

        return response
