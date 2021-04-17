from os import environ

STATIC_FILES = environ.get('STATIC_FILES', 'web/static')
DIST_DIR = environ.get('DIST_DIR', 'web/dist')

KRPC_ADDRESS = environ.get('KRPC_ADDRESS', '127.0.0.1')

KRPC_PORT = 50000
KRPC_STREAM_PORT = 50001

CROSSBAR_ADDRESS = environ.get('CROSSBAR_ADDRESS', '127.0.0.1')
CROSSBAR_PORT = environ.get('CROSSBAR_PORT', 8080)
