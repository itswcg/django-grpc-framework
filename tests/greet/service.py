from greet import api_pb2_grpc
from greet import api_pb2


class Greeter(api_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return api_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return api_pb2.HelloReply(message='Hello again, %s!' % request.name)
