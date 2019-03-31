import krpc
from pprint import pprint
from kpl import kpl
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_cytoscape as cyto
from math import sqrt
from dash_smoothie import Smoothie
import kerbal

layouts = ['preset', 'grid', 'random', 'circle', 'cose', 'concentric', 'breadthfirst']

body_names = kerbal.getBodyNames()
print('body_names', body_names)

graphs = []
for i in kerbal.vectors:
    graphs.append(html.H2(i))
    graphs.append(Smoothie(id=i, label=i, millisPerPixel=30,  axisProps=[
        {'name': 'x', 'r': 255},
        {'name': 'y', 'g': 255},
        {'name': 'z', 'b': 255}]))

#app = Dash()
style = [{'selector':'node','style':{'content': 'data(label)', 'color':'white'}}] #+ [{'selector': i, 'style': {'height': int(i['size']/100), 'width': int(i['size']/100)}} for i in body_names]
layout = html.Div(style={'width':'100%', 'height': '100%'}, children=[
    html.H1('kmap'),
    dcc.Dropdown(id='dropdown',
                value='preset',
                clearable=False,
                options=[{'label':i, 'value': i} for i in layouts]),
    dcc.Dropdown(id='refframe',
                value='Kerbin',
                clearable=False,
                options=[{'label':i, 'value': i} for i in body_names]),
    cyto.Cytoscape(
        id='cyto',
        layout={'name': 'preset', 'animate' : True, 'animationDuration':1000},
        elements=kerbal.getPositions(0, 'Sun'),
        stylesheet=style,
    ),
    *graphs,
    dcc.Interval(id='kmap-interval', interval = 3000, n_intervals=0),
    dcc.Interval(id='kmap-interval2', interval = 300, n_intervals=0),

    dcc.Store(id='kmap-storage', storage_type='session', data='Kerbin'),
], )

def update_smoothie(n, id):
    results = kerbal.getStats()[id]
    print(id, results)
    return [*results]

for v in kerbal.vectors:
    kpl.callback(Output(v, 'extendData'), [Input('kmap-interval2', 'n_intervals')], [State(v, 'id')])(update_smoothie)


@kpl.callback(Output('cyto', 'layout'), [Input('dropdown', 'value')])
def update_layout(v):
    return {'name': v, 'animate' : True, 'animationDuration':1000}

kpl.callback(Output('cyto', 'elements'),
            [Input('kmap-interval', 'n_intervals')],
            [State('kmap-storage', 'data')])(kerbal.getPositions)

def update_ref(selectedNodes, referenceFrame):
    # print('storing ', sel)
    if not selectedNodes and not referenceFrame: raise PreventUpdate
    if selectedNodes: return selectedNodes[0]['id']
    else: return referenceFrame

kpl.callback(Output('kmap-storage', 'data'),
            [Input('cyto', 'selectedNodeData'), Input('refframe', 'value')])(update_ref)

if __name__ == '__main__':
    kpl.layout = layout
    kpl.run_server(host='0.0.0.0', port=8888, debug=True)
