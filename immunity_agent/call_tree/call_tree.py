import sys
import json
import ast
import inspect
import traceback
from immunity_agent.call_tree.node import Node

import matplotlib
matplotlib.use('Agg')

import networkx as nx
import matplotlib.pyplot as plt


class CallTreeBuilder:
    def __init__(self, project_root):
        self.root = None
        self.current_node = None
        self.project_root = project_root
        self.in_library_code = False

        self.nodes = {}

    def trace_calls(self, frame, event, arg):
        filename = frame.f_code.co_filename
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno

        try:

            if not filename.startswith(self.project_root):
                if not self.in_library_code:
                    #######################
                    self.process_call(frame)
                    #######################
                    # Мы зашли в библиотечный код; устанавливаем флаг
                    self.in_library_code = True
                else:
                    # Если уже в библиотечном коде, просто выходим, чтобы игнорировать дальнейшие вызовы
                    return
            else:
                # Если вернулись в пользовательский код, сбрасываем флаг
                self.in_library_code = False

            if self.project_root in filename:
                if event == 'call':
                    self.process_call(frame)

                elif event == 'line':
                    self.process_line(frame)

                elif event == 'return':
                    self.process_return(frame)

        except AttributeError as e:
            print(f"Ignored AttributeError: {e}")

        # Возвращаем саму функцию для продолжения отслеживания
        return self.trace_calls

    def process_call(self, frame):
        func_name = frame.f_code.co_name
        args = frame.f_locals  # Локальные переменные (аргументы функции)

        # Создаем новый узел для функции
        new_node = Node(func_name, args)

        # Если это первый вызов, устанавливаем его корнем
        if self.root is None:
            self.root = new_node
            self.current_node = new_node
        else:
            # Добавляем новый узел как дочерний к текущему узлу
            self.current_node.add_child(new_node)
            # Переходим к новому узлу (новый контекст)
            self.current_node = new_node

    def process_line(self, frame):
        line_no = frame.f_lineno
        filename = frame.f_code.co_filename

        # Получаем исходный код строки
        source_code = inspect.getframeinfo(frame).code_context[0].strip()

        # Разбираем строку в AST
        try:
            tree = ast.parse(source_code, mode='single')
            # Обходим дерево AST и извлекаем информацию о переменных и функциях
            # Для этого можно использовать ast.NodeVisitor или аналогичный метод
            self.analyze_ast(tree, frame)
        except SyntaxError as e:
            print(f"SyntaxError: {e} in line: {source_code}")

    #####################

    def analyze_ast(self, tree, frame):
        # Проходим по AST дерева, чтобы найти вызовы функций и переменные
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self.get_func_name(node)
                args = self.get_func_args(node, frame)

                # Создаем новый узел для вызова функции
                new_node = Node(func_name, args)
                self.node_counter += 1

                self.current_node.add_child(new_node)
                self.current_node = new_node
            elif isinstance(node, ast.Assign):
                # Найдем все переменные, которым происходит присваивание
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        value = self.get_variable_value(var_name, frame)

                        # Создаем новый узел для переменной
                        new_node = Node(f"Assign: {var_name}", {var_name: value})
                        self.node_counter += 1

                        self.current_node.add_child(new_node)
                        self.current_node = new_node

    def get_func_name(self, node):
        # Получаем имя функции из AST узла
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return f"{node.func.value.id}.{node.func.attr}"
        return "unknown"

    def get_func_args(self, node, frame):
        # Извлекаем аргументы функции из AST и текущего фрейма
        args = {}
        for arg in node.args:
            if isinstance(arg, ast.Name):
                arg_name = arg.id
                args[arg_name] = frame.f_locals.get(arg_name, '<unknown>')
            elif isinstance(arg, (ast.Constant, ast.Str, ast.Num)):
                args[str(arg)] = arg.value
        return args

    def get_variable_value(self, var_name, frame):
        # Получаем значение переменной из текущего фрейма
        return frame.f_locals.get(var_name, '<unknown>')

    #########################

    def process_return(self, frame):
        # Переходим к родительскому узлу (возврат из функции)
        if self.current_node.parent is not None:
            self.current_node = self.current_node.parent

    def serialize_to_json(self):
        """Сериализует дерево вызовов в формат JSON."""
        if self.root is not None:
            return json.dumps(self.root.to_dict(), indent=4)
        else:
            return "{}"

    def visualize_with_networkx(self):
        """Создает и визуализирует граф вызовов функций с помощью NetworkX и Matplotlib."""
        if self.root is None:
            print("Дерево вызовов пусто!")
            return

        G = nx.DiGraph()

        # Рекурсивная функция для добавления узлов и рёбер в граф
        def add_nodes_edges(node):
            G.add_node(node.func_name, label=f"{node.func_name}({', '.join([str(k) + '=' + str(v) for k, v in node.args.items()])})")
            for child in node.children:
                G.add_edge(node.func_name, child.func_name)
                add_nodes_edges(child)

        # Строим граф
        add_nodes_edges(self.root)

        # Рисуем граф
        pos = nx.spring_layout(G)
        labels = nx.get_node_attributes(G, 'label')
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=900, node_color='teal', font_size=7, font_weight='bold', edge_color='gray')
        plt.title("Call Graph")
        plt.figure(figsize=(20,20))
        plt.savefig("D:\\graph.png")
