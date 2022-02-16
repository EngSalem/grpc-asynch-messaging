import asyncio
import logging
import random
from typing import Iterable, List

import grpc
import dummy_pb2
import dummy_pb2_grpc

from async_client import Client
import time


async def main() -> None:
     alice = Client(id='1', name='alice');
     bob = Client(id='2', name='bob')
     chad = Client(id='3', name='Chad')
     async with grpc.aio.insecure_channel('localhost:50051') as channel:
         stub = dummy_pb2_grpc.MessagingStub(channel)
         print('------- Alice sending message ------')
         await alice.send_a_message(stub, 'Hello my name is Alice', alice.id)
         time.sleep(3)
         await chad.send_a_message(stub, 'My name is Chad', chad.id)
         time.sleep(5)
         print('------- Bob receiving message -------')
         await bob.receive_messages(stub, bob.name, bob.id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())




