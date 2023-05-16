import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dash, html, dcc, Input, Output

from garbage_code.cyto_data import Singletone
from garbage_code.data_service import generate_graph, generate_table, get_random_words

app = dash.Dash(__name__)
server = app.server
Data = Singletone()
generate_graph(Data)


stylesheet = [
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

app.layout = html.Div(
    children=[
        dbc.Button("display graph", id="button-display-1"),
        dbc.Button("display table", id="button-display-2"),
        dbc.Button("display lambda", id="button-display-3"),
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
                    stylesheet=stylesheet,
                )
            ]
        ),
        html.Div(
            children=[
                dbc.Container(
                    id="table",
                )
            ]
        ),
    ]
)


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
