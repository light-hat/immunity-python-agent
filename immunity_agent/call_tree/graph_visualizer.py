import networkx as nx
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use('Agg')


class GraphVisualizer:
    def __init__(self, graph):
        self.dfg_data = graph

    def visualize(self, output_path="D:\graph.png"):

        G = nx.DiGraph()

        for func_name, node_data in self.dfg_data.items():
            # Добавляем узлы
            G.add_node(func_name)

            # Добавляем рёбра (переменные)
            for var_name, caller_func in node_data['inputs'].items():
                if caller_func:
                    G.add_edge(caller_func, func_name, label=var_name)

            for var_name, called_func in node_data['outputs'].items():
                if called_func:
                    G.add_edge(func_name, called_func, label=var_name)

        pos = nx.spring_layout(G, seed=42)

        plt.figure(figsize=(12, 8))

        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue')
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

        # Рисуем рёбра
        nx.draw_networkx_edges(G, pos, arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        plt.title('Data Flow Graph with Variables')

        # Сохранение графика в файл
        plt.savefig(output_path)
        print(f"Graph saved to {output_path}")

    '''def visualize(self):
        G = nx.DiGraph()

        for func_name, node_data in self.dfg_data.items():
            # Добавляем узлы
            G.add_node(func_name)

            # Добавляем рёбра (переменные)
            for var_name, caller_func in node_data['inputs'].items():
                if caller_func:
                    G.add_edge(caller_func, func_name, label=var_name)

            for var_name, called_func in node_data['outputs'].items():
                if called_func:
                    G.add_edge(func_name, called_func, label=var_name)

        pos = nx.spring_layout(G, seed=42)  # Определение расположения узлов
        plt.figure(figsize=(12, 8))

        # Рисуем узлы
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue')
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

        # Рисуем рёбра
        nx.draw_networkx_edges(G, pos, arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        plt.title('Data Flow Graph with Variables')
        plt.show()'''
