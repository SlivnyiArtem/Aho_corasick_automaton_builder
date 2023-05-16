import random
import re
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from pandas import DataFrame

from process import AhoKorasicProcessWindow

cur_df: DataFrame


def get_random_lexem(lexem_length):
    vowels = 'уеыаоэяию'
    consonants = 'йцкнгшщзхфвпрлджчсмтб'
    res = []
    for i in range(lexem_length):
        res.append(random.choice(consonants) if i % 2 == 0 else random.choice(vowels))
    return "".join(res)


def get_random_words(lexem_length: int, random_list_len: int):
    common_lexem = get_random_lexem(lexem_length)
    miss_cnt = 0
    result = set()
    with open('../singular.txt', 'r', encoding="utf-8") as f:
        words = f.readlines()
    words = [s.strip("\n") for s in words]
    while True:
        if len(result) == random_list_len:
            break
        random_word: str = random.choice(words)
        if re.search(common_lexem, random_word) is not None:
            result.add(random_word)
        else:
            miss_cnt += 1
            if miss_cnt == 1000:
                common_lexem = get_random_lexem(lexem_length)
                miss_cnt = 0
    return result


r = get_random_words(3, 5)
print()

def copy_to_excel(path_to_excel: str):
    global cur_df
    cur_df.to_excel(path_to_excel)


def generate_table(table_dict):
    global cur_df
    cur_df = pd.DataFrame()
    # print(table_dict)
    for item in table_dict.keys():
        prefix, value = item
        cur_df.loc[prefix, table_dict[item]] = value
    # print(df)

    table = dbc.Table.from_dataframe(cur_df, index=True)
    return table


app = dash.Dash(__name__)
server = app.server

# edges = pd.DataFrame.from_dict(
#     {
#         "from": ["earthquake", "earthquake", "burglary", "alarm", "alarm"],
#         "to": ["report", "alarm", "alarm", "John Calls", "Mary Calls"],
#     }
# )

_, visualize_dict, _, _, _, node_dict = AhoKorasicProcessWindow.calculate("рама рамштайн")

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

        cy_edges.append({"data": {"source": source, "target": target, "label": visualize_dict[(source, target)]}})

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
            "label": "data(label)",
            "curve-style": "bezier",
        },
    },
]

app.layout = html.Div(
    children=[
        ##смотриздесь
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
                 children='Enter a value and press submit'),
        html.Div(dcc.Input(id='input-on-submit-2', type='text')),
        html.Button('Submit-2', id='submit-val-2', n_clicks=0),
        html.Div(id='container-button-basic-2',
                 children='Enter a value and press submit'),
        ##
        dbc.Button("display graph", id="button-display-1"),
        dbc.Button("display table", id="button-display-2"),
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
                    elements=cy_edges + cy_nodes,
                    style={"height": "75vh", "width": "100%"},
                    stylesheet=stylesheet,
                )
            ]
        ),
        html.Div(
            children=[
                dbc.Container(
                    # children=generate_table(visualize_dict),
                    id="table",
                    # elements=generate_table(visualize_dict),
                )
            ]
        ),
    ]
)


@app.callback(Output("graph", "layout"), [Input("dropdown-layout", "value")])
def update_cytoscape_layout(layout):
    return {"name": layout}


@app.callback(Output("graph", "elements"), Input("button-display-1", "n_clicks"))  # prevent_initial_call=True) ?????
def hide_graph(n: int):
    if n is not None and n % 2 == 1:
        return []
    else:
        return cy_edges + cy_nodes


@app.callback(Output("table", "children"), Input("button-display-2", "n_clicks"))  # prevent_initial_call=True) ?????
def hide_table(n: int):
    if n is not None and n % 2 == 1:
        return []
    else:
        return generate_table(visualize_dict)


if __name__ == "__main__":
    app.run_server(debug=False)
