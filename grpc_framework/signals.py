"""
Signal for grpc_framework
"""
from django.dispatch import Signal
from django.db import close_old_connections

# server signal
grpc_server_init = Signal(providing_args=["server"])
grpc_server_started = Signal(providing_args=["server"])
grpc_server_shutdown = Signal(providing_args=["server"])

# request signal
grpc_request_started = Signal(providing_args=["request", "context"])
grpc_request_exception = Signal(providing_args=["request", "context", "exception"])
grpc_request_finished = Signal(providing_args=["request", "context"])

# close old connections every request
grpc_request_started.connect(close_old_connections)
grpc_request_exception.connect(close_old_connections)
grpc_request_finished.connect(close_old_connections)
