from greet import greet_pb2
from greet import greet_pb2_grpc

from core.models import Greet


class Greeter(greet_pb2_grpc.GreeterServicer):

    def record_name(self, name):
        Greet.objects.create(name=name)

    def SayHello(self, request, context):
        self.record_name(request.name)
        return greet_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        self.record_name(request.name)
        return greet_pb2.HelloReply(message='Hello again, %s!' % request.name)
