import json
import types


class Node:
    def __init__(self, func_name, args=None):
        self.func_name = func_name  # Имя функции
        self.args = self.sanitize_args(args) if args else {}  # Аргументы функции
        self.children = []  # Дочерние узлы
        self.parent = None  # Родительский узел

        self.inputs = {}   # Входящие переменные (ребра)
        self.outputs = {}  # Исходящие переменные (ребра)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_input(self, var_name, caller_func):
        self.inputs[var_name] = caller_func

    def add_output(self, var_name, called_func):
        self.outputs[var_name] = called_func

    def to_dict(self):
        def serialize_value(value):
            # Преобразуем значение в строку, если это не серийное
            if isinstance(value, (str, int, float, bool, type(None))):
                return value
            elif isinstance(value, (dict, list)):
                return json.dumps(value, default=str)
            else:
                try:
                    return str(value)
                except Exception:
                    return '<unserializable>'

        return {
            'func_name': self.func_name,
            'args': {k: serialize_value(v) for k, v in self.args.items()},
            'children': [child.to_dict() for child in self.children],
            'inputs': self.inputs,
            'outputs': self.outputs,
        }

    def sanitize_args(self, args):
        """Обрабатывает аргументы функции, чтобы сделать их сериализуемыми в JSON."""
        sanitized_args = {}
        for key, value in args.items():
            try:
                # Попробуем напрямую сериализовать в JSON (проверяем примитивные типы)
                json.dumps(value)
                sanitized_args[key] = value
            except (TypeError, OverflowError):
                # Если значение не сериализуемо, приводим его к строке
                sanitized_args[key] = str(value)
        return sanitized_args

    def __repr__(self):
        return f"Node(func_name={self.func_name}, args={self.args}, children={self.children})"

    def serialize_to_json(self):
        return json.dumps(self.to_dict(), indent=4)
