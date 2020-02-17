from greet import api_pb2_grpc
from greet import api_pb2

from core.models import Greet


class Greeter(api_pb2_grpc.GreeterServicer):

    def record_name(self, name):
        Greet.objects.create(name=name)

    def SayHello(self, request, context):
        self.record_name(request.name)
        return api_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        self.record_name(request.name)
        return api_pb2.HelloReply(message='Hello again, %s!' % request.name)
