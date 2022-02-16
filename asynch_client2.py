import asyncio
import logging
import random
from typing import Iterable, List

import grpc
import dummy_pb2
import dummy_pb2_grpc

## send a message

async def send_a_message(stud: dummy_pb2_grpc.MessagingStub, message: str, id: str) -> None:
    ## create a message object
    msg = dummy_pb2.TextMessage
    msg.sender_id = id
    msg.message = message

    print('message created ')
    _ = stud.send(msg)

async def receive_messages(stud: dummy_pb2_grpc.MessagingStub, name: str, id: str) -> None:
    ## create a member call
    member = dummy_pb2.Member
    member.name = name
    member.id = id
    messages = stud.receive(member)
    print('type is', messages)
    async for msg in messages:
        print(msg)
        print(f"Message received from {msg.sender_id}: {msg.message}")

async def main() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = dummy_pb2_grpc.MessagingStub(channel)
        print('-------- receiving message ----------')
        await receive_messages(stub, 'ahmed', '2')
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
