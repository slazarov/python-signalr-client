#!/usr/bin/python
# -*- coding: utf-8 -*-

# Stanislav Lazarov

# A practical example showing how to connect to Bittrex
from signalr import Connection


# Create debug message handler.
async def on_debug(**msg):
    print(msg)


# Create error handler
async def on_error(msg):
    print(msg)


# Create hub message handler
async def on_message(msg):
    print(msg)


if __name__ == "__main__":
    # Create connection
    connection = Connection('https://socket-stage.bittrex.com/signalr/')

    # Register hub
    hub = connection.register_hub('coreHub')

    # Assign debug message handler. It streams unfiltered data, uncomment it to test.
    # connection.received += on_debug

    # Assign error handler
    connection.error += on_error

    # Assign hub message handler
    hub.client.on('updateExchangeState', on_message)

    # Send a message
    hub.server.invoke('SubscribeToExchangeDeltas', 'BTC-ETH')

    # Start the client
    connection.start()