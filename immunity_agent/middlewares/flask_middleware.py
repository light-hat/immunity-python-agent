from immunity_agent.logger import logger_config

logger = logger_config("Immunity Flask middleware")

class ImmunityFlaskMiddleware:
    """
    Промежуточное ПО для инструментирования фреймворка Flask.
    """
    def __init__(self, app):
        """
        Конструктор.
        """
        self.app = app

    def __call__(self, environ, start_response):
        """
        Переопределяем метод вызова.
        :param environ:
        :param start_response:
        :return: Ответ.
        """
        # Перехват входящего запроса
        request_info = self._capture_request(environ)
        logger.info("==== Incoming Request ====")
        logger.info(request_info)

        # Обертка для захвата ответа
        response_body = []

        def custom_start_response(status, headers, exc_info=None):
            # Сохранение данных о статусе и заголовках ответа
            self.status = status
            self.headers = headers
            return lambda data: response_body.append(data)

        # Передача управления приложению
        app_iter = self.app(environ, custom_start_response)

        # Сбор ответа из app_iter
        response_body.extend(app_iter)
        response_data = b"".join(response_body)

        # Анализ ответа
        response_info = self._capture_response(self.status, self.headers, response_data)
        logger.info("==== Outgoing Response ====")
        logger.info(response_info)

        return [response_data]

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
