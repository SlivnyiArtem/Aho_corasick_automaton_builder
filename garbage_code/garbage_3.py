import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

from process import AhoKorasicProcessWindow


def generate_table():
    data = {'Cap': ['A', 'B', 'C', 'F'], 'non-Cap': ['a', 'b', 'c', "F"], 'non-Cap2': ['a', 'b', 'c', "F"]}
    df = pd.DataFrame(data)

    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ])for i in range(len(df))]
    )


app = dash.Dash(__name__)
server = app.server

# edges = pd.DataFrame.from_dict(
#     {
#         "from": ["earthquake", "earthquake", "burglary", "alarm", "alarm"],
#         "to": ["report", "alarm", "alarm", "John Calls", "Mary Calls"],
#     }
# )

_, visualize_dict, _, _, _, node_dict = AhoKorasicProcessWindow.calculate("акк акаунт")
# print(node_dict)
# print(frame)

visited_nodes = set()

cy_edges = []
cy_nodes = []
print(visualize_dict)
for source in node_dict.keys():
    node_targets = node_dict[source]
    for target in node_targets:
        if source not in visited_nodes:
            visited_nodes.add(source)
            cy_nodes.append({"data": {"id": source, "label": source}})
        if target not in visited_nodes:
            visited_nodes.add(target)
            cy_nodes.append({"data": {"id": target, "label": target}})

        cy_edges.append({"data": {"source": source, "target": target}})

# define stylesheet
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
            "curve-style": "bezier",
        },
    },
]

app.layout = html.Div(
    [
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
                    id="cytoscape",
                    elements=cy_edges + cy_nodes,
                    style={"height": "75vh", "width": "100%"},
                    stylesheet=stylesheet,
                )
            ]
        ),
        html.Div(children=[
            generate_table()
        ]),
    ]
)


@app.callback(Output("cytoscape", "layout"), [Input("dropdown-layout", "value")])
def update_cytoscape_layout(layout):
    return {"name": layout}


if __name__ == "__main__":
    app.run_server(debug=False)
