from concurrent import futures
import grpc

from grpc_framework.settings import grpc_settings
from grpc_framework.service import Service


class GrpcServer:
    """GrpcServer"""

    def __init__(self, max_workers=5,
                 handlers=None,
                 interceptors=None,
                 options=None,
                 maximum_concurrent_rpcs=None,
                 compression=None):
        self.interceptors = interceptors or self.add_interceptors()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), handlers,
                                  self.interceptors, options,
                                  maximum_concurrent_rpcs, compression)

    def add_interceptors(self):
        pass

    def run(self, address, port, *args, **kwargs):
        self.add_services()
        self.server.add_insecure_port(f'{address}:{port}')
        self.server.start()
        self.server.wait_for_termination()

    def add_services(self):
        grpc_apps = grpc_settings.grpc_apps
        for grpc_app in grpc_apps:
            service = Service(grpc_app)
            handler = service.find_handler()
            handler(service.service_class(), self.server)
