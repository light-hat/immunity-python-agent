from immunity_agent.control_flow import ControlFlowBuilder
from immunity_agent.logger import logger_config
from immunity_agent.request.django_request import DjangoRequest
from immunity_agent.response.django_response import DjangoResponse
from immunity_agent.api.client import Client
from django.conf import settings
import sys


logger = logger_config("Immunity Django middleware")

class ImmunityDjangoMiddleware:
    """
    Промежуточное ПО для инструментирования фреймворка Django.
    """
    def __init__(self, get_response):
        """
        Конструктор.
        """
        self.get_response = get_response
        self.api_client = Client()
        self.project = self.api_client.project
        logger.info('Агент Immunity IAST активирован.')

    def __call__(self, request):
        """
        Переопределяем метод вызова.
        :param request: Объект запроса.
        :return: Ответ.
        """
        logger.info(f'Отслеживаю запрос {request.path}')
        self.control_flow = ControlFlowBuilder(project_root=str(settings.BASE_DIR))
        sys.settrace(self.control_flow.trace_calls)

        response = self.get_response(request)

        sys.settrace(None)

        #print(DjangoRequest.serialize(request)) # DEBUG PRINT
        #print(self.control_flow.serialize()) # DEBUG PRINT
        #print(DjangoResponse.serialize(response)) # DEBUG PRINT

        self.api_client.upload_context(
            request.path,
            self.project,
            DjangoRequest.serialize(request),
            self.control_flow.serialize(),
            DjangoResponse.serialize(response)
        )

        return response
