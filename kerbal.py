#!/usr/local/bin/python3

import krpc
import time
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.endpoints import WebSocketEndpoint



import uvicorn


conn = krpc.connect(name='george')
vessel = conn.space_center.active_vessel
refframe = vessel.orbit.body.reference_frame

fields = {
    'position': vessel.position,
    'orbit': vessel.orbit
}
print('connected to', vessel.name)

# pos = conn.add_stream(vessel.position, refframe)
# orbit = conn.add_stream(getattr, vessel.orbit, 'apoapsis')





#input()
app = FastAPI()

app.mount('/deps', StaticFiles(directory='deps'), name='deps')
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def home():
    return HTMLResponse(render_template('kerbal.html'))

@app.websocket_route('/krpc')
class Krpcws(WebSocketEndpoint):
    encoding = 'json'
    async def on_connect(self, websocket):#, data):
        self.websocket = websocket
    with conn.stream(vessel.position, refframe) as p:
        with p.condition:
            websocket.send_json({'pos': p()})

def render_template(path, **kwargs):
    return templates.get_template(path).render(**kwargs)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
