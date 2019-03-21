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
temps = deque(maxlen=10)
# temps = pd.DataFrame({  'temps': [0],
                        # 'times': [time()] })
# archive = []
p = Path('.')

flight_chars = ['aerodynamic_force', 'angle_of_attack',  'atmosphere_density', 'bedrock_altitude', 'center_of_mass', 'direction', 'drag', 'dynamic_pressure', 'elevation', 'equivalent_air_speed', 'g_force', 'heading', 'horizontal_speed', 'latitude', 'lift', 'longitude', 'mach', 'mean_altitude', 'pitch', 'roll', 'rotation', 'sideslip_angle', 'speed', 'speed_of_sound',  'static_air_temperature', 'static_pressure', 'static_pressure_at_msl', 'surface_altitude', 'terminal_velocity',  'total_air_temperature', 'true_air_speed', 'velocity', 'vertical_speed']

def Add_Dash(server):
    dash_app = Dash(server=server, url_base_pathname='/kdash/')
    conn = krpc.connect(name='kdash')
    vessel = conn.space_center.active_vessel
    refframe = vessel.orbit.body.reference_frame
    def getFlightChars(x):
        j = {i: getattr(x, i) for i in flight_chars}
        j['time'] = time()
        return j
    flightStats = conn.add_stream(vessel.flight, refframe)
    # flightStats.add_callback(getFlightChars)
    # flightStats.start()
    # dash_app.css.append_css({
    #     "external_url": "https://derp.sfo2.digitaloceanspaces.com/style.css"
    #     })

    # Create layout
    dash_app.layout = html.Div(id='flex-container', children=[
        html.H1(children='KPL!'),
        html.Div(children='Kerbal Propulsion Laborotory'),
        html.H3(children='- Dashboard -'),
        daq.Gauge(id='therm', min=0, max=330, value=0),
        html.P(id='thermValue'),
        # dcc.Graph(id='thermGraph'),
        ex.ExtendableGraph(id='exGraph', figure={'data': [{'x':[], 'y':[]}]}),
        dcc.Interval(id='interval-component', interval = 1000, n_intervals=0)
        # get_datasets()
        ]

      )


    @dash_app.callback(Output('therm', 'value'),
                        [Input('interval-component', 'n_intervals')])
    def update_therm(n):
        temps.append(getFlightChars(flightStats()))
        print('static air temp: ', temps[-1]['static_air_temperature'])
        return temps[-1]['static_air_temperature']


    @dash_app.callback(Output('exGraph', 'extendData'),
                        [Input('interval-component', 'n_intervals')],
                        [State('exGraph', 'figure')])
    def update_therm_graph(n, fig):

        return [ {  'x': [temps[-1]['time']] ,
                    'y' : [temps[-1]['static_air_temperature']] } ]


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
