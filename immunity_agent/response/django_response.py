import json
import logging
from immunity_agent.logger import logger_config


logger = logger_config("Immunity Django response handler")


class DjangoResponse:
    """
    Класс, описывающий логику сериализации Django-ответа.
    """

    @staticmethod
    def serialize_response_item(components_dict):
        """
        Метод, возвращающий сериализованное поле запроса
        (заголовки, метаданные и т.д., то что с ходу не лезет в json).
        """
        result = {}
        for key, value in components_dict.items():
            result[key] = str(value)
        return result

    @staticmethod
    def serialize(response, indentation=None):
        """
        Метод, возвращающий сериализованный ответ.
        """
        return json.dumps({
            'status': response.status_code,
            'headers': DjangoResponse.serialize_response_item(response.headers),
            'body': str(response.content),
            'content_type': response.get('content-type'),
            'content_length': response.get('content-length'),
            'charset': response.get('charset'),
            'version': response.get('version'),
            'reason_phrase': response.reason_phrase,
            'cookies': DjangoResponse.serialize_response_item(response.cookies),
            'streaming': response.streaming,
        }, indent=indentation)
