#!/usr/bin/python

from setuptools import setup, find_packages

install_requires = \
    [
        'aiocfscrape>=0.0.4',
        'aiohttp>=3.0.9',
        'Js2Py>=0.59',
        'ujson>=1.35',
        'uvloop>=0.9.1',
        'websockets>=4.0.1'
    ]

setup(
    name='signalr-client-aio',
    version='0.0.1.3',
    author='Stanislav Lazarov',
    author_email='s.a.lazarov@gmail.com',
    license='MIT',
    url='https://github.com/slazarov/python-signalr-client',
    packages=find_packages(exclude=['tests*']),
    install_requires=install_requires,
    description='Simple python SignalR client using asyncio.',
    download_url='https://github.com/slazarov/python-signalr-client.git',
    keywords=['signalr', 'sginalr-weboscket', 'signalr-client', 'signalr-asyncio', 'signalr-aio'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
