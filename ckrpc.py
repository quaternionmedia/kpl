import krpc
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from os import environ
import asyncio
from time import time
from json import dumps
flight_chars = ['aerodynamic_force', 'angle_of_attack',  'atmosphere_density', 'bedrock_altitude', 'center_of_mass', 'direction', 'drag', 'dynamic_pressure', 'elevation', 'equivalent_air_speed', 'g_force', 'heading', 'horizontal_speed', 'latitude', 'lift', 'longitude', 'mach', 'mean_altitude', 'pitch', 'roll', 'rotation', 'sideslip_angle', 'speed', 'speed_of_sound',  'static_air_temperature', 'static_pressure', 'static_pressure_at_msl', 'surface_altitude', 'terminal_velocity',  'total_air_temperature', 'true_air_speed', 'velocity', 'vertical_speed']
# broken = ['ballistic_coefficient', 'drag_coefficient', 'lift_coefficient',  'reynolds_number','stall_fraction', 'thrust_specific_fuel_consumption','simulate_aerodynamic_force_at',]
# redundant = ['normal', 'anti_normal', 'prograde', 'radial', 'retrograde', 'anti_radial']

class Ckerbal(ApplicationSession):
    async def onJoin(self, details):
        print('kerbal session started!')
        self.conn = krpc.connect(name='george')
        print('connected!')
        self.vessel = self.conn.space_center.active_vessel
        self.refframe = self.vessel.orbit.body.reference_frame
        self.last_update = time()
        def getFlightChars(x):
            j = {}
            for i in flight_chars:
                j[i] = getattr(x, i)
            # print('new attrs', j )
            return j
            # publish(u'local.krpc.position', j)
        self.flightStats = self.conn.add_stream(self.vessel.flight, self.refframe)
        self.flightStats.add_callback(getFlightChars)
        self.flightStats.start()
        while True:
            with self.flightStats.condition:
                if time() - self.last_update > 1:
                    stats = getFlightChars(self.flightStats())
                    print(stats)
                    self.publish('local.krpc.flightStats',
                                    dumps(stats))
                    self.last_update = time()

    async def onDisconnect(self):
        asyncio.get_event_loop().stop()

if __name__ == '__main__':
    runner = ApplicationRunner(environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://localhost:7777/ws"), u"realm1",)
    runner.run(Ckerbal)
