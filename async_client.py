import asyncio
import logging
import random
from typing import Iterable, List

import grpc
import dummy_pb2
import dummy_pb2_grpc

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ids', action='store', dest='member_ids',
                    help='Input client ID')
args = parser.parse_args()

## create class Client

class Client:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    async def send_a_message(self, stub: dummy_pb2_grpc.MessagingStub, message: str, id: str) -> None:
        ## create a message object
        msg = dummy_pb2.TextMessage
        msg.sender_id = id
        msg.message = message

        print('message created ')
        _ = stub.send(msg)
        print('message sent')

    async def receive_messages(self, stud: dummy_pb2_grpc.MessagingStub, name: str, id: str) -> None:
        ## create a member call
        member = dummy_pb2.Member()
        member.name = name
        member.id = id
        messages = stud.receive(member)
        async for m in messages:
           print(f"Message received from {m.sender_id}: {m.message}")


