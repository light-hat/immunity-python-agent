"""
Модуль, отвечающий за запуск агента из консоли.

Парсит аргументы командной строки, устанавливает конфигурацию агента,
выводит новую конфигурацию на экран.
"""

import argparse

from immunity_agent.config import Config

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        "Immunity IAST Python agent. Вызов из консоли используется для конфигурации агента."
    )
    parser.add_argument("host", help="Хост серверной части IAST")
    parser.add_argument("port", help="Порт, на котором она хостится")
    parser.add_argument("project_name", help="Имя проекта")
    args = parser.parse_args()

    config = Config()
    config.set("host", args.host)
    config.set("port", args.port)
    config.set("project", args.project_name)

    print("Новая конфигурация:")
    print("Хост серверной части:", args.host)
    print("Порт серверной части:", args.port)
    print("Имя проекта:", args.project_name)
