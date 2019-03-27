import dash
import krpc

kpl = dash.Dash(__name__,suppress_callback_exceptions = True)

kpl.title = 'KPL'
kpl.css.config.serve_locally = True
kpl.scripts.config.serve_locally = True
kpl.conn = krpc.connect(name='kpl')
print('kpl connected!', kpl.conn)

server = kpl.server
