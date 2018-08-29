#!/usr/bin/python
# -*- coding: utf-8 -*-

# signalr_aio/transports/_transport.py
# Stanislav Lazarov

# -----------------------------------
# Internal Imports
from ._exceptions import ConnectionClosed
from ._parameters import WebSocketParameters
from ._queue_events import InvokeEvent, CloseEvent

# -----------------------------------
# External Imports
try:
    from ujson import dumps, loads
except ModuleNotFoundError:
    from json import dumps, loads
import websockets
import asyncio
import logging

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ModuleNotFoundError:
    pass

logger = logging.getLogger(__name__)


class Transport:
    def __init__(self, connection):
        self._connection = connection
        self._max_reconnects = connection.max_reconnects
        self._timeout = connection.timeout
        self._ws_params = None
        self._conn_handler = None
        self.ws_loop = None
        self.invoke_queue = None
        self.ws = None
        self._reconnects = 0
        self._set_loop_and_queue()

    # ===================================
    # Public Methods

    def start(self):
        self._ws_params = WebSocketParameters(self._connection)
        self._connect()
        if not self.ws_loop.is_running():
            self.ws_loop.run_forever()
            self.ws.close()
            logger.debug('Websocket: OFF; Event loop: OFF; Exiting...')

    def send(self, message):
        asyncio.Task(self.invoke_queue.put(InvokeEvent(message)), loop=self.ws_loop)

    def close(self):
        asyncio.Task(self.invoke_queue.put(CloseEvent()), loop=self.ws_loop)

    # ===================================
    # Private Methods

    def _set_loop_and_queue(self):
        try:
            self.ws_loop = asyncio.get_event_loop()
        except RuntimeError:
            self.ws_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ws_loop)
        self.invoke_queue = asyncio.Queue(loop=self.ws_loop)

    def _connect(self):
        self._conn_handler = asyncio.ensure_future(self._socket(self.ws_loop), loop=self.ws_loop)

    async def _socket(self, loop):
        try:
            async with websockets.connect(self._ws_params.socket_url, extra_headers=self._ws_params.headers,
                                          loop=loop) as self.ws:
                self._connection.started = True
                await self._master_handler(self.ws)
        except asyncio.CancelledError:
            self._reconnects += 1
            if self._reconnects <= self._max_reconnects:
                self._connect()
            else:
                # Stop the loop if the user is not using it for something else.
                if len(asyncio.all_tasks()) and asyncio.current_task() == list(asyncio.all_tasks())[0]:
                    self.ws_loop.stop()

    async def _master_handler(self, ws):
        tasks = [asyncio.ensure_future(self._consumer_handler(ws), loop=self.ws_loop),
                 asyncio.ensure_future(self._producer_handler(ws), loop=self.ws_loop)]
        done, pending = await asyncio.wait(tasks, loop=self.ws_loop, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        await self.ws.close()
        self._conn_handler.cancel()

    async def _consumer_handler(self, ws):
        try:
            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=self._timeout)
                    if len(message) > 0:
                        data = loads(message)
                        await self._connection.received.fire(**data)
                except asyncio.TimeoutError:
                    logger.debug('No data in {} seconds, pinging the server.'.format(self._timeout))
                    try:
                        pong_waiter = await ws.ping()
                        await asyncio.wait_for(pong_waiter, timeout=5)
                        logger.debug('Ping OK, connection is alive. Attempting to retrieve next message.')
                    except asyncio.TimeoutError:
                        logger.debug('Ping timeout, reconnecting.')
                        asyncio.current_task().cancel()
        except asyncio.CancelledError:
            logger.debug('Canceling {}.'.format(self._consumer_handler.__name__))

    async def _producer_handler(self, ws):
        try:
            while True:
                event = await self.invoke_queue.get()
                if event is not None:
                    if event.type == 'INVOKE':
                        await ws.send(dumps(event.message))
                    elif event.type == 'CLOSE':
                        await ws.close()
                        while ws.open is True:
                            await asyncio.sleep(0.1)
                        else:
                            self._connection.started = False
                            break
                else:
                    break
                self.invoke_queue.task_done()
        except asyncio.CancelledError:
            logger.debug('Canceling {}.'.format(self._producer_handler.__name__))
