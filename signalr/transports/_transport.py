#!/usr/bin/python
# -*- coding: utf-8 -*-

# signalr/transports/_transport.py
# Stanislav Lazarov


from ._parameters import WebSocketParameters
from ._queue_events import InvokeEvent, CloseEvent
from ujson import dumps, loads
import asyncio
import uvloop
import websockets

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Transport:
    def __init__(self, connection):
        self._connection = connection
        self._ws_params = None
        self.ws_loop = None
        self.invoke_queue = None

        self._set_loop()

    def _set_loop(self):
        self.ws_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ws_loop)
        self.invoke_queue = asyncio.Queue(loop=self.ws_loop)

    def start(self):
        self._ws_params = WebSocketParameters(self._connection)
        self.ws_loop.run_until_complete(self.socket(self.ws_loop))

    def send(self, message):
        asyncio.Task(self.invoke_queue.put(InvokeEvent(message)), loop=self.ws_loop)

    def close(self):
        asyncio.Task(self.invoke_queue.put(CloseEvent()), loop=self.ws_loop)

    async def socket(self, loop):
        async with websockets.connect(self._ws_params.socket_url, extra_headers=self._ws_params.headers,
                                      loop=loop) as ws:
            self._connection.started = True
            await self.handler(ws)

    async def handler(self, ws):
        consumer_task = asyncio.ensure_future(self.consumer_handler(ws))
        producer_task = asyncio.ensure_future(self.producer_handler(ws))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    async def consumer_handler(self, ws):
        try:
            async for message in ws:
                if len(message) > 0:
                    data = loads(message)
                    await self._connection.received.fire(**data)
        except Exception as e:
            raise e

    async def producer_handler(self, ws):
        while True:
            try:
                event = await self.invoke_queue.get()
                if event is not None:
                    if event.type == 'INVOKE':
                        await ws.send(dumps(event.message))
                    elif event.type == 'CLOSE':
                        await ws.close(code=1000, reason='lol')
                else:
                    break
            except Exception as e:
                print(e)
