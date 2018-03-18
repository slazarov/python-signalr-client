# python-signalr-client
**Python** signalR client using asyncio.
It's mainly based on [TargetProcess signalR client](https://github.com/TargetProcess/signalr-client-py) which uses gevent.

I am mainly developing the client for my **[Python Bittrex Websocket](https://github.com/slazarov/python-bittrex-websocket)** project, however I would make it as universal as possible.

# Road map
- Error handling

# Notices
None right now.


# Compatibility
Asyncio requires Python 3.5+.

For Python2.X compatibility try [TargetProcess' gevent based SignalR client](https://github.com/TargetProcess/signalr-client-py).


# Installation
#### Pypi (most stable)
```python
pip install signalr_client_aio
```
#### Github (master)
```python
pip install git+https://github.com/slazarov/python-signalr-client.git
```
#### Github (work in progress branch)
```python
pip install git+https://github.com/slazarov/python-signalr-client.git@next-version-number
```

# Sample usage
```python
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
```

# Change log

0.0.1.0 - Initial release.

# Other libraries
**[Python Bittrex Websocket](https://github.com/slazarov/python-bittrex-websocket)**

Python websocket client for getting live streaming data from [Bittrex Exchange](http://bittrex.com).


**[Python Bittrex Autosell](https://github.com/slazarov/python-bittrex-autosell)**

Python CLI tool to auto sell coins on Bittrex.

It is used in the cases when you want to auto sell a specific coin for another, but there is no direct market, so you have to use an intermediate market.