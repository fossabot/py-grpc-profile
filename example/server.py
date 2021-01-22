import logging
import time
from concurrent import futures

import grpc
from example.echo.echo_pb2 import EchoMessage
from example.echo.echo_pb2_grpc import EchoServicer, add_EchoServicer_to_server

from py_grpc_profile.server.interceptor import ProfileInterceptor


class EchoService(EchoServicer):
    def Echo(self, request, context):
        logging.info(f"start: {self.__class__.__name__}")
        time.sleep(1)
        logging.info(f"finish: {self.__class__.__name__}")
        return EchoMessage(msg=request.msg)


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[ProfileInterceptor()],
    )
    add_EchoServicer_to_server(EchoService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
