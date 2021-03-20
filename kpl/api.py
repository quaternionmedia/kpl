import krpc
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from kpl.responses import ORJSONResponse
from kpl.constants import flight_chars
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from json import dumps
from config import KRPC_ADDRESS, KRPC_PORT, KRPC_STREAM_PORT

app = FastAPI()

app.mount('/static', StaticFiles(directory='/app/static', html=True), name='static')
app.mount('/', StaticFiles(directory='/app/dist', html=True), name='dist')

