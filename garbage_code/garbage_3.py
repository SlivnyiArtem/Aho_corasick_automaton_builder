import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

from process import AhoKorasicProcessWindow

app = dash.Dash(__name__)
server = app.server

edges = pd.DataFrame.from_dict({'from': ['earthquake', 'earthquake', 'burglary', 'alarm', 'alarm'],
                                'to': ['report', 'alarm', 'alarm', 'John Calls', 'Mary Calls']})

_, labels, _, _, _ = AhoKorasicProcessWindow.calculate("акк акаунт")

print(labels)
node_dict = {}
for start, end in labels.keys():
    node_dict[start] = end
    print(node_dict)
    # source.append(start)
    # target.append(end)

visited_nodes = set()

cy_edges = []
cy_nodes = []

# for index, row in edges.iterrows():
# source, target = row['from'], row['to']
for source in node_dict.keys():
    target = node_dict[source]
    print(type(source))
    if source not in visited_nodes:
        visited_nodes.add(source)
        cy_nodes.append({"data": {"id": source, "label": source}})
    if target not in visited_nodes:
        visited_nodes.add(target)
        cy_nodes.append({"data": {"id": target, "label": target}})

    cy_edges.append({
        'data': {
            'source': source,
            'target': target
        }
    })

# define stylesheet
stylesheet = [
    {
        "selector": 'node',
        'style': {"label": "data(label)", }
    },
    {
        "selector": 'edge',
        "style": {
            "target-arrow-shape": "triangle",
            'curve-style': 'bezier'
        }
    }]

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-layout',
        options=[
            {'label': 'random',
             'value': 'random'},
            {'label': 'grid',
             'value': 'grid'},
            {'label': 'circle',
             'value': 'circle'},
            {'label': 'concentric',
             'value': 'concentric'},
            {'label': 'breadthfirst',
             'value': 'breadthfirst'},
            {'label': 'cose',
             'value': 'cose'}],
        value='grid'
    ),
    html.Div(children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=cy_edges + cy_nodes,
            style={
                'height': '95vh',
                'width': '100%'
            },
            stylesheet=stylesheet
        )
    ])
])


@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}


if __name__ == '__main__':
    app.run_server(debug=False)
