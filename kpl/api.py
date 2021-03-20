import krpc
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from kpl.responses import ORJSONResponse
from kpl.constants import flight_chars
from pika import BlockingConnection, ConnectionParameters
from json import dumps
from config import KRPC_ADDRESS, KRPC_PORT, KRPC_STREAM_PORT

def getAll(obj):
    # return {attr: getattr(obj, attr) for attr in flight_chars}
    res = {}
    for attr in flight_chars:
        try:
            res[attr] = getattr(obj, attr)
        except Exception as e:
            print('error converting', attr, e)
    return res

class Ksp:
    def __init__(self, name='kpl',
                address=KRPC_ADDRESS, 
                rpc_port=KRPC_PORT, 
                stream_port=KRPC_STREAM_PORT):
        try:
            self.connection = BlockingConnection(ConnectionParameters('rabbit'))
            self.channel = self.connection.channel()
            
            self.conn = krpc.connect(
                name=name,
                # address='192.168.1901.130',
                address=address,
                rpc_port=rpc_port, stream_port=stream_port)
            print(self.conn.krpc.get_status().version)
            self.vessel = self.conn.space_center.active_vessel
            self.flight = self.vessel.flight()
                
            self.streams = []
            
            for char in flight_chars:
                self.channel.queue_declare(queue=char)
                stream = self.conn.add_stream(getattr, self.flight, char)
                stream.add_callback(self.publish(char))
                self.streams.append(stream)
            [stream.start() for stream in self.streams]
        except Exception as e:
            print('error initializing Ksp object', e)
    def publish(self, channel):
        print('setting up ', channel)
        def pub(value):
            # print('publishing', channel, value)
            self.channel.basic_publish(exchange='', routing_key=channel, body=dumps(value))
        return pub
        
k = Ksp()        

app = FastAPI(default_response_class=ORJSONResponse)

@app.get('/stats')
def getFlighStats():
    if k.conn.krpc.current_game_scene.name == 'flight':
        vessel = k.conn.space_center.active_vessel
        return getAll(vessel.flight())

app.mount('/static', StaticFiles(directory='/app/static', html=True), name='static')
app.mount('/', StaticFiles(directory='/app/dist', html=True), name='dist')

