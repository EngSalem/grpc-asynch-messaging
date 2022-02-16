from concurrent.futures import ThreadPoolExecutor
import logging
import threading
import time
from typing import Iterable
from google.protobuf.json_format import MessageToJson
import grpc
import dummy_pb2 as dummy
import dummy_pb2_grpc as rpc
import yaml
import argparse


class Messaging(rpc.MessagingServiceServicer):
    def __init__(self):
        self.messages = []

    def sendMessage(self, request, context):
        self.messages.append(request)
        return dummy.Empty()

    def getMessage(self, request, context):
        msg = self.messages.pop()
        return msg

def server(address: str) -> None:
    '''
    param address:
    param chatMembers:
    return: None
    '''

    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    ## add group chat members to server
    rpc.add_MessagingServiceServicer_to_server(servicer=rpc.MessagingServiceServicer(), server=server)
    server.add_insecure_port(address)
    server.start()
    server.wait_for_termination()

server("[::]:11912")