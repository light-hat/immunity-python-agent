"""
Модуль клиента для взаимодействия с API управляющего сервера.

Этот модуль предоставляет функциональность для загрузки контекстных данных
в API управляющего сервера программного средства интерактивного анализа.
"""

import base64

import requests

from immunity_agent.config import Config
from immunity_agent.logger import logger_config

logger = logger_config("Immunity API")


class Client:  # pylint: disable=too-few-public-methods
    """
    Класс клиента для взаимодействия с API управляющего сервера.

    Этот класс предоставляет методы для отправки данных в API.

    :param host: Хост сервера API.
    :type host: str
    :param port: Порт сервера API.
    :type port: int
    :param project: Название проекта.
    :type project: str
    """

    def __init__(self):
        """
        Конструктор класса.

        Инициализирует конфигурацию и устанавливает параметры подключения.
        """
        self.config = Config()
        self.host = self.config.get("host")
        self.port = self.config.get("port")
        self.project = self.config.get("project")

    def upload_context(  # pylint: disable=too-many-arguments, too-many-positional-arguments
            self,
            endpoint: str,
            project: str,
            request: str,
            control_flow: str,
            response: str,
    ) -> requests.Response:
        """
        Отправка контекста в API.

        Метод кодирует данные запроса, потока управления и ответа в Base64 и
        отправляет их на сервер.

        :param endpoint: Адрес перехваченного запроса.
        :type endpoint: str
        :param project: Проект, к которому относится запрос.
        :type project: str
        :param request: Запрос в формате HTTP.
        :type request: str
        :param control_flow: Контрольный поток выполнения.
        :type control_flow: str
        :param response: Ответ от сервера в формате HTTP.
        :type response: str
        :return: Объект Response от библиотеки `requests`.
        :rtype: requests.Response
        :raises requests.exceptions.RequestException: В случае ошибки при выполнении HTTP-запроса.
        """
        url = f"http://{self.host}:{self.port}/api/agent/context/"
        headers = {"Content-Type": "application/json"}

        try:
            # flowchart: start
            response = requests.post(
                url,
                headers=headers,
                json={
                    "project": project,
                    "request": base64.b64encode(request.encode("utf-8")).decode(
                        "utf-8"
                    ),
                    "control_flow": base64.b64encode(
                        control_flow.encode("utf-8")
                    ).decode("utf-8"),
                    "response": base64.b64encode(response.encode("utf-8")).decode(
                        "utf-8"
                    ),
                },
                timeout=15,
            )
            if response.status_code == 200:
                logger.info(f"Данные о запросе {endpoint} отправлены на обработку.")
            else:
                logger.error(
                    f"Сбой отправки данных о запросе {endpoint}. "
                    f"Код ответа: {response.status_code}; "
                    f"Содержимое ответа: {response.text}"
                )
            return response  # flowchart: end
        except requests.exceptions.RequestException as e:
            logger.exception(
                f"Произошла ошибка при отправке данных о запросе {endpoint}"
            )
            raise e

    def upload_dependencies(  # pylint: disable=too-many-arguments, too-many-positional-arguments
            self,
            dependencies_json: str,
            project: str
    ) -> requests.Response:
        """
        Отправка библиотек анализируемого проекта в API.

        Метод кодирует данные о библиотеках проекта в Base64 и
        отправляет их на сервер.

        :param dependencies_json: Сериализованные в JSON данные.
        :type dependencies_json: str
        :param project: Проект, к которому относится запрос.
        :type project: str
        :raises requests.exceptions.RequestException: В случае ошибки при выполнении HTTP-запроса.
        """
        url = f"http://{self.host}:{self.port}/api/agent/dependencies/"
        headers = {"Content-Type": "application/json"}

        try:
            # flowchart: start
            response = requests.post(
                url,
                headers=headers,
                json={
                    "project": project,
                    "payload": base64.b64encode(dependencies_json.encode("utf-8")).decode(
                        "utf-8"
                    ),
                },
                timeout=15,
            )
            if response.status_code == 200:
                logger.info(f"Данные о настройках успешно отправлены.")
            else:
                logger.error(
                    f"Сбой отправки данных о настройках"
                    f"Код ответа: {response.status_code}; "
                    f"Содержимое ответа: {response.text}"
                )
            return response  # flowchart: end
        except requests.exceptions.RequestException as e:
            logger.exception(
                f"Произошла ошибка при отправке данных о настройках"
            )
            raise e

    def upload_config(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        self,
        config_json: str,
        project: str,
        framework: str
    ) -> requests.Response:
        """
        Отправка конфигурации анализируемого проекта в API.

        Метод кодирует данные о конфигурации проекта в Base64 и
        отправляет их на сервер.

        :param config_json: Адрес перехваченного запроса.
        :type config_json: str
        :param project: Проект, к которому относится запрос.
        :type project: str
        :param framework: Имя фреймворка.
        :type framework: str
        :raises requests.exceptions.RequestException: В случае ошибки при выполнении HTTP-запроса.
        """
        url = f"http://{self.host}:{self.port}/api/agent/config/"
        headers = {"Content-Type": "application/json"}

        try:
            # flowchart: start
            response = requests.post(
                url,
                headers=headers,
                json={
                    "project": project,
                    "payload": base64.b64encode(config_json.encode("utf-8")).decode(
                        "utf-8"
                    ),
                    "framework": framework
                },
                timeout=15,
            )
            if response.status_code == 200:
                logger.info(f"Данные о настройках успешно отправлены.")
            else:
                logger.error(
                    f"Сбой отправки данных о настройках"
                    f"Код ответа: {response.status_code}; "
                    f"Содержимое ответа: {response.text}"
                )
            return response # flowchart: end
        except requests.exceptions.RequestException as e:
            logger.exception(
                f"Произошла ошибка при отправке данных о настройках"
            )
            raise e
