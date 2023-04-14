import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

# prepare data
edges = pd.DataFrame.from_dict(
    {
        "from": ["earthquake", "earthquake", "burglary", "alarm", "alarm"],
        "to": ["report", "alarm", "alarm", "John Calls", "Mary Calls"],
    }
)
nodes = set()

cy_edges = []
cy_nodes = []

for index, row in edges.iterrows():
    source, target = row["from"], row["to"]

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append({"data": {"id": source, "label": source}})
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append({"data": {"id": target, "label": target}})

    cy_edges.append({"data": {"source": source, "target": target}})

# define stylesheet
stylesheet = [
    {
        "selector": "node",  # For all nodes
        "style": {
            "opacity": 0.9,
            "label": "data(label)",  # Label of node to display
            "background-color": "#07ABA0",  # node color
            "color": "#008B80",  # node label color
        },
    },
    {
        "selector": "edge",  # For all edges
        "style": {
            "target-arrow-color": "#C5D3E2",  # Arrow color
            "target-arrow-shape": "triangle",  # Arrow shape
            "line-color": "#C5D3E2",  # edge color
            "arrow-scale": 2,  # Arrow size
            "curve-style": "bezier",  # Default curve-If it is style, the arrow will not be displayed, so specify it
        },
    },
]

# define layout
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
                    style={"height": "95vh", "width": "100%"},
                    stylesheet=stylesheet,
                )
            ]
        ),
    ]
)


@app.callback(Output("cytoscape", "layout"), [Input("dropdown-layout", "value")])
def update_cytoscape_layout(layout):
    return {"name": layout}


if __name__ == "__main__":
    app.run_server(debug=False)
