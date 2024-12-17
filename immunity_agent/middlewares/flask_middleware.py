"""
Промежуточное ПО для интеграции агента Immunity IAST с фреймворком Flask.

Этот модуль предоставляет промежуточное программное обеспечение (middleware) для фреймворка Flask,
которое позволяет интегрировать агент Immunity IAST для мониторинга и анализа запросов и ответов.
"""

import json
import sys
from io import BytesIO
from typing import Any, Dict, List, Tuple
from urllib.parse import parse_qs

from immunity_agent.api.client import Client
from immunity_agent.control_flow import ControlFlowBuilder
from immunity_agent.logger import logger_config

logger = logger_config("Immunity Flask middleware")


class ImmunityFlaskMiddleware:  # pylint: disable=too-few-public-methods
    """
    Промежуточное ПО для инструментирования фреймворка Flask.

    Этот класс реализует промежуточное ПО для фреймворка Flask, которое
    интегрирует агент Immunity IAST для мониторинга и анализа запросов
    и ответов.

    :param app: Экземпляр приложения Flask.
    :type app: Flask
    :param base_path: Базовый путь к приложению.
    :type base_path: str
    """

    def __init__(self, app: object, base_path: str):
        """
        Конструктор класса.

        Устанавливает приложение Flask, базовый путь и создаёт экземпляр клиента API.

        :param app: Экземпляр приложения Flask.
        :type app: Flask
        :param base_path: Базовый путь к приложению.
        :type base_path: str
        """
        self.app = app
        self.base_path = base_path
        self.api_client = Client()
        self.project = self.api_client.project
        self.status = None
        self.headers = None
        self.control_flow = None
        logger.info("Агент Immunity IAST активирован.")

    def __call__(self, environ: Dict[str, str], start_response: callable) -> bytes:
        """
        Переопределяем метод вызова.

        Этот метод перехватывает запросы и ответы, собирает информацию о них и передает её в API.

        :param environ: Словарь окружения WSGI.
        :type environ: Dict[str, str]
        :param start_response: Функция начала ответа.
        :type start_response: Callable[[str, List[Tuple[str, str]], Any], None]
        :return: Ответ.
        :rtype: bytes
        """
        # Перехват входящего запроса
        request_info = self._capture_request(environ)

        # Буфер для записи ответа
        response_body = []

        def custom_start_response(
            response_status: str,
            response_headers: List[Tuple[str, str]],
            exc_info: Any = None,
        ) -> None:
            """
            Модификация функции начала ответа для сохранения статуса и заголовков.

            :param response_status: Статус ответа.
            :type response_status: str
            :param response_headers: Заголовки ответа.
            :type response_headers: List[Tuple[str, str]]
            :param exc_info: Информация об исключении.
            :type exc_info: Any
            """
            # Сохранение данных о статусе и заголовках
            self.status = response_status
            self.headers = response_headers
            # Передача управления оригинальному start_response
            return start_response(response_status, response_headers, exc_info)

        self.control_flow = ControlFlowBuilder(project_root=self.base_path)
        sys.settrace(self.control_flow.trace_calls)

        # Вызов приложения с модифицированным start_response
        app_iter = self.app(environ, custom_start_response)

        try:
            # Сбор ответа из app_iter
            for data in app_iter:
                response_body.append(data)
                yield data
        finally:
            # Закрываем итератор, если он поддерживает метод close()
            if hasattr(app_iter, "close"):
                app_iter.close()

        # Анализируем полный ответ (после сборки всего тела)
        response_data = b"".join(response_body)
        response_info = self._capture_response(self.status, self.headers, response_data)

        self.api_client.upload_context(
            request_info["path"],
            self.project,
            json.dumps(request_info),
            self.control_flow.serialize(),
            json.dumps(response_info),
        )

    def _capture_request(self, environ: Dict[str, str]) -> Dict[str, any]:
        """
        Сбор информации о запросе из WSGI environ.

        :param environ: Словарь окружения WSGI.
        :type environ: Dict[str, str]
        :return: Информация о запросе.
        :rtype: Dict[str, any]
        """
        request_info = {
            "method": environ.get("REQUEST_METHOD"),
            "path": environ.get("PATH_INFO"),
            "query": parse_qs(environ.get("QUERY_STRING", "")),
            "headers": self._extract_headers(environ),
        }

        # Чтение тела запроса
        try:
            request_body = environ["wsgi.input"].read(
                int(environ.get("CONTENT_LENGTH", 0) or 0)
            )
            environ["wsgi.input"] = self._reset_stream(request_body)  # Сохраняем поток
            request_info["body"] = request_body.decode("utf-8")
        except Exception:  # pylint: disable=broad-except
            request_info["body"] = None

        return request_info

    def _capture_response(
        self, status: str, headers: List[Tuple[str, str]], body: bytes
    ) -> Dict[str, any]:
        """
        Сбор информации об ответе.

        :param status: Статус ответа.
        :type status: str
        :param headers: Заголовки ответа.
        :type headers: List[Tuple[str, str]]
        :param body: Тело ответа.
        :type body: bytes
        :return: Информация об ответе.
        :rtype: Dict[str, any]
        """
        return {
            "status": status,
            "headers": dict(headers),
            "body": body.decode("utf-8") if body else None,
        }

    def _extract_headers(self, environ: Dict[str, str]) -> Dict[str, str]:
        """
        Извлечение заголовков из WSGI environ.

        :param environ: Словарь окружения WSGI.
        :type environ: Dict[str, str]
        :return: Заголовки запроса.
        :rtype: Dict[str, str]
        """
        return {
            key[5:]: value for key, value in environ.items() if key.startswith("HTTP_")
        }

    def _reset_stream(self, body: bytes) -> BytesIO:
        """
        Восстанавливает wsgi.input поток после чтения.

        :param body: Данные тела запроса.
        :type body: bytes
        :return: Поток байтов.
        :rtype: BytesIO
        """
        return BytesIO(body)
