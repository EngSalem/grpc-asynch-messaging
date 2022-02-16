import grpc
import dummy_pb2 as dummy
import dummy_pb2_grpc as rpc
import argparse
import os
import threading

class Client:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:11912')
        ## defining the stub for communication
        self.conn = rpc.MessagingServiceStub(channel)

    def receive_messages(self):
        for msg in self.conn.getMessage(dummy.Empty()):
            print(msg.message)


client = Client()
client.receive_messages()


