from kpl import kpl
from math import sqrt
from time import time

floats = [ 'angle_of_attack',  'atmosphere_density', 'bedrock_altitude', 'dynamic_pressure', 'elevation', 'equivalent_air_speed', 'g_force', 'heading', 'horizontal_speed', 'latitude', 'longitude', 'mach', 'mean_altitude', 'pitch', 'roll',  'sideslip_angle', 'speed', 'speed_of_sound',  'static_air_temperature', 'static_pressure', 'static_pressure_at_msl', 'surface_altitude', 'terminal_velocity',  'total_air_temperature', 'true_air_speed', 'vertical_speed']

vectors = ['aerodynamic_force', 'center_of_mass', 'direction', 'drag', 'lift', 'velocity']
quaternions = ['rotation']
vessel = kpl.conn.space_center.active_vessel
refframe = vessel.orbit.body.reference_frame
ranges = []

def symlog(n):
    if n < 0: return -sqrt(sqrt(-n))
    else: return sqrt(sqrt(n))
    # return n/1000000000

def getStats():
    s = flightStats()
    j = {i: round(getattr(s, i), 2) for i in floats}

    v = {i: getattr(s, i) for i in vectors}
    w = {i: (round(v[i][0], 2), round(v[i][1], 2), round(v[i][2], 2)) for i in vectors}
    j['time'] = round(time(), 2)
    return {**j, **w}

flightStats = kpl.conn.add_stream(vessel.flight, refframe)
# print('init stats with:', stats[-1])

def getBodyNames():
    return list(kpl.conn.space_center.bodies.keys())

def getPositions(n, refName):
    print('getting positions from', refName)
    refframe = kpl.conn.space_center.bodies[refName].reference_frame
    bodies = []
    for k, b in kpl.conn.space_center.bodies.items():
        body = {
            'name': k,
            'satellites': [s.name for s in b.satellites],
            'mass': b.mass,
            'position': b.position(refframe),
            'size': b.equatorial_radius,
            }
        if not b.orbit: body['radius'] = 0
        else: body['radius']  = b.orbit.radius
        bodies.append(body)
        # body_names.append(k)
    # pprint(bodies)

    vessels = []
    n = 0
    for i in kpl.conn.space_center.vessels:
        vessels.append({
            'name': str(n) + i.name,
            'orbiting': i.orbit.body.name,
            'radius': i.orbit.radius,
            'position': i.position(refframe),
            'mass': i.mass,
            'satellites': '',
            })
        n += 1
    # pprint(vessels)


    elements = [ { 'data': {
                    'id':i['name'],
                    'label': i['name']},
                'position':{
                    'x': int(2*symlog(i['position'][0])),
                    'y': int(2*symlog(i['position'][2]))
                },} for i in bodies+vessels]
    # pprint(elements)

    for b in bodies:
        if len(b['satellites']) > 0:
            for s in b['satellites']:
                # optional add parents for each satellite
                # elements[body_names.index(s)]['data']['parent'] = b['name']
                # add edge from body to satellite
                elements.append({'data':{'source': b['name'], 'target': s}})
                # print('making edge: ', b['name'], s)
    for v in vessels:
        elements.append({'data':{'source': v['name'], 'target': v['orbiting']}})
    # pprint(elements)
    return elements
