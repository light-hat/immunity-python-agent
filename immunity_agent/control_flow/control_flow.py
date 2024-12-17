"""
Модуль для перехвата и обработки потока управления.

Этот модуль предоставляет функционал для отслеживания и сериализации потоков управления
в рамках программного средства интерактивного анализа.
"""

import inspect
import json
import time
from types import FrameType
from typing import Any, Callable, Optional

from immunity_agent.logger import logger_config

logger = logger_config("Immunity control flow handler")


class ControlFlowBuilder:
    """
    Класс, описывающий логику захвата потока управления.

    Этот класс предназначен для отслеживания и сериализации событий в потоке управления программы.

    :param project_root: Корневая директория проекта.
    :type project_root: str
    """

    def __init__(self, project_root: str):
        """
        Конструктор класса.

        Устанавливает корневую директорию проекта и инициализирует необходимые атрибуты.

        :param project_root: Корневая директория проекта.
        :type project_root: str
        """
        self.project_root = project_root
        self.external_call_detected = False
        self.control_flow = []

    def serialize(self, indentation: int = None) -> str:
        """
        Сериализация логики захвата потока управления в формате JSON.

        :param indentation: Количество отступов для форматирования JSON (по умолчанию None).
        :type indentation: int | None
        :return: Строка с сериализованным потоком управления.
        :rtype: str
        """
        return json.dumps(self.control_flow, indent=indentation)

    def serialize_locals(self, local_dict: dict) -> list:
        """
        Сериализация локальных переменных в виде списка словарей.

        :param local_dict: Сырой словарь с локальными переменными.
        :type local_dict: dict
        :return: Список словарей с сериализованными переменными.
        :rtype: list
        """
        serialized = []
        try:
            for var_name, var_value in local_dict.items():
                try:
                    value_str = str(var_value)
                except Exception:  # pylint: disable=broad-except
                    value_str = "<non-serializable>"

                serialized.append(
                    {
                        "name": var_name,
                        "type": type(var_value).__name__,
                        "value": value_str if value_str else "<Non-serializable>",
                    }
                )
        except Exception:  # pylint: disable=broad-except
            serialized.append(str(local_dict))
        return serialized

    def serialize_error(self, error_tuple: tuple) -> dict:
        """
        Сериализация ошибки в виде словаря.

        :param error_tuple: Кортеж с данными об ошибке (тип, сообщение, трассировка стека).
        :type error_tuple: tuple
        :return: Словарь с сериализованной ошибкой.
        :rtype: dict
        """
        return {
            "exception_type": error_tuple[0].__name__,
            "message": str(error_tuple[1]),
        }

    def trace_calls(  # pylint: disable=too-many-statements
        self, frame, event: str, arg
    ) -> Callable[[FrameType, str, Any], Optional[Callable]]:
        """
        Функция-трассировщик для отслеживания вызовов.

        Эта функция будет вызываться перед каждым событием в процессе исполнения программы.
        Она позволяет отслеживать различные события, такие как вызовы функций, выполнение
        строк кода и возврат из функций.

        :param frame: Текущий фрейм выполнения.
        :type frame: types.FrameType
        :param event: Тип события. Возможные значения: 'call', 'line', 'return', 'exception'.
        :type event: str
        :param arg: Дополнительная информация о событии. Например, для события 'return' это
        значение, которое возвращается из функции.
        :type arg: Any
        :return: Новая функция-трассировщик или None, если трассировка больше не требуется.
        :rtype: Optional[Callable[[types.FrameType, str, Any], Optional[Callable]]]
        """
        filename = frame.f_code.co_filename

        if event == "call":
            func_name = frame.f_code.co_name
            func_filename = frame.f_code.co_filename
            func_line_number = frame.f_lineno

            # Проверяем, если вызов происходит в проекте
            if self.project_root in func_filename:
                self.external_call_detected = False
            else:
                if not self.external_call_detected:
                    # Только если внешняя функция не была зарегистрирована ранее
                    module = inspect.getmodule(frame)
                    module_name = module.__name__ if module else "<Unknown>"
                    args = frame.f_locals.copy()
                    self.control_flow.append(
                        {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "event": "external_call",
                            "name": func_name,
                            "module": module_name,
                            "filename": func_filename,
                            "line": func_line_number,
                            "args": self.serialize_locals(args),
                        }
                    )
                    self.external_call_detected = True
                else:
                    self.external_call_detected = False

        if self.project_root in filename:
            if event == "call":
                # Вызов функции
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append(
                    {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "event": "internal_call",
                        "name": func_name,
                        "module": module_name,
                        "filename": func_filename,
                        "line": func_line_number,
                        "args": self.serialize_locals(args),
                    }
                )

                return self.trace_calls

            if event == "line":
                # Выполнение строки кода внутри функции
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno
                code_line = (
                    inspect.getframeinfo(frame).code_context[0].strip()
                    if inspect.getframeinfo(frame).code_context is not None
                    else "None"
                )

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append(
                    {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "event": "code_line",
                        "name": func_name,
                        "module": module_name,
                        "filename": func_filename,
                        "line": func_line_number,
                        "args": self.serialize_locals(args),
                        "code": code_line,
                    }
                )

                return self.trace_calls

            if event == "return":
                # Возврат из функции
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno
                return_value = arg

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append(
                    {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "event": "return",
                        "name": func_name,
                        "module": module_name,
                        "filename": func_filename,
                        "line": func_line_number,
                        "final_state": self.serialize_locals(args),
                        "returned_value": (
                            self.serialize_locals(return_value)
                            if return_value
                            else "None"
                        ),
                    }
                )

                return self.trace_calls

            if event == "exception":
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno
                return_value = arg

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append(
                    {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "event": "error",
                        "source": [
                            {
                                "function": func_name,
                                "module": module_name,
                                "filename": func_filename,
                                "line": func_line_number,
                            }
                        ],
                        "details": self.serialize_error(return_value),
                    }
                )

                return self.trace_calls

            return self.trace_calls

        return self.trace_calls
