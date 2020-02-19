import logging

import grpc

logger = logging.getLogger('grpc.request')


class LoggerInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        logger.info(handler_call_details)
        return continuation(handler_call_details)
