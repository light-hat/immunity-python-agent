import json
from immunity_agent.context import DataCollector


class DataBuilder:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    def build(self) -> DataCollector:
        """
        Метод для построения объекта DataCollector на основе запроса и ответа.
        """
        collector = DataCollector()

        # Сбор данных из запроса
        collector.request_method = self.request.method
        collector.request_url = self.request.get_full_path()
        collector.request_headers = dict(self.request.headers)
        collector.request_body = self.request.body.decode('utf-8', errors='ignore')
        collector.query_params = self.request.GET.dict()
        collector.form_params = self.request.POST.dict()
        collector.json_payload = self._parse_json_payload(self.request)
        collector.cookies = self.request.COOKIES
        collector.session_data = self.request.session.items()
        collector.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        collector.client_ip = self.request.META.get('REMOTE_ADDR', '')

        # Сбор данных из ответа
        collector.response_status = self.response.status_code
        collector.response_headers = dict(self.response.items())
        collector.response_body = self.response.content.decode('utf-8', errors='ignore')

        # Логирование SQL запросов
        #collector.sql_queries = self._log_sql_queries()

        # Информация о пользователе
        collector.user_authenticated = self.request.user.is_authenticated
        if collector.user_authenticated:
            collector.user_id = str(self.request.user.id)
            collector.auth_token = self.request.META.get('HTTP_AUTHORIZATION', '')

        # Производительность
        #collector.performance_metrics['response_time'] = self._measure_response_time()

        # Логирование ошибок
        #collector.errors = self._log_errors()

        return collector

    def _parse_json_payload(self, request):
        """
        Попытка парсинга JSON-тела запроса.
        """
        try:
            return json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    '''def _log_sql_queries(self):
        """
        Логирование SQL-запросов.
        """
        return [{'sql': query['sql'], 'time': query['time']} for query in connection.queries]

    def _measure_response_time(self):
        """
        Измерение времени отклика.
        """
        # В данном случае просто заглушка, метод можно улучшить
        return None'''

    '''def _log_errors(self):
        """
        Получение списка ошибок, возникших в течение обработки запроса.
        """
        # Пример: заполняем список ошибками, если такие были пойманы
        return []'''
