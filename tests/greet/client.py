import grpc
from greet import api_pb2_grpc
from greet import api_pb2


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = api_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(api_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)
    response = stub.SayHelloAgain(api_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
