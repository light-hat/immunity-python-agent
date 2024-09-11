import sys
import json
import ast
import inspect
import traceback
#from immunity_agent.control_flow.node import Node

#import networkx as nx
#import matplotlib.pyplot as plt


class ControlFlowBuilder:
    def __init__(self, project_root):
        self.project_root = project_root
        self.external_call_detected = False

    def trace_calls(self, frame, event, arg):
        filename = frame.f_code.co_filename

        if event == 'call':
            filename = frame.f_code.co_filename
            func_name = frame.f_code.co_name
            line_no = frame.f_lineno

            # Проверяем, если вызов происходит в проекте
            if self.project_root in filename:
                # Если это функция из вашего проекта, сбрасываем флаг
                self.external_call_detected = False
            else:
                if not self.external_call_detected:
                    # Только если внешняя функция не была зарегистрирована ранее
                    module = inspect.getmodule(frame)
                    module_name = module.__name__ if module else "Unknown"
                    print(f"External call: {func_name}() in {module_name} - {filename}:{line_no}")
                    self.external_call_detected = True

        if self.project_root in filename:
            if event == 'call':
                # Вызов функции
                code = frame.f_code
                func_name = code.co_name
                func_filename = code.co_filename
                func_lineno = code.co_firstlineno

                print(f"Calling function {func_name} in {func_filename}:{func_lineno}")

                vars = frame.f_locals.copy()
                #print("ARGS" + str(vars)) # !!!

                return self.trace_calls  # Продолжаем отслеживать внутри функции

            elif event == 'line':
                # Выполнение строки кода внутри функции
                code = frame.f_code
                func_name = code.co_name
                line_no = frame.f_lineno
                filename = code.co_filename
                code_line = inspect.getframeinfo(frame).code_context[0].strip()

                print(f"Executing line {line_no} in function {func_name} of file {filename}; line: {code_line}")

                vars = frame.f_locals.copy()
                #print("STATE" + str(vars))

                return self.trace_calls  # Продолжаем отслеживать следующие строки

            elif event == 'return':
                # Возврат из функции
                code = frame.f_code
                func_name = code.co_name
                func_filename = code.co_filename
                func_lineno = frame.f_lineno
                return_value = arg

                print(f"Returning from {func_name} in {func_filename}:{func_lineno} with value {return_value}")

                vars = frame.f_locals.copy()
                print("FINAL VARS" + str(vars))

                return None  # Прекращаем отслеживание этой функции

            else:
                print("Обнаружен exception " + str(event))
