from django.dispatch import Signal
from django.db import close_old_connections

grpc_server_init = Signal()
grpc_server_started = Signal()
grpc_server_shutdown = Signal()

grpc_request_started = Signal(providing_args=["request", "context"])
grpc_request_exception = Signal(providing_args=["request", "context", "exception"])
grpc_request_finished = Signal(providing_args=["request", "context"])

grpc_request_started.connect(close_old_connections)
grpc_request_exception.connect(close_old_connections)
grpc_request_finished.connect(close_old_connections)
