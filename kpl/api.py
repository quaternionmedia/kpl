from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from kpl.responses import ORJSONResponse
from kpl.constants import flight_chars

import krpc

def getAll(obj):
    # return {attr: getattr(obj, attr) for attr in flight_chars}
    res = {}
    for attr in flight_chars:
        try:
            res[attr] = getattr(obj, attr)
        except Exception as e:
            print('error converting', attr, e)
    return res
conn = krpc.connect(
            name='kpl',
            address='127.0.0.1',
            rpc_port=50000, stream_port=50001)
print(conn.krpc.get_status().version)
vessel = conn.space_center.active_vessel

app = FastAPI()
app = FastAPI(default_response_class=ORJSONResponse)

@app.get('/stats')
def getFlighStats():
    return getAll(vessel.flight())
    


app.mount('/static', StaticFiles(directory='web/static', html=True), name='static')
app.mount('/', StaticFiles(directory='web/dist', html=True), name='dist')

