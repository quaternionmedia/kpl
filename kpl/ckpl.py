import krpc
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from os import environ
import asyncio
from constants import flight_chars
from config import KRPC_ADDRESS, KRPC_PORT, KRPC_STREAM_PORT

class Ckpl(ApplicationSession):
    async def onJoin(self, details):
        print('kerbal session started!')
        self.conn = krpc.connect(name='ckpl',
            address=KRPC_ADDRESS,
            rpc_port=KRPC_PORT,
            stream_port=KRPC_STREAM_PORT,
        )
        print('connected!')
        self.vessel = self.conn.space_center.active_vessel
        self.refframe = self.vessel.orbit.body.reference_frame
        self.flight = self.vessel.flight()
        
        self.streams = []
        
        for char in flight_chars:
            stream = self.conn.add_stream(getattr, self.flight, char)
            stream.add_callback(self._publish(char))
            self.streams.append(stream)
        [stream.start() for stream in self.streams]
    def _publish(self, channel):
        print('setting up ', channel)
        def pub(value):
            # print('publishing', channel, value)
            self.publish('local.ksp.' + channel, value)
        return pub
    async def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    from config import CROSSBAR_ADDRESS, CROSSBAR_PORT
    runner = ApplicationRunner(environ.get('AUTOBAHN_DEMO_ROUTER', f'ws://{CROSSBAR_ADDRESS}:{CROSSBAR_PORT}/ws'), u'realm1',)
    runner.run(Ckpl)