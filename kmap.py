import krpc
from pprint import pprint
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_cytoscape as cyto
from math import sqrt

def symlog(n):
    if n < 0: return -sqrt(sqrt(-n))
    else: return sqrt(sqrt(n))
    # return n/1000000000

conn = krpc.connect(name='kpl')
body_names = []

def getPositions(n, refName):
    print('getting positions from', refName)
    refframe = conn.space_center.bodies[refName].reference_frame
    bodies = []
    for k, b in conn.space_center.bodies.items():
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
        body_names.append(k)
    # pprint(bodies)

    vessels = []
    n = 0
    for i in conn.space_center.vessels:
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
    pprint(elements)
    return elements

layouts = ['preset', 'grid', 'random', 'circle', 'cose', 'concentric', 'breadthfirst']


app = Dash()
style = [{'selector':'node','style':{'content': 'data(label)', 'color':'white'}}] + [{'selector': i, 'style': {'size': int(i['size']/10)}} for i in body_names]
app.layout = html.Div(style={'width':'100%', 'height': '100%'}, children=[
    html.H1('kmap'),
    dcc.Dropdown(id='dropdown',
                value='preset',
                clearable=False,
                options=[{'label':i, 'value': i} for i in layouts]),
    cyto.Cytoscape(
        id='cyto',
        layout={'name': 'preset', 'animate' : True, 'animationDuration':1000},
        elements=getPositions(0, 'Sun'),
        stylesheet=style,
    ),
    dcc.Interval(id='interval-component', interval = 3000, n_intervals=0),
    dcc.Store(id='storage', storage_type='session', data='Kerbin'),
], )

@app.callback(Output('cyto', 'layout'), [Input('dropdown', 'value')])
def update_layout(v):
    return {'name': v, 'animate' : True, 'animationDuration':1000}

app.callback(Output('cyto', 'elements'),
            [Input('interval-component', 'n_intervals')],
            [State('storage', 'data')])(getPositions)

@app.callback(Output('storage', 'data'), [Input('cyto', 'selectedNodeData')])
def update_ref(sel):
    # print('storing ', sel)
    if not sel: raise PreventUpdate
    else:
        return sel[0]['id']


if __name__ == '__main__':
    app.run_server(debug=True)
