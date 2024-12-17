import sys
import json
from immunity_agent.api.client import Client
from immunity_agent.control_flow import ControlFlowBuilder
from immunity_agent.logger import logger_config

logger = logger_config("Immunity Flask middleware")

class ImmunityFlaskMiddleware:
    """
    Промежуточное ПО для инструментирования фреймворка Flask.
    """
    def __init__(self, app, base_path):
        """
        Конструктор.
        """
        self.app = app
        self.base_path = base_path
        self.api_client = Client()
        self.project = self.api_client.project
        logger.info('Агент Immunity IAST активирован.')

    def __call__(self, environ, start_response):
        # Перехват входящего запроса
        request_info = self._capture_request(environ)
        #print("==== Incoming Request ====")
        #print(request_info)

        # Буфер для записи ответа
        response_body = []

        def custom_start_response(status, headers, exc_info=None):
            # Сохранение данных о статусе и заголовках
            self.status = status
            self.headers = headers
            # Передача управления оригинальному start_response
            return start_response(status, headers, exc_info)

        self.control_flow = ControlFlowBuilder(project_root=str(self.base_path))
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
            if hasattr(app_iter, 'close'):
                app_iter.close()

        # Анализируем полный ответ (после сборки всего тела)
        response_data = b"".join(response_body)
        response_info = self._capture_response(self.status, self.headers, response_data)
        #print("==== Outgoing Response ====")
        #print(response_info)

        self.api_client.upload_context(
            request_info["path"],
            self.project,
            json.dumps(request_info),
            self.control_flow.serialize(),
            json.dumps(response_info)
        )

    def _capture_request(self, environ):
        """
        Сбор информации о запросе из WSGI environ.
        """
        from urllib.parse import parse_qs
        request_info = {
            "method": environ.get("REQUEST_METHOD"),
            "path": environ.get("PATH_INFO"),
            "query": parse_qs(environ.get("QUERY_STRING", "")),
            "headers": self._extract_headers(environ),
        }

        # Чтение тела запроса
        try:
            request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0) or 0))
            environ["wsgi.input"] = self._reset_stream(request_body)  # Сохраняем поток
            request_info["body"] = request_body.decode("utf-8")
        except Exception:
            request_info["body"] = None

        return request_info

    def _capture_response(self, status, headers, body):
        """
        Сбор информации об ответе.
        """
        return {
            "status": status,
            "headers": dict(headers),
            "body": body.decode("utf-8") if body else None,
        }

    def _extract_headers(self, environ):
        """
        Извлечение заголовков из WSGI environ.
        """
        return {key[5:]: value for key, value in environ.items() if key.startswith("HTTP_")}

    def _reset_stream(self, body):
        """
        Восстанавливает wsgi.input поток после чтения.
        """
        from io import BytesIO
        return BytesIO(body)
