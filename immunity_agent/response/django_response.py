"""
Класс для сериализации ответов в фреймворке Django.

Этот модуль предоставляет функциональность для сериализации ответов в фреймворке Django,
что позволяет передавать данные в API для дальнейшего анализа.
"""

import json
from typing import Any, Dict, Union

from django.http import HttpResponse

from immunity_agent.logger import logger_config

logger = logger_config("Immunity Django response handler")


class DjangoResponse:
    """
    Класс, описывающий логику сериализации Django-ответов.

    Этот класс предоставляет методы для преобразования объектов ответов Django в JSON-формат,
    что позволяет отправлять данные в API для последующего анализа.

    :param response: Объект ответа Django.
    :type response: HttpResponse
    """

    @staticmethod
    def serialize_response_item(
        response_components_dict: Dict[str, Union[str, Any]]
    ) -> Dict[str, str]:
        """
        Метод, возвращающий сериализованные компоненты ответа.

        Этот метод преобразовывает значения компонентов ответа в строку и возвращает результат.

        :param response_components_dict: Словарь компонентов ответа.
        :type response_components_dict: Dict[str, Union[str, Any]]
        :return: Сериализованная версия компонентов ответа.
        :rtype: Dict[str, str]
        """
        result = {}
        for key, value in response_components_dict.items():
            result[key] = str(value)
        return result

    @staticmethod
    def serialize(response: HttpResponse, indentation: int = None) -> str:
        """
        Метод, возвращающий сериализованную версию ответа.

        Этот метод объединяет все компоненты ответа в единый JSON-объект и возвращает его.

        :param response: Объект ответа Django.
        :type response: HttpResponse
        :param indentation: Уровень отступа для форматированного вывода.
        :type indentation: int
        :return: Сериализованный ответ в формате JSON.
        :rtype: str
        """
        return json.dumps(
            {
                "status": response.status_code,
                "headers": DjangoResponse.serialize_response_item(response.headers),
                "body": str(response.content),
                "content_type": response.get("content-type"),
                "content_length": response.get("content-length"),
                "charset": response.get("charset"),
                "version": response.get("version"),
                "reason_phrase": response.reason_phrase,
                "cookies": DjangoResponse.serialize_response_item(response.cookies),
                "streaming": response.streaming,
            },
            indent=indentation,
        )
