import json
import base64
from typing import Dict, Any, List, Optional


class DataCollector:
    def __init__(self):
        # HTTP запросы и ответы
        self.request_method: Optional[str] = None
        self.request_url: Optional[str] = None
        self.request_headers: Dict[str, str] = {}
        self.request_body: Optional[str] = None
        self.response_status: Optional[int] = None
        self.response_headers: Dict[str, str] = {}
        self.response_body: Optional[str] = None

        # Инъекции данных и параметры
        self.query_params: Dict[str, str] = {}
        self.form_params: Dict[str, str] = {}
        self.json_payload: Dict[str, Any] = {}
        self.cookies: Dict[str, str] = {}

        # Исключения и логи ошибок
        self.errors: List[str] = []

        # Куки и сессии
        self.session_data: Dict[str, Any] = {}

        # Перенаправления
        self.redirect_url: Optional[str] = None

        # Данные об аутентификации и авторизации
        self.user_authenticated: bool = False
        self.user_id: Optional[str] = None
        self.auth_token: Optional[str] = None

        # API вызовы и WebSocket соединения
        self.api_calls: List[Dict[str, Any]] = []
        self.websocket_messages: List[Dict[str, Any]] = []

        # Метрики производительности
        self.performance_metrics: Dict[str, Any] = {
            'response_time': None
        }

        # Клиентские данные и окружение пользователя
        self.user_agent: Optional[str] = None
        self.client_ip: Optional[str] = None

        # Взаимодействие с базами данных
        self.sql_queries: List[Dict[str, Any]] = []

        # Поток управления
        self.control_flow: List[Dict[str, Any]] = []

    def serialize_to_dict(self) -> Dict[str, Any]:
        data = {
            'request_method': self.request_method,
            'request_url': self.request_url,
            'request_headers': self.request_headers,
            'request_body': self.request_body,
            'response_status': self.response_status,
            'response_headers': self.response_headers,
            'response_body': self.response_body,
            'query_params': self.query_params,
            'form_params': self.form_params,
            'json_payload': self.json_payload,
            'cookies': self.cookies,
            'errors': self.errors,
            'session_data': self.session_data,
            'redirect_url': self.redirect_url,
            'user_authenticated': self.user_authenticated,
            'user_id': self.user_id,
            'auth_token': self.auth_token,
            'api_calls': self.api_calls,
            'websocket_messages': self.websocket_messages,
            'performance_metrics': self.performance_metrics,
            'user_agent': self.user_agent,
            'client_ip': self.client_ip,
            #'sql_queries': self.sql_queries,
            #'external_services_calls': self.external_services_calls,
            #'suspicious_activity': self.suspicious_activity,
        }

        return data

    def serialize_to_json(self) -> str:
        """
        Сериализация данных в JSON формат.
        """
        data = {
            'request_method': self.request_method,
            'request_url': self.request_url,
            'request_headers': self.request_headers,
            'request_body': self.request_body,
            'response_status': self.response_status,
            'response_headers': self.response_headers,
            'response_body': self.response_body,
            'query_params': self.query_params,
            'form_params': self.form_params,
            'json_payload': self.json_payload,
            'cookies': self.cookies,
            'errors': self.errors,
            'session_data': self.session_data,
            'redirect_url': self.redirect_url,
            'user_authenticated': self.user_authenticated,
            'user_id': self.user_id,
            'auth_token': self.auth_token,
            'api_calls': self.api_calls,
            'websocket_messages': self.websocket_messages,
            'performance_metrics': self.performance_metrics,
            'user_agent': self.user_agent,
            'client_ip': self.client_ip,
            #'sql_queries': self.sql_queries,
            #'external_services_calls': self.external_services_calls,
            #'suspicious_activity': self.suspicious_activity,
        }
        return json.dumps(data, ensure_ascii=False)

    def serialize_to_base64(self) -> str:
        """
        Сериализация данных в JSON формат и кодирование в Base64.
        """
        json_data = self.serialize_to_json()
        base64_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
        return base64_data
