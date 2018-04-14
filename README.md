# python-signalr-client
**Python** signalR client using asyncio.
It's mainly based on [TargetProcess signalR client](https://github.com/TargetProcess/signalr-client-py) which uses gevent.

I am mainly developing the client for my **[Python Bittrex Websocket](https://github.com/slazarov/python-bittrex-websocket)** project, however I would make it as universal as possible.

# Road map
- Error handling

# Notices
None right now.

# Supplemental libraries
* For better performance users can install `ujson` which is automatically detected and overrides `json`.

* Users can pass a custom session to the client, i.e a [`cfscrape`](https://github.com/Anorov/cloudflare-scrape) session in order to bypass Cloudflare.




# Compatibility
Asyncio requires Python 3.5+.

For Python2.X compatibility try [TargetProcess' gevent based SignalR client](https://github.com/TargetProcess/signalr-client-py).


# Installation
#### Pypi (most stable)
```python
pip install signalr-client-aio
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
from signalr_aio import Connection
from base64 import b64decode
from zlib import decompress, MAX_WBITS
import json

def process_message(message):
    deflated_msg = decompress(b64decode(message), -MAX_WBITS)
    return json.loads(deflated_msg.decode())

# Create debug message handler.
async def on_debug(**msg):
    # In case of 'queryExchangeState'
    if 'R' in msg and type(msg['R']) is not bool:
        decoded_msg = process_message(msg['R'])
        print(decoded_msg)

# Create error handler
async def on_error(msg):
    print(msg)


# Create hub message handler
async def on_message(msg):
    decoded_msg = process_message(msg[0])
    print(decoded_msg)

if __name__ == "__main__":
    # Create connection
    # Users can optionally pass a session object to the client, e.g a cfscrape session to bypass cloudflare.
    connection = Connection('https://beta.bittrex.com/signalr', session=None)

    # Register hub
    hub = connection.register_hub('c2')

    # Assign debug message handler. It streams unfiltered data, uncomment it to test.
    connection.received += on_debug

    # Assign error handler
    connection.error += on_error

    # Assign hub message handler
    hub.client.on('uE', on_message)
    hub.client.on('uS', on_message)

    # Send a message
    hub.server.invoke('SubscribeToExchangeDeltas', 'BTC-ETH')
    hub.server.invoke('SubscribeToSummaryDeltas')
    hub.server.invoke('queryExchangeState', 'BTC-NEO')

    # Start the client
    connection.start()
```

# Change log
0.0.1.5 - 06/04/2018:
* Removed `cfscrape` from package. Users can optionally pass a `cfscrape` session to clients.
* Removed `ujson`. The package will automatically detect if the user chooses to use `ujson`.

0.0.1.0 - Initial release.

# Other libraries
**[Python Bittrex Websocket](https://github.com/slazarov/python-bittrex-websocket)**

Python websocket client for getting live streaming data from [Bittrex Exchange](http://bittrex.com).


**[Python Bittrex Autosell](https://github.com/slazarov/python-bittrex-autosell)**

Python CLI tool to auto sell coins on Bittrex.

It is used in the cases when you want to auto sell a specific coin for another, but there is no direct market, so you have to use an intermediate market.