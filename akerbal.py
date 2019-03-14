#!/usr/bin/python3
import asyncio
import krpc

class KspSession(object):
    def __init__ (self):
        self.conn = krpc.connect(name="stream_test")
        self.msg("KRPC client Connected!")

        # Set up a queue for tasks to communicate
        self.event_queue = asyncio.Queue()
        self.vessel = self.conn.space_center.active_vessel

        # Get the event loop and add some tasks
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(
            self.listen_other(self.vessel.position,
            self.vessel.orbit.body.reference_frame))
        # self.loop.create_task(
            # self.listen_flight_attr(self.vessel.orbit.body.reference_frame,
                                    # "speed"))

        # Finally add a task to handle all the flight events
        self.loop.create_task(self.handle_flight_events())

    def msg(self, s, duration=5.0):
        print('new message:', s)
        self.conn.ui.message(s, duration=duration)

    @asyncio.coroutine
    async def handle_flight_events (self):
        while True:
            # Wait until an item is put on the queue before dequeuing
            data = await self.event_queue.get()
            self.msg('Flight event: {} at {}'.format(data[0], data[1]))
            # Process event here..
            # Test part, adjust course, deploy chutes, suicide burn etc..

    @asyncio.coroutine
    async def listen_flight_attr(self, ref, attr):
        self.msg(f"Listening for {attr} events")
        with self.conn.stream(self.vessel.flight, ref) as flight:
            while True:
                # yield # Let the CPU do other work
                val = getattr(flight(), attr)
                # if val > minimum and val < maximum:
                    # Put the flight data on the queue
                data = ( attr, val )
                await self.event_queue.put(data)
                return
    @asyncio.coroutine
    async def listen_other(self, attr, ref=None):
        self.msg(f"Listening for {attr} events")
        with self.conn.stream(attr, ref) as d:
                # yield # Let the CPU do other work
            with d.condition:
                # while True:
                    val = d()
                    # if val > minimum and val < maximum:
                        # Put the flight data on the queue
                    data = ( attr, val )
                    await self.event_queue.put(data)
                    return


    def run(self):
        # Run all tasks in an event loop, and don't stop
        self.loop.run_forever()

sess = KspSession()
sess.run()
