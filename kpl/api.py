import krpc
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from kpl.responses import ORJSONResponse
from kpl.constants import flight_chars
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from json import dumps
from .config import KRPC_ADDRESS, KRPC_PORT, KRPC_STREAM_PORT, STATIC_FILES, DIST_DIR

app = FastAPI()

app.mount('/static', StaticFiles(directory=STATIC_FILES, html=True), name='static')
app.mount('/', StaticFiles(directory=DIST_DIR, html=True), name='dist')

