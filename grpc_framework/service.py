import logging

from importlib import import_module
from inspect import getmembers, isclass, isfunction

logger = logging.getLogger('grpc.request')


class Service:
    """Service"""

    def __init__(self, app):
        self.app = app
        self.pb_class = []
        self.pb_func = []
        self.pd_module = import_module(self.app + '.api_pb2_grpc')
        for mod in getmembers(self.pd_module):
            if isclass(mod[1]) and mod[0].endswith('Servicer'):
                self.pb_class.append(mod[1])
            if isfunction(mod[1]) and mod[0].startswith('add_') and mod[0].endswith('_to_server'):
                self.pb_func.append(mod[1])

    @property
    def service_class(self):
        if len(self.pb_class) != 1:
            raise Exception
        service_module = import_module(self.app + '.service')
        service_class = [mod[1] for mod in getmembers(service_module) if
                         isclass(mod[1]) and mod[1] not in self.pb_class]
        for service in service_class:
            if issubclass(service, (self.pb_class[0])):
                return service()
        else:
            raise Exception

    def find_handler(self):
        if len(self.pb_func) != 1:
            raise
        return self.pb_func[0]
