# python-signalr-client
**Python** signalR client using asyncio.
It's mainly based on [TargetProcess signalR client](https://github.com/TargetProcess/signalr-client-py) which uses gevent.

I am mainly developing the client for my **[Python Bittrex Websocket](https://github.com/slazarov/python-bittrex-websocket)** project, however I would make it as universal as possible.

# Road map
- Error handling

# Notices
None right now.


# Compatibility
Asyncio requires Python 3.4+.

For Python2.X compatibility try [TargetProcess' gevent based SignalR client](https://github.com/TargetProcess/signalr-client-py).


# Installation
#### Pypi (most stable)
```python
pip install xxx
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

# Change log

0.0.1.0 - Initial release.

# Other libraries
**[Python Bittrex Websocket](https://github.com/slazarov/python-bittrex-websocket)**

Python websocket client for getting live streaming data from [Bittrex Exchange](http://bittrex.com).


**[Python Bittrex Autosell](https://github.com/slazarov/python-bittrex-autosell)**

Python CLI tool to auto sell coins on Bittrex.

It is used in the cases when you want to auto sell a specific coin for another, but there is no direct market, so you have to use an intermediate market.