import requests
import base64
from immunity_agent.config import Config
import immunity_agent.logger as logger
from immunity_agent.logger import logger_config


logger = logger_config("Immunity API")

class Client:
    """
    Класс клиента для взаимодействия с API.
    """
    def __init__(self):
        self.config = Config()
        self.host = self.config.get('host')
        self.port = self.config.get('port')
        self.project = self.config.get('project')

    def upload_context(self, id, project, request, control_flow, response):
        """
        Загрузка контекста в API.
        """
        url = f'http://{self.host}:{self.port}/api/agent/context/'
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, json={
            'project': project,
            'request': base64.b64encode(request.encode('utf-8')).decode('utf-8'),
            'control_flow': base64.b64encode(control_flow.encode('utf-8')).decode('utf-8'),
            'response': base64.b64encode(response.encode('utf-8')).decode('utf-8'),
        })
        if response.status_code == 200:
            logger.info(f'Данные о запросе {id} отправлены на обработку.')
        else:
            logger.error(f'Сбой отправки данных о запросе {id}. Код ответа: {response.status_code}; Содержимое ответа: {response.text}')
        return response
