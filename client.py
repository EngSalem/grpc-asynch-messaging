import grpc
import dummy_pb2 as dummy
import dummy_pb2_grpc as rpc
import argparse
import os
import threading

class Client:
    def __init__(self, id, message):
        self.msg = dummy.TextMessage()
        self.msg.sender_id = id
        self.msg.message = message

        channel = grpc.insecure_channel('localhost:11912')
        ## defining the stub for communication
        self.conn = rpc.MessagingServiceStub(channel)

    def send_message(self):
        self.conn.sendMessage(self.msg)

        print('message sent '+ self.msg.message)


client = Client('1', 'Hello World!')

print('message sent successfully')
