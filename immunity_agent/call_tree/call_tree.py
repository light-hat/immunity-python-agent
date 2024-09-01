import sys
import json
from immunity_agent.call_tree.node import Node

import networkx as nx
import matplotlib.pyplot as plt


class CallTreeBuilder:
    def __init__(self, project_root):
        self.root = None
        self.current_node = None
        self.project_root = project_root
        self.in_library_code = False

    '''def trace_calls(self, frame, event, arg):
        filename = frame.f_code.co_filename
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno

        try:

            if not filename.startswith(self.project_root):
                if not self.in_library_code:
                    #######################
                    func_name = frame.f_code.co_name
                    args = frame.f_locals  # Локальные переменные (аргументы функции)

                    # Создаем новый узел для функции
                    new_node = Node(func_name, args)

                    # Если это первый вызов, устанавливаем его корнем
                    if not self.root is None:
                        # Добавляем новый узел как дочерний к текущему узлу
                        self.current_node.add_child(new_node)
                        # Переходим к новому узлу (новый контекст)
                        self.current_node = new_node
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

                elif event == 'return':
                    # Переходим к родительскому узлу (возврат из функции)
                    if self.current_node.parent is not None:
                        self.current_node = self.current_node.parent

        except AttributeError as e:
            print(f"Ignored AttributeError: {e}")

        # Возвращаем саму функцию для продолжения отслеживания
        return self.trace_calls'''

    def trace_calls(self, frame, event, arg):
        filename = frame.f_code.co_filename
        func_name = frame.f_code.co_name

        # Пропуск кода, не относящегося к проекту
        if not filename.startswith(self.project_root):
            return

        if func_name not in self.nodes:
            self.nodes[func_name] = Node(func_name)

        if event == 'call':
            caller_frame = frame.f_back
            caller_func_name = caller_frame.f_code.co_name if caller_frame else None

            # Сохранение входящих переменных
            local_vars = caller_frame.f_locals if caller_frame else {}
            for var_name, var_value in local_vars.items():
                self.nodes[func_name].add_input(var_name, caller_func_name)
                if caller_func_name in self.nodes:
                    self.nodes[caller_func_name].add_output(var_name, func_name)

        elif event == 'return':
            # Здесь можно обработать возврат, чтобы отслеживать изменения переменных
            pass

        return self.trace_calls

    def to_dict(self):
        return {func_name: node.to_dict() for func_name, node in self.nodes.items()}

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
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
        plt.title("Call Graph")
        plt.show()
