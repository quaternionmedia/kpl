from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State#, Event
import dash_extendable_graph as ex
import dash_daq as daq
from time import time
from collections import deque
from kpl import kpl
from pprint import pprint
from math import floor
stats = deque([], maxlen=10)

floats = [ 'angle_of_attack',  'atmosphere_density', 'bedrock_altitude', 'dynamic_pressure', 'elevation', 'equivalent_air_speed', 'g_force', 'heading', 'horizontal_speed', 'latitude', 'longitude', 'mach', 'mean_altitude', 'pitch', 'roll',  'sideslip_angle', 'speed', 'speed_of_sound',  'static_air_temperature', 'static_pressure', 'static_pressure_at_msl', 'surface_altitude', 'terminal_velocity',  'total_air_temperature', 'true_air_speed', 'vertical_speed']

vectors = ['aerodynamic_force', 'center_of_mass', 'direction', 'drag', 'lift', 'velocity']
quaternions = ['rotation']


# def Add_Dash(server):
    # dash_app = Dash(server=server, url_base_pathname='/kdash/')

# conn = krpc.connect(name='kdash')
vessel = kpl.conn.space_center.active_vessel
refframe = vessel.orbit.body.reference_frame
ranges = []
def getFlightChars(x):
    j = {i: round(getattr(x, i), 2) for i in floats}
    j['time'] = round(time(), 2)
    return j
flightStats = kpl.conn.add_stream(vessel.flight, refframe)
stats.append(getFlightChars(flightStats()))
print('init stats with:', stats[-1])

layout = html.Div(id='flex-container', className='flex-container', children=[
        html.Div(id='header', className='twelve columns', style= {'align': 'center', 'background-color': '#222'}, children=[
            html.H1(className='two columns', children='KPL!'),
            html.H2(className='eight columns', children='Kerbal Propulsion Laborotory'),
            html.H3(className='two columns', children='Dashboard')
            ]),
        html.Div(id='speeds', className='twelve columns', children=[
            # daq.Gauge(id='therm', label='speed', min=0, max=200, value=0, className='three columns', labelPosition='bottom', showCurrentValue=True, style={'padding-left': '10%'}),
            # dcc.Graph(id='thermGraph'),
            ex.ExtendableGraph(id='exGraph', className='twelve columns', figure={'data': [{'x':[], 'y':[]}]}, )
            ]),
        html.Div(id='gauges', className='twelve columns', children=[
            # get_datasets()
            *[ daq.Gauge(id=i, label=i, min=0, max=1, value=0, size=110, labelPosition='bottom', showCurrentValue=True, className='one column', style={'padding-left': '5%'}, ) for i in floats]
            ]),
        dcc.Interval(id='kdash-interval', interval = 1000, n_intervals=0),
        dcc.Store(id='kdash-storage', storage_type='session', data=stats[-1]),
            ]
        )

@kpl.callback(Output('kdash-storage', 'data'),
                    [Input('kdash-interval', 'n_intervals')],
                    )
def store_data(n):
    if not n: raise PreventUpdate
    stats.append(getFlightChars(flightStats()))
    # print('updated storage', stats[-1])
    return stats[-1]

def update_gauge(n, d, prop):
    return d[prop] or 0

def update_gauge_range_min(n, d, prop, minimum):
    print('gauge min', n, prop, minimum, min(d[prop] or 0, minimum), type(min(d[prop] or 0, minimum)))
    return int(floor(min(d[prop] or 0, minimum)))

def update_gauge_range_max(n, d, prop, maximum):
    return max(d[prop] or 0, maximum)


for i in floats:
    kpl.callback(Output(i, 'value'),
                        [Input('kdash-interval', 'n_intervals')],
                        [State('kdash-storage', 'data'),
                        State(i, 'id')])(update_gauge)

# kpl.callback(Output('roll', 'min'), [Input('kdash-interval', 'n_intervals')],[State('kdash-storage', 'data'), State('roll', 'id'), State('roll', 'min')])(update_gauge_range_min)

# for i in floats:
#     kpl.callback(Output(i, 'min'),
#                     [Input('kdash-interval', 'n_intervals')],
#                     [State('kdash-storage', 'data'),
#                     State(i, 'id'),
#                     State(i, 'min')])(update_gauge_range_min)
for i in floats:
    kpl.callback(Output(i, 'max'),
                        [Input('kdash-interval', 'n_intervals')],
                        [State('kdash-storage', 'data'),
                        State(i, 'id'),
                        State(i, 'max')])(update_gauge_range_max)

@kpl.callback(Output('exGraph', 'extendData'),
                    [Input('kdash-storage', 'data')])
                    # [State('exGraph', 'figure')])
def update_therm_graph(d):
    return [ dict(x=[d['time']], y=[d['speed']]) ]


    # return kpl.server
if __name__ == '__main__':
    kpl.layout = layout
    kpl.run_server(host='0.0.0.0', port=8888, debug=True)
