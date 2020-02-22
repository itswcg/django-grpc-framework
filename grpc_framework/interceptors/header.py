"""
SetHead interceptor
"""
import grpc


def _unary_unary_rpc_terminator(code, details):
    def terminate(request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class SetHeaderInterceptor(grpc.ServerInterceptor):
    """SetHeaderInterceptor"""

    def __init__(self, header, value):
        self._header = header
        self._value = value
        self._terminate = _unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, 'Not set header')

    def intercept_service(self, continuation, handler_call_details):
        if (self._header, self._value) in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._terminate
