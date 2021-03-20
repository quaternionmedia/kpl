from os import environ

KRPC_ADDRESS = environ.get('KRPC_ADDRESS', '127.0.0.1')
KRPC_PORT = 50000
KRPC_STREAM_PORT = 50001