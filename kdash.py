import glob
from pathlib import Path, PurePath
from dash import Dash
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
temps = deque([{'time':None, 'speed':None}], maxlen=10)
# temps = pd.DataFrame({  'temps': [0],
                        # 'times': [time()] })


floats = [ 'angle_of_attack',  'atmosphere_density', 'bedrock_altitude', 'dynamic_pressure', 'elevation', 'equivalent_air_speed', 'g_force', 'heading', 'horizontal_speed', 'latitude', 'lift', 'longitude', 'mach', 'mean_altitude', 'pitch', 'roll',  'sideslip_angle', 'speed', 'speed_of_sound',  'static_air_temperature', 'static_pressure', 'static_pressure_at_msl', 'surface_altitude', 'terminal_velocity',  'total_air_temperature', 'true_air_speed', 'velocity', 'vertical_speed']

vectors = ['aerodynamic_force', 'center_of_mass', 'direction', 'drag', ]
quaternions = ['rotation']


def Add_Dash(server):
    dash_app = Dash(server=server, url_base_pathname='/kdash/')
    dash_app.title = 'kerbal dashboard'
    dash_app.css.config.serve_locally = True
    dash_app.scripts.config.serve_locally = True
    conn = krpc.connect(name='kdash')
    vessel = conn.space_center.active_vessel
    refframe = vessel.orbit.body.reference_frame
    def getFlightChars(x):
        j = {i: getattr(x, i) for i in floats}
        j['time'] = time()
        return j
    flightStats = conn.add_stream(vessel.flight, refframe)
    # flightStats.add_callback(getFlightChars)
    # flightStats.start()
    # dash_app.css.append_css({
    #     "external_url": "https://derp.sfo2.digitaloceanspaces.com/style.css"
    #     })

    # Create layout
    dash_app.layout = html.Div(id='flex-container', className='flex-container', children=[
            html.Div(id='header', className='twelve columns', style= {'align': 'center', 'background-color': '#222'}, children=[
                html.H1(className='two columns', children='KPL!'),
                html.H2(className='eight columns', children='Kerbal Propulsion Laborotory'),
                html.H3(className='two columns', children='Dashboard')
                ]),
            html.Div(id='speeds', className='twelve columns', children=[
                daq.Gauge(id='therm', label='speed', min=0, max=200, value=0, className='three columns', labelPosition='bottom', showCurrentValue=True, style={'padding-left': '10%'}),
                # dcc.Graph(id='thermGraph'),
                ex.ExtendableGraph(id='exGraph', className='nine columns', figure={'data': [{'x':[], 'y':[]}]}, )
                ]),
            html.Div(id='gauges', className='twelve columns', children=[
                # get_datasets()
                *[ daq.Gauge(id=i, label=i, min=0, max=1000, value=0, size=110, labelPosition='bottom', showCurrentValue=True, className='one column', style={'padding-left': '5%'}, ) for i in floats]
                ]),
            dcc.Interval(id='interval-component', interval = 1000, n_intervals=0),
            dcc.Store(id='session'),#, storage_type='session'),
                ]
            )


    @dash_app.callback([Output('therm', 'value'), Output('therm', 'max')],
                        [Input('interval-component', 'n_intervals')],
                        [State('therm', 'max')])
    def update_therm(n, m):
        temps.append(getFlightChars(flightStats()))
        s = temps[-1]['speed']
        # print('speed: ', s)
        m = max(s, m)
        return [s, m]

    # @dash_app.callback(Output('therm', 'max'),
    #                     [Input('interval-component', 'n_intervals')],
    #                     )
    # def update_therm_range(value):
    #     print(value)
    #     if value > 2000:
    #         return value


    @dash_app.callback(Output('exGraph', 'extendData'),
                        [Input('interval-component', 'n_intervals')],
                        [State('exGraph', 'figure')])
    def update_therm_graph(n, fig):

        return [ {  'x': [temps[-1]['time']] ,
                    'y' : [temps[-1]['speed']] } ]


    return dash_app.server







#
# def get_datasets():
#     """Gets all CSVS in datasets directory."""
#     data_filepath = list(p.glob('application/datasets/*.csv'))
#     arr = []
#     for index, csv in enumerate(data_filepath):
#         print(PurePath(csv))
#         df = pd.read_csv(data_filepath[index]).head(10)
#         table_preview = dash_table.DataTable(
#             id='table' + str(index),
#             columns=[{"name": i, "id": i} for i in df.columns],
#             data=df.to_dict("rows"),
#             sorting=True,
#         )
#         arr.append(table_preview)
#     return arr
