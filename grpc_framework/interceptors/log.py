"""
log interceptor
"""
import grpc
from grpc_framework.decorators import log_deco


class LoggerInterceptor(grpc.ServerInterceptor):

    @log_deco
    def intercept_service(self, continuation, handler_call_details):
        return continuation(handler_call_details)
