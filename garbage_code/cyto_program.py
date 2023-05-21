import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import Input, Output, dash, dcc, html, State

from garbage_code.cyto_data import Singletone
from garbage_code.data_service import generate_graph, generate_table, get_random_words

app = dash.Dash(__name__)
server = app.server
Data = Singletone()
generate_graph(Data)


def make_style():
    return [
        {
            "selector": "node",
            "style": {
                "opacity": 0.9,
                "label": "data(label)",
                "background-color": "#07ABA0",
            },
        },
        {
            "selector": "edge",
            "style": {
                "target-arrow-color": "#C5D3E2",
                "target-arrow-shape": "triangle",
                "line-color": "#C5D3E2",
                "label": "data(label)",
                "curve-style": "bezier",
            },
        },
    ]


def make_layout():
    # app.layout = html.Div([
    #
    # ])

    return html.Div(
        children=[
            html.Div(dcc.Input(id='input_on_submit', type='text', value="text_inf")),
            html.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id='container-button-basic',
                     children='Enter a value and press submit'),

            dcc.Input(id='username', value='Initial Value', type='text'),
            html.Button(id='submit-button', type='submit', children='Submit'),
            html.Div(id='output_div'),

            # #
            # html.Div(dcc.Input(id='input_on_submit', type='text', value="text_inf")),
            # html.Button('Submit', id='submit-val', n_clicks=0),
            # html.Div(id='container-button-basic',
            #          children='Enter a value and press submit'),
            # html.Div(dcc.Input(id='input-on-submit-2', type='text')),
            # html.Button('Submit-2', id='submit-val-2', n_clicks=0),
            # html.Div(id='container-button-basic-2',
            #          children='Enter a value and press submit'),
            # #
            #
            # dbc.Button("display graph", id="button-display-1"),
            # dbc.Button("display table", id="button-display-2"),
            # dbc.Button("display lambda", id="button-display-3"),
            dcc.Dropdown(
                id="dropdown-layout",
                options=[
                    {"label": "random", "value": "random"},
                    {"label": "grid", "value": "grid"},
                    {"label": "circle", "value": "circle"},
                    {"label": "concentric", "value": "concentric"},
                    {"label": "breadthfirst", "value": "breadthfirst"},
                    {"label": "cose", "value": "cose"},
                ],
                value="grid",
            ),
            html.Div(
                children=[
                    cyto.Cytoscape(
                        id="graph",
                        elements=Data.cy_edges + Data.cy_nodes,
                        style={"height": "75vh", "width": "100%"},
                        stylesheet=make_style(),
                    )
                ]
            ),
            html.Div(
                children=[
                    dbc.Container(id="table", )
                ]
            ),
        ]
    )


# stylesheet = [
#     {
#         "selector": "node",
#         "style": {
#             "opacity": 0.9,
#             "label": "data(label)",
#             "background-color": "#07ABA0",
#         },
#     },
#     {
#         "selector": "edge",
#         "style": {
#             "target-arrow-color": "#C5D3E2",
#             "target-arrow-shape": "triangle",
#             "line-color": "#C5D3E2",
#             "label": "data(label)",
#             "curve-style": "bezier",
#         },
#     },
# ]
#
# stylesheet = [
#
# ]

app.layout = make_layout()


@app.callback(Output('output_div', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('username', 'value')],
                  )
def update_output(clicks, input_value):
    # if clicks is not None:
    print(clicks, input_value)


@app.callback([Input("input_on_submit", "value")])
def update_cytoscape_sdf(layout):
    print("value")
    return {"name": layout}


@app.callback(Output("graph", "layout"), [Input("dropdown-layout", "value")])
def update_cytoscape_layout(layout):
    return {"name": layout}


@app.callback(Output("graph", "elements"), Input("button-display-1", "n_clicks"))
def hide_graph(n: int):
    if n is not None and n % 2 == 1:
        return []
    else:
        return Data.cy_edges + Data.cy_nodes


@app.callback(Output("table", "children"), Input("button-display-2", "n_clicks"))
def hide_table(n: int):
    if n is not None and n % 2 == 1:
        return []
    else:
        table, df = generate_table(Data.V)
        return table


if __name__ == "__main__":
    r = get_random_words(3, 5)
    print(r)
    app.run_server(debug=False)
