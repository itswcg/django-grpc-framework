import logging

import grpc

logger = logging.getLogger('grpc.server')


class LoggerInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        logger.info(handler_call_details.method)
        return continuation(handler_call_details)
