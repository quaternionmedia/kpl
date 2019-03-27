import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from kpl import kpl
import kdash, kmap


kpl.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@kpl.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/kdash':
         return kdash.layout
    elif pathname == '/kmap':
         return kmap.layout
    else:
        return '404'

if __name__ == '__main__':
    kpl.run_server(host='0.0.0.0', port=8888, debug=True)
