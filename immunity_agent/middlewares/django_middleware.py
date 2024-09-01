from immunity_agent.call_tree import CallTreeBuilder
from django.conf import settings
import sys


class ImmunityDjangoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.tree_builder = CallTreeBuilder(project_root=str(settings.BASE_DIR))

    def __call__(self, request):
        sys.settrace(self.tree_builder.trace_calls)

        response = self.get_response(request)

        sys.settrace(None)

        call_tree_json = self.tree_builder.serialize_to_json()
        print("\nJSON Representation:\n", call_tree_json)

        # Визуализация графа вызовов
        self.tree_builder.visualize_with_networkx()

        return response
