import types
from functools import wraps

from grpc_framework.signals import grpc_request_started, grpc_request_finished, grpc_request_exception


class DecoMeta(type):
    def __new__(cls, name, bases, attrs):

        for attr_name, attr_value in attrs.iteritems():
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = cls.deco(attr_value)

        return super(DecoMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def deco(cls, func):
        def wrapper(*args, **kwargs):
            print("before", func.func_name)
            result = func(*args, **kwargs)
            print("after", func.func_name)
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
            raise
        else:
            grpc_request_finished.send(None, request=args[0], context=args[1])
        return response

    return inner


deco_meta = DecoMeta
