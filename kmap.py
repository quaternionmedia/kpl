import krpc
from pprint import pprint
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto

conn = krpc.connect(name='kpl')
vessels = []
n = 0
for i in conn.space_center.vessels:
    vessels.append({
        'name': str(n) + i.name,
        'orbiting': i.orbit.body.name,
        'radius': i.orbit.radius,
        'mass': i.mass
        })
    n += 1
# pprint(vessels)

bodies = []
body_names = []
for k, b in conn.space_center.bodies.items():
    body = {
        'name': k,
        'satellites': [s.name for s in b.satellites],
        'mass': b.mass
        }
    if not b.orbit: body['radius'] = 0
    else: body['radius']  = b.orbit.radius
    bodies.append(body)
    body_names.append(k)
# pprint(bodies)
elements = [{'data': { 'id':i['name'], 'label': i['name'] }} for i in bodies]

for n, b in enumerate(bodies):
    if len(b['satellites']) > 0:
        for s in b['satellites']:
            elements[body_names.index(s)]['data']['parent'] = b['name']
pprint(elements)

app = Dash()
style = [{'selector':'node','style':{'content': 'data(label)', 'color':'white'}}]
app.layout = html.Div([
    html.H1('kmap'),
    cyto.Cytoscape(
        id='cyto',
        layout={'name': 'circle'},
        elements=elements,
        stylesheet=style,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
