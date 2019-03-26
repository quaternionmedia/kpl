import krpc
from pprint import pprint
conn = krpc.connect(name='kpl')
vessels = []
for i in conn.space_center.vessels:
    vessels.append({
        'name': i.name,
        'orbiting': i.orbit.body.name,
        'radius': i.orbit.radius,
        'mass': i.mass
        })
pprint(vessels)

bodies = []
for k, b in conn.space_center.bodies.items():
    body = {
        'name': k,
        'satellites': [s.name for s in b.satellites],
        'mass': b.mass
        }
    if not b.orbit: body['radius'] = 0
    else: body['radius']  = b.orbit.radius
    bodies.append(body)
pprint(bodies)

# if __name__ == '__main__':
    # app.run('0.0.0.0', '8888')
