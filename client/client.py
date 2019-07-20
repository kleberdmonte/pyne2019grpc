import grpc

import pyne_pb2
import pyne_pb2_grpc

def SayHello(**kwargs):
    with grpc.insecure_channel('pyne:3000') as channel:
        stub = pyne_pb2_grpc.GreeterStub(channel)
        req = pyne_pb2.HelloRequest(**kwargs)
        response = stub.SayHello(req)
        print(response.greetings)


def CalcSum(**kwargs):
    with grpc.insecure_channel('pyne:3000') as channel:
        stub = pyne_pb2_grpc.CalculatorStub(channel)
        req = pyne_pb2.SumRequest(**kwargs)
        response = stub.Sum(req)
        print(f'Result = {response.result}')


def UtcNow(**kwargs):
    with grpc.insecure_channel('pyne:3000') as channel:
        stub = pyne_pb2_grpc.NtpStub(channel)
        req = pyne_pb2.UtcNowRequest(**kwargs)
        
        for response in stub.UtcNow(req):
            print(f'Utc Now = {response.yyMMddHHmmss}')

if __name__ == '__main__':
    # CalcSum(value=(10, -5, 5, 10))
    # SayHello(a='teste', b=25)
    UtcNow(interval_in_secs=1, max_amount=5)

