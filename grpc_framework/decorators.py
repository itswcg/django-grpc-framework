"""
grpc_framework decorators.
"""
from functools import wraps
import types
import time

from grpc_framework.signals import grpc_request_started, grpc_request_finished, grpc_request_exception
from grpc_framework.utils.log import log_response


class DecoMeta(type):
    def __new__(cls, name, bases, attrs):

        for attr_name, attr_value in attrs.iteritems():
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = cls.deco(attr_value)

        return super(DecoMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def deco(cls, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper


def signal_deco(func):
    if func is None:
        return

    @wraps(func)
    def inner(*args, **kwargs):
        grpc_request_started.send(None, request=args[0], context=args[1])
        try:
            response = func(*args, **kwargs)
        except Exception as exc:
            grpc_request_exception.send(None, request=args[0], context=args[1], exception=exc)
            raise exc
        else:
            grpc_request_finished.send(None, request=args[0], context=args[1])
        return response

    return inner


def log_deco(func):
    if func is None:
        return

    @wraps(func)
    def inner(*args, **kwargs):
        code = 'success'
        start_time = time.time()
        handler_call_details = args[2]

        try:
            results = func(*args, **kwargs)
        except Exception as exc:
            code = 'error'
            raise exc
        finally:
            resp_time = round(((time.time() - start_time)) * 1000)
            response = {
                'code': code,
                'resp_time': resp_time
            }
            log_response(handler_call_details.method, response)
        return results

    return inner


deco_meta = DecoMeta
