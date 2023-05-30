# import json
#
# import dash
# import dash_bootstrap_components as dbc
# import dash_cytoscape as cyto
# import dash_html_components as html
# import requests
# from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
#
#
# def load_json(st):
#     if "http" in st:
#         return requests.get(st).json()
#     else:
#         with open(st, "rb") as f:
#             x = json.load(f)
#         return x
#
#
# app = dash.Dash(__name__)
# server = app.server
#
# # Load Data
# default_elements = load_json("https://js.cytoscape.org/demos/colajs-graph/data.json")
# stylesheet = load_json("https://js.cytoscape.org/demos/colajs-graph/cy-style.json")
#
# # App
# app.layout = html.Div(
#     children=[
#         dbc.Button("display", id="btn_display"),
#         # dbc.Button("redraw", id="btn_redraw"),
#         html.Div(
#             [
#                 cyto.Cytoscape(
#                     id="cytoscape-responsive-layout",
#                     elements=default_elements,
#                     stylesheet=stylesheet,
#                     layout={
#                         "name": "cose",
#                     },
#                 )
#             ],
#         ),
#     ]
# )
#
#
# @app.callback(Output("cytoscape-responsive-layout", "elements"), Input("btn_display", "n_clicks"))
# # prevent_initial_call=True) ?????
# def redraw(n: int):
#     if n is not None and n % 2 == 1:
#         elements = []
#     else:
#         elements = default_elements
#     return elements
#
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8052)
