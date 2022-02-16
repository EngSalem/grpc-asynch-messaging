import asyncio
import logging
import time
from typing import AsyncIterable, Iterable

import grpc
import dummy_pb2
import dummy_pb2_grpc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ids', action='store', dest='member_ids',
                    help='Input client ID')
args = parser.parse_args()



class ChatServicer(dummy_pb2_grpc.MessagingServicer):

    def __init__(self, member_list):
        ## defining chat members where they are initialized by a string comma separated
        self.members = member_list.split(',')
        ## initialize chat history for each member with empty buffer
        ## we use multiple buffers each identified by a member id
        self.chat_history = {_id: [] for _id in self.members}
        print('created server instance for members: '+ ' '.join(self.members))

    async def send(self, request: dummy_pb2.TextMessage, context) -> dummy_pb2.Empty:
        ## this function takes the message and add it to chat history
        ## check who sent the message
        current_sender = request.sender_id
        for _id in self.members:
            ## add message to all particpants buffers except to sender
            if _id != current_sender:
               self.chat_history[_id].append(request)

        ## returns empty as previously defined in proto
        return dummy_pb2.Empty()

    async def receive(self, request: dummy_pb2.Member, context) -> AsyncIterable[dummy_pb2.TextMessage]:
        ## this method takes the chat member info and return its messages
        ## first retrieve the buffer for the signed in client

        while len(self.chat_history[request.id]) > 0:
            ## get message from buffer and delete it
            msg = self.chat_history[request.id].pop()
            yield msg


async def serve() -> None:
    server = grpc.aio.server()
    dummy_pb2_grpc.add_MessagingServicer_to_server(ChatServicer(args.member_ids), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
