import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from algorithm.generators import generate_random_words, generate_lambda_table
from algorithm.generators import generate_table
from algorithm.processor import calculate

app = dash.Dash(__name__)
server = app.server

style = {
    'display': 'flex',
    'flex-direction': 'row',
    'justify-content': 'space-around',
    'align-items': 'center',
    'border': '1px solid black',
    'padding': '10px',
}

input_style = {
    'margin': '10px',
    'width': '100%',
    'height': '50px',
}

button_style = {
    'margin': '10px',
    'width': '100%',
    'height': '50px',
    # 'background-color': 'blue',
    'color': 'white',
}

graph_style = {
    'display': 'block',
    'margin': '10px',
    'width': '50%',
}

table_style = {
    'display': 'block',
    'margin': '10px',
    'width': '50%',
}

stylesheet = [
    {
        "selector": "node",  # For all nodes
        "style": {
            "opacity": 0.9,
            "label": "data(label)",
            "background-color": "#07ABA0",
        },
    },
    {
        "selector": "edge",  # For all edges
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
        html.Div(dcc.Input(id='input-on-submit', type='text', style=input_style)),
        html.Button('Generate', id='submit-val', n_clicks=0, style=button_style),
        ##
        html.Div(dcc.Input(id='input-random-generator', type='value', style=input_style)),
        html.Button('Generate_RND', id='submit-random-generator-input', n_clicks=0, style=button_style),
        ##
        dcc.Dropdown(
            id='display_graph',
            options=[
                {'label': 'Show graph', 'value': 'on'},
                {'label': 'Hide graph', 'value': 'off'}
            ],
            value='on'
        ),
        dcc.Dropdown(
            id='display_table',
            options=[
                {'label': 'Show table', 'value': 'on'},
                {'label': 'Hide table', 'value': 'off'}
            ],
            value='on'
        ),
        dcc.Dropdown(
            id='display_lambda_table',
            options=[
                {'label': 'Show table', 'value': 'on'},
                {'label': 'Hide table', 'value': 'off'}
            ],
            value='on'
        ),
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
            id="wrapper_graph",
            children=[
                cyto.Cytoscape(
                    id="graph",
                    elements=[] + [],
                    style={"height": "75vh", "width": "100%"},
                    stylesheet=stylesheet,
                )
            ],
            # style=graph_style,
            style={'display': 'block'}
        ),
        html.Div(
            id="wrapper_table",
            children=[
                dbc.Container(
                    id="table",
                    children=generate_table({})
                )
            ],
            # style=table_style
            style={'display': 'block',
                   "margin-left": "150px", }
        ),
        html.Div(
            id="wrapper_lambda_table",
            children=[
                dbc.Container(
                    id="lambda_table",
                    children=generate_lambda_table({})
                )
            ],
            # style=table_style
            style={'display': 'block',
                   # "margin-left": "150px",
                   }
        ),
    ],
    # style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}
    # style={
    #     # "width": "190px",
    #     # "height": "40px",
    #     "margin-left": "85px",
    #     "margin-top": "100px",
    #     "margin-right": "85px",
    #     # "display": "inline-block",
    #     "verticalAlign": "middle",
    #     "font-family": "Helvetica",
    # },
)


@app.callback(
    Output("graph", "elements", allow_duplicate=True),
    Output("table", "children", allow_duplicate=True),
    Output("lambda_table", "children", allow_duplicate=True),

    Input('submit-val', 'n_clicks'),
    Input('submit-random-generator-input', 'n_clicks'),
    State('input-on-submit', 'value'),
    State('input-random-generator', 'value'),
    prevent_initial_call=True,
)
def update_output(n_clicks_1, n_clicks_2, value, rnd_cnt):
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'submit-random-generator-input':
        value = " ".join(generate_random_words(3, int(rnd_cnt)))
    _, visualize_dict, _, nodes, _, node_dict = calculate(value)
    visited_nodes = set()
    cy_edges = []
    cy_nodes = []

    for source in node_dict.keys():
        node_targets = node_dict[source]
        for target in node_targets:
            if source not in visited_nodes:
                visited_nodes.add(source)
                cy_nodes.append({"data": {"id": source, "label": source}})
            if target not in visited_nodes:
                visited_nodes.add(target)
                cy_nodes.append({"data": {"id": target, "label": target}})
            cy_edges.append(
                {"data": {"source": source, "target": target, "label": visualize_dict[(source, target)]}})
    return cy_edges + cy_nodes, generate_table(visualize_dict), generate_lambda_table(nodes)


@app.callback(
    Output('container-button-basic-2', 'children'),
    Input('submit-val-2', 'n_clicks'),
    State('input-on-submit-2', 'value')
)
def update_output_next(n_clicks, value):
    return 'The input value was "{}'.format(value)


@app.callback(Output("graph", "layout"), [Input("dropdown-layout", "value")])
def update_cytoscape_layout(layout):
    return {"name": layout}


@app.callback(
    Output(component_id='wrapper_graph', component_property='style'),
    [Input(component_id='display_graph', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}


@app.callback(
    Output(component_id='wrapper_table', component_property='style'),
    [Input(component_id='display_table', component_property='value')])
def show_hide_element_1(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}


@app.callback(
    Output(component_id='wrapper_lambda_table', component_property='style'),
    [Input(component_id='display_lambda_table', component_property='value')])
def show_hide_element_2(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}


if __name__ == "__main__":
    app.run_server(debug=False)
