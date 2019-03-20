import dash
import kdash

from flask import Flask

server = kdash.Add_Dash(Flask(__name__))

# dash_app = dash.Dash(server=server, url_base_pathname='/dataview/')

kdash.Add_Dash

if __name__ == '__main__':
    server.run('0.0.0.0', 8888, debug=True)
