import krpc
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from os import environ
import asyncio
from time import time

class Ckerbal(ApplicationSession):
    async def onJoin(self, details):
        print('Ckerbal session started!')
        self.conn = krpc.connect(name='george')
        self.vessel = self.conn.space_center.active_vessel
        self.refframe = self.vessel.orbit.body.reference_frame
        self.lpos = time()
        def getPos():
            with self.conn.stream(self.vessel.position, self.refframe) as p:
                with p.condition:
                    if time() - self.lpos > .1:
                        self.lpos = time();
                        pos = p()
                        # print('new position', pos, time())
                        self.publish(u'local.krpc.position', pos)

        while True:
            getPos()



    async def onDisconnect(self):
        asyncio.get_event_loop().stop()

if __name__ == '__main__':
    runner = ApplicationRunner(environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://localhost:7777/ws"), u"realm1",)
    runner.run(Ckerbal)
