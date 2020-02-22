"""
Service for grpc_framework.
"""
from importlib import import_module
from inspect import getmembers, isclass, isfunction

from grpc_framework.decorators import signal_deco
from grpc_framework.exceptions import ServiceException


class Service:
    """GrpcService"""

    def __init__(self, app):
        self.app = app
        self.pb_class = []
        self.pb_func = []
        self.pd_module = import_module(self.app + f'.{self.app}_pb2_grpc')
        for mod in getmembers(self.pd_module):
            if isclass(mod[1]) and mod[0].endswith('Servicer'):
                self.pb_class.append(mod[1])
            if isfunction(mod[1]) and mod[0].startswith('add_') and mod[0].endswith('_to_server'):
                self.pb_func.append(mod[1])

    @property
    def service_class(self):
        if len(self.pb_class) != 1:
            raise ServiceException
        service_module = import_module(self.app + '.service')
        service_class = [mod[1] for mod in getmembers(service_module) if
                         isclass(mod[1]) and mod[1] not in self.pb_class]
        pb_class_func_names = [name for name, fn in getmembers(self.pb_class[0]) if isfunction(fn)]
        for service in service_class:
            if issubclass(service, (self.pb_class[0])):
                for name, fn in getmembers(service):
                    if name in pb_class_func_names and isfunction(fn):
                        setattr(service, name, signal_deco(fn))
                return service
        else:
            raise ServiceException

    def find_handler(self):
        if len(self.pb_func) != 1:
            raise ServiceException
        return self.pb_func[0]
