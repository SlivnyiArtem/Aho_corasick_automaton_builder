import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input

if __name__ == '__main__':
    app = dash.Dash()

    app.layout = html.Div([
        dcc.Input(id='username', value='Initial Value', type='text'),
        html.Button(id='submit-button', type='submit', children='Submit'),
        html.Div(id='output_div')
    ])

    @app.callback(Output('output_div', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('username', 'value')],
                  )
    def update_output(clicks, input_value):
        if clicks is not None:
            print(clicks, input_value)

    app.run_server(host='0.0.0.0')