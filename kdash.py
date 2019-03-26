import glob
from pathlib import Path, PurePath
from dash import Dash, callback_context
from dash.exceptions import PreventUpdate
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State#, Event
import plotly.graph_objs as go
import dash_extendable_graph as ex
import dash_daq as daq
import pandas as pd
from random import random
from time import time
from collections import deque
import krpc
from pprint import pprint
temps = deque([], maxlen=10)

floats = [ 'angle_of_attack',  'atmosphere_density', 'bedrock_altitude', 'dynamic_pressure', 'elevation', 'equivalent_air_speed', 'g_force', 'heading', 'horizontal_speed', 'latitude', 'longitude', 'mach', 'mean_altitude', 'pitch', 'roll',  'sideslip_angle', 'speed', 'speed_of_sound',  'static_air_temperature', 'static_pressure', 'static_pressure_at_msl', 'surface_altitude', 'terminal_velocity',  'total_air_temperature', 'true_air_speed', 'vertical_speed']

vectors = ['aerodynamic_force', 'center_of_mass', 'direction', 'drag', 'lift', 'velocity']
quaternions = ['rotation']


def Add_Dash(server):
    dash_app = Dash(server=server, url_base_pathname='/kdash/')
    dash_app.title = 'kerbal dashboard'
    dash_app.css.config.serve_locally = True
    dash_app.scripts.config.serve_locally = True
    conn = krpc.connect(name='kdash')
    vessel = conn.space_center.active_vessel
    refframe = vessel.orbit.body.reference_frame
    ranges = []
    def getFlightChars(x):
        j = {i: getattr(x, i) for i in floats}
        j['time'] = time()
        return j
    flightStats = conn.add_stream(vessel.flight, refframe)
    temps.append(getFlightChars(flightStats()))

    dash_app.layout = html.Div(id='flex-container', className='flex-container', children=[
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
            dcc.Interval(id='interval-component', interval = 1000, n_intervals=0),
            dcc.Store(id='storage', storage_type='session'),
                ]
            )

    @dash_app.callback(Output('storage', 'data'),
                        [Input('interval-component', 'n_intervals')],
                        )
    def store_data(n):
        if n is None:
            raise PreventUpdate
        temps.append(getFlightChars(flightStats()))
        # print('updated storage', n)
        return temps[-1]

    def update_gauge(d, prop):
        return d[prop] or 0

    def update_gauge_range_min(d, prop, minimum):
        return min(d[prop] or 0, minimum)

    def update_gauge_range_max(d, prop, maximum):
        return max(d[prop] or 0, maximum)


    for i in floats:
        dash_app.callback(Output(i, 'min'),
                        [Input('storage', 'data')],
                        [State(i, 'id'),
                        State(i, 'min')])(update_gauge_range_min)
    for i in floats:
        dash_app.callback(Output(i, 'max'),
                            [Input('storage', 'data')],
                            [State(i, 'id'),
                            State(i, 'max')])(update_gauge_range_max)
    for i in floats:
        dash_app.callback(Output(i, 'value'),
                            [Input('storage', 'data')],
                            [State(i, 'id')])(update_gauge)

    @dash_app.callback(Output('exGraph', 'extendData'),
                        [Input('interval-component', 'n_intervals')])
                        # [State('exGraph', 'figure')])
    def update_therm_graph(n):
        return [ {  'x': [temps[-1]['time']] ,
                    'y' : [temps[-1]['speed']] } ]


    return dash_app.server
