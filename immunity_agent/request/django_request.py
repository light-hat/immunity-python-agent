import json
from immunity_agent.logger import logger_config


logger = logger_config("Immunity Django request handler")


class DjangoRequest:
    """
    Класс, описывающий логику сериализации Django-запроса.
    """

    @staticmethod
    def serialize_request_item(components_dict):
        """
        Метод, возвращающий сериализованное поле запроса
        (заголовки, метаданные и т.д., то что с ходу не лезет в json).
        """
        result = {}
        for key, value in components_dict.items():
            result[key] = str(value)
        return result

    @staticmethod
    def serialize(request, indentation=None):
        """
        Метод, возвращающий сериализованный запрос.
        """
        return json.dumps({
            'method': request.method,
            'path': request.path,
            'body': str(request.body),
            'headers': DjangoRequest.serialize_request_item(request.headers),
            'user': str(request.user),
            'GET': request.GET.dict(),
            'POST': request.POST.dict(),
            'COOKIES': request.COOKIES,
            'FILES': request.FILES.dict(),
            'META': DjangoRequest.serialize_request_item(request.META),
        }, indent=indentation)
