from concurrent import futures
from functools import reduce
from datetime import datetime
import time

import time

import grpc

import pyne_pb2
import pyne_pb2_grpc

class Greeter(pyne_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f'{request.name} said Hello.')
        print(f'{request.age} years old.')
        return pyne_pb2.HelloResponse(greetings=f'Hello, {request.name}. I heard you are {request.age}.')


class Calculator(pyne_pb2_grpc.CalculatorServicer):
    def Sum(self, request, context):
        # print(f'a = {request.a}.')
        print(f'value = {request.value}.')

        if len(request.value) > 1:
            result = reduce(lambda x, y: x + y, request.value)
        else:
            result = 0

        return pyne_pb2.SumResponse(result=result)


class Ntp(pyne_pb2_grpc.NtpServicer):
    def UtcNow(self, request, context):
        print(f'Interval = {request.interval_in_secs}.')
        print(f'Max Amount = {request.max_amount}.')

        for _ in range(request.max_amount):
            time.sleep(request.interval_in_secs)

            now = datetime.utcnow()
            format_now = now.strftime('%Y%-M-%d %H:%m:%s')
            print(format_now)

            yield pyne_pb2.UtcNowResponse(yyMMddHHmmss=format_now)
            # yield format_now


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pyne_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    pyne_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
    pyne_pb2_grpc.add_NtpServicer_to_server(Ntp(), server)

    server.add_insecure_port('0.0.0.0:3000')
    server.start()
    print('Waiting for requests...')
    try:
        while True:
            time.sleep(60 * 60 * 24) # One day in seconds.
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
