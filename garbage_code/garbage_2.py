import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import networkx as nwx
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
visited_nodes = set()

# Important_elements!!!
cy_edges = []
cy_nodes = []

for index, row in edges.iterrows():
    source, target = row["from"], row["to"]

    if source not in visited_nodes:
        visited_nodes.add(source)
        cy_nodes.append({"data": {"id": source, "label": source}})
    if target not in visited_nodes:
        visited_nodes.add(target)
        cy_nodes.append({"data": {"id": target, "label": target}})

    cy_edges.append({"data": {"source": source, "target": target}})

stylesheet = [
    {"selector": "node", "style": {"label": "data(label)"}},
    {"selector": "edge", "style": {"target-arrow-shape": "triangle", "curve-style": "bezier"}},
]

# define layout
layout = html.Div(
    [
        dcc.Dropdown(id="dropdown-layout", value="grid"),
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

# import matplotlib.pyplot as plt
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, \
#     QHBoxLayout, QInputDialog, QLineEdit, QDesktopWidget
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#
# import Aho_Korasic_Node
# import graph_constructor
# import service_funcs
#
#
# class AhoKorasicProcessWindow(QWidget):
#     def __init__(self):
#
#         super(AhoKorasicProcessWindow, self).__init__()
#
#         self.setGeometry(100, 100, 1000, 1000)
#
#         self.center()
#         self.setWindowTitle('AhoCorasik window')
#         self.grid = QGridLayout()
#         self.setLayout(self.grid)
#
#         self.verticalGroupBox = QGroupBox()
#         # self.verticalGroupBox.setGeometry(0, 0, 50, 1000)
#         layout = QHBoxLayout()
#
#         # button = QPushButton("Новый словарь")
#         # button.setObjectName("restart_btn")
#         # button.setGeometry(QtCore.QRect(450, 700, 300, 50))
#         # button.setFont(QtGui.QFont('Times', 17))
#         # button.clicked.connect(self.restart)
#         #
#         # layout.addWidget(button)
#         layout.setSpacing(10)
#
#         self.verticalGroupBox.setLayout(layout)
#         self.figure = plt.figure()
#         self.canvas = FigureCanvas(self.figure)
#         self.grid.addWidget(self.canvas, 0, 1, 9, 9)
#         # self.grid.addWidget(self.verticalGroupBox, 300, 5)
#         # self.table = QTableWidget(self)
#         # self.grid.addWidget(self.table, 100, 1, 9, 9)
#
#         self.show()
#
#     def calculate(self, text):
#         input_data = text
#         prefixes = service_funcs.get_prefixes(service_funcs.get_words_from_str(input_data))
#         abc = service_funcs.get_abc_from_str(input_data)
#         node_dict = {}
#         visualize_dict = {}
#         for prefix in prefixes:
#             node = Aho_Korasic_Node.AhoKorasicNode(prefix, abc, prefixes)
#             start_node = node.value[:-1]
#             if start_node == '':
#                 start_node = "NullNode"
#             visualize_dict[(start_node, node.value)] = node.value[-1]
#             node_dict[node.value] = node
#
#         for node in node_dict.values():
#             if node.suffix_link is not None:
#                 visualize_dict[(node.value, node.suffix_link)] = "\u03bb"
#             else:
#                 visualize_dict[(node.value, "NullNode")] = "\u03bb"
#         graph = graph_constructor.form_graph(visualize_dict)
#         return graph, visualize_dict, prefixes, node_dict, abc
#
#     def restart(self):
#         text, _ = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
#         graph, labels, _, _, _ = self.calculate(text)
#         # labels - dict : {(node_from_name, node_to_name):label_str, ...}
#         # graph - nwx.DiGraph + exec add_edges_from with dict : {(node_from_name, node_to_name):label_str, ...}
#         print(graph)
#         print(labels)
#         # self.draw_table(prefixes, node_dict, abc)
#         self.draw_scheme(graph, labels)
#
#     # def draw_table(self, prefixes, node_dict, abc):
#     #     prefixes = list(set(prefixes))
#     #     prefixes.sort(key=lambda k: (len(k), k))
#     #     abc.sort()
#     #     columns_list = ["NodeValue"] + abc + ["\u03bb"]
#     #     self.table.setColumnCount(len(columns_list))
#     #     self.table.setRowCount(len(prefixes))
#     #     self.table.setHorizontalHeaderLabels(columns_list)
#     #     for i in range(self.table.rowCount()):
#     #         for j in range(self.table.columnCount()):
#     #             if j == 0:
#     #                 value = prefixes[i]
#     #             elif j == self.table.columnCount() - 1:
#     #                 value = node_dict.get(prefixes[i]).suffix_link
#     #             else:
#     #                 value = node_dict.get(prefixes[i]).prefix_links.get(columns_list[j])
#     #             if value is None:
#     #                 value = "\u03bb"
#     #             self.table.setItem(i, j, QTableWidgetItem(value))
#     #     self.table.resizeColumnsToContents()
#
#     def draw_scheme(self):
#         self.figure.clf()
#         graph = nwx.DiGraph()
#         graph.add_edges_from(edge_dictionary.keys())
#         # layout = graphviz_layout(graph, prog="dot")
#         nwx.draw(graph, layout, with_labels=True)
#         nwx.draw_networkx_edge_labels(graph, layout, edge_labels=labels)
#         self.canvas.draw_idle()
#         pass
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#
# import sys
# import PyQt5
#
#
# # from PyQt5 import QtWidgets, QtCore
#
#
# class MainWindow(PyQt5.QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Ахо-Корасик")
#         self.setFixedSize(1200, 800)
#
#         self.central_widget = PyQt5.QtWidgets.QWidget(self)
#         self.stacked_widget = PyQt5.QtWidgets.QStackedWidget(self.central_widget)
#         self.stacked_widget.setGeometry(PyQt5.QtCore.QRect(0, 0, 1200, 800))
#         self.setCentralWidget(self.central_widget)
#         self.stacked_widget.addWidget(AhoKorasicProcessWindow(self))
#
#
# if __name__ == "__main__":
#     app = PyQt5.QtWidgets.QApplication(sys.argv)
#     w = AhoKorasicProcessWindow()
#     w.show()
#     sys.exit(app.exec_())
