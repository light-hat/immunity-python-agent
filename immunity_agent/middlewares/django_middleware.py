from immunity_agent.control_flow import ControlFlowBuilder
from immunity_agent.context import DataCollector, DataBuilder
from django.conf import settings
import sys


class ImmunityDjangoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        #self.data_collector = DataCollector()
        #self.control_flow = ControlFlowBuilder()

        #self.tree_builder = CallTreeBuilder(project_root=str(settings.BASE_DIR))
        self.control_flow = ControlFlowBuilder(project_root=str(settings.BASE_DIR))

        sys.settrace(self.control_flow.trace_calls)

        response = self.get_response(request)

        #builder = DataBuilder(request, response)
        #collector = builder.build()
        # = collector.serialize_to_json()
        #print(collector.serialize_to_dict())
        #print(collector.serialize_to_json())

        sys.settrace(None)

        #call_tree_json = self.tree_builder.serialize_to_json()
        #print("\nJSON Representation:\n", call_tree_json)

        # Визуализация графа вызовов
        #self.tree_builder.visualize_with_networkx()

        return response
