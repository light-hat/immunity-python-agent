import json
import inspect
import logging
from immunity_agent.logger import logger_config


logger = logger_config("Immunity control flow handler")


class ControlFlowBuilder:
    """
    Класс, описывающий логику захвата потока управления.
    """
    def __init__(self, project_root):
        """
        Конструктор класса.
        :param project_root: Корневая директория проекта.
        """
        self.project_root = project_root
        self.external_call_detected = False
        self.control_flow = list()

    def serialize(self, indentation=None):
        """
        Сериализует логику захвата потока управления в формате JSON.
        :param indentation: Количество отступов для индентификации (необязательный).
        :return: Строка с сериализованной логикой захвата потока управления.
        """
        return json.dumps(self.control_flow, indent=indentation)

    def serialize_locals(self, local_dict):
        """
        Сериализует локальные переменные в виде списка словарей.
        :param local_dict: Сырой словарь с локальными переменными.
        :return: Словарь с сериализованными переменными.
        """
        serialized = []
        for var_name, var_value in local_dict.items():
            try:
                value_str = str(var_value)
            except Exception:
                value_str = "<non-serializable>"

            serialized.append({
                "name": var_name,
                "type": type(var_value).__name__,
                "value": value_str if value_str else "<Non-serializable>"
            })
        return serialized

    def serialize_error(self, error_tuple):
        """
        Сериализует ошибку в виде словаря.
        :param error_tuple: Кортеж с данными об ошибке
        (тип, сообщение, трассировка стека).
        :return: Словарь с сериализованной ошибкой.
        """
        return {
            "exception_type": error_tuple[0].__name__,
            "message": str(error_tuple[1]),
        }

    def trace_calls(self, frame, event, arg): # todo: refactor
        """
        Переопределяем метод трассировки вызовов.
        :param frame: Фрейм (содержит необходимую информацию о текущем вызове)
        :param event: Тип события
        :param arg: Параметры вызова
        :return: Функция трассировки вызовов (саму себя).
        """
        filename = frame.f_code.co_filename

        if event == 'call':
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
                    self.control_flow.append({
                        "event": "function",
                        "type": "external_call",
                        "name": func_name,
                        "module": module_name,
                        "filename": func_filename,
                        "line": func_line_number,
                        "args": self.serialize_locals(args),
                    })
                    self.external_call_detected = True

        if self.project_root in filename:
            if event == 'call':
                # Вызов функции
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append({
                    "event": "function",
                    "type": "internal_call",
                    "name": func_name,
                    "module": module_name,
                    "filename": func_filename,
                    "line": func_line_number,
                    "args": self.serialize_locals(args),
                })

                return self.trace_calls

            elif event == 'line':
                # Выполнение строки кода внутри функции
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno
                code_line = inspect.getframeinfo(frame).code_context[0].strip()

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append({
                    "event": "code",
                    "type": "execution",
                    "name": func_name,
                    "module": module_name,
                    "filename": func_filename,
                    "line": func_line_number,
                    "args": self.serialize_locals(args),
                    "code": code_line,
                })

                return self.trace_calls

            elif event == 'return':
                # Возврат из функции
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno
                return_value = arg

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append({
                    "event": "code",
                    "type": "execution",
                    "name": func_name,
                    "module": module_name,
                    "filename": func_filename,
                    "line": func_line_number,
                    "final_state": self.serialize_locals(args), # final state
                    "returned_value": self.serialize_locals(return_value) if return_value else "None",
                })

                return self.trace_calls

            elif event == 'exception':
                func_name = frame.f_code.co_name
                func_filename = frame.f_code.co_filename
                func_line_number = frame.f_lineno
                return_value = arg

                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "<Unknown>"
                args = frame.f_locals.copy()
                self.control_flow.append({
                    "event": "error",
                    "type": "exception",
                    "source": [{
                        "function": func_name,
                        "module": module_name,
                        "filename": func_filename,
                        "line": func_line_number,
                    }],
                    "details": self.serialize_error(return_value),
                })

            return self.trace_calls

        return self.trace_calls
