import krpc
from pprint import pprint
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from math import log10

def symlog(n):
    # if n < 0: return -log10(-n)
    # else: return log10(n+1)
    return n/5000000

conn = krpc.connect(name='kpl')
ref = conn.space_center.bodies['Sun'].reference_frame

bodies = []
body_names = []
for k, b in conn.space_center.bodies.items():
    body = {
        'name': k,
        'satellites': [s.name for s in b.satellites],
        'mass': b.mass,
        'position': b.position(ref),
        'size': b.equatorial_radius,
        }
    if not b.orbit: body['radius'] = 0
    else: body['radius']  = b.orbit.radius
    bodies.append(body)
    body_names.append(k)
pprint(bodies)

vessels = []
n = 0
for i in conn.space_center.vessels:
    vessels.append({
        'name': str(n) + i.name,
        'orbiting': i.orbit.body.name,
        'radius': i.orbit.radius,
        'position': i.position(ref),
        'mass': i.mass
        })
    n += 1
# pprint(vessels)


elements = [{'data': {
                'id':i['name'],
                'label': i['name']},
            'position':{
                'x': symlog(i['position'][0]),
                'y': symlog(i['position'][1])
            },
            'style': {'size': str(int(i['size']/10000))}} for i in bodies]
pprint(elements)

for b in bodies:
    if len(b['satellites']) > 0:
        for s in b['satellites']:
            # optional add parents for each satellite
            # elements[body_names.index(s)]['data']['parent'] = b['name']
            # add edge from body to satellite
            elements.append({'data':{'source': b['name'], 'target': s}})
            print('making edge: ', b['name'], s)
pprint(elements)

layouts = ['preset', 'grid', 'random', 'circle', 'cose', 'concentric']


app = Dash()
style = [{'selector':'node','style':{'content': 'data(label)', 'color':'white'}}]
app.layout = html.Div(style={'width':'100%', 'height': '100%'}, children=[
    html.H1('kmap'),
    dcc.Dropdown(id='dropdown', options=[{'label':i, 'value': i} for i in layouts]),
    cyto.Cytoscape(
        id='cyto',
        layout={'name': 'cose', 'animate' : True},
        elements=elements,
        stylesheet=style,
    )
], )

@app.callback(Output('cyto', 'layout'), [Input('dropdown', 'value')])
def update_layout(v):
    return {'name': v, 'animate' : True}

if __name__ == '__main__':
    app.run_server(debug=True)
