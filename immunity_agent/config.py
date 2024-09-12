import json
import logging
from immunity_agent.logger import logger_config


logger = logger_config("Immunity settings unit")


class Config:
    """
    Модуль конфигурации агента.
    """
    def __init__(self):
        self.filename = "immunity_agent/config.json"
        self.data = self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError as e:
            logger.error(e)
            return {}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
