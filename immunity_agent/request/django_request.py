"""
Класс для сериализации запросов в фреймворке Django.

Этот модуль предоставляет функциональность для сериализации запросов в фреймворке Django,
что позволяет передавать данные в API для дальнейшего анализа.
"""

import json
from typing import Any, Dict, Union

from immunity_agent.logger import logger_config

logger = logger_config("Immunity Django request handler")


class DjangoRequest:
    """
    Класс, описывающий логику сериализации Django-запросов.

    Этот класс предоставляет методы для преобразования объектов запросов Django в JSON-формат,
    что позволяет отправлять данные в API для последующего анализа.

    :param request: Объект запроса Django.
    :type request: HttpRequest
    """

    @staticmethod
    def serialize_request_item(
        request_components_dict: Dict[str, Union[str, Any]]
    ) -> Dict[str, str]:
        """
        Метод, возвращающий сериализованные компоненты запроса.

        Этот метод преобразовывает значения компонентов запроса в строку и возвращает результат.

        :param request_components_dict: Словарь компонентов запроса.
        :type request_components_dict: Dict[str, Union[str, Any]]
        :return: Сериализованная версия компонентов запроса.
        :rtype: Dict[str, str]
        """
        result = {}
        for key, value in request_components_dict.items():
            result[key] = str(value)
        return result

    @staticmethod
    def serialize(request: object, indentation: int = None) -> str:
        """
        Метод, возвращающий сериализованную версию запроса.

        Этот метод объединяет все компоненты запроса в единый JSON-объект и возвращает его.

        :param request: Объект запроса Django.
        :type request: HttpRequest
        :param indentation: Уровень отступа для форматированного вывода.
        :type indentation: int
        :return: Сериализованный запрос в формате JSON.
        :rtype: str
        """
        return json.dumps(
            {
                "method": request.method,
                "path": request.path,
                "body": str(request.body),
                "headers": DjangoRequest.serialize_request_item(request.headers),
                "user": str(request.user),
                "GET": request.GET.dict(),
                "POST": request.POST.dict(),
                "COOKIES": request.COOKIES,
                "FILES": request.FILES.dict(),
                "META": DjangoRequest.serialize_request_item(request.META),
            },
            indent=indentation,
        )
