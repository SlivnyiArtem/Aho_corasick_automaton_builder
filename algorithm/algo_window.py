from PyQt5 import QtGui
from PyQt5 import QtCore
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFrame, QInputDialog, QPushButton, QTableWidget, QGridLayout, QLineEdit, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as cnv
import networkx as nwx

from algorithm import service_funcs, Aho_Korasic_Node, graph_constructor


def calculate(text):
    input_data = text
    prefixes = service_funcs.get_prefixes(service_funcs.get_words_from_str(input_data))
    abc = service_funcs.get_abc_from_str(input_data)
    node_dict = {}
    visualize_dict = {}
    for prefix in prefixes:
        node = Aho_Korasic_Node.AhoKorasicNode(prefix, abc, prefixes)
        visualize_dict[(node.value[:-1], node.value)] = node.value[-1]
        node_dict[node.value] = node

    for node in node_dict.values():
        if node.suffix_link is not None:
            visualize_dict[(node.value, node.suffix_link)] = "λ"
        else:
            visualize_dict[(node.value, "")] = "λ"
    graph = graph_constructor.form_graph(visualize_dict)
    is_planar, _ = nwx.check_planarity(nwx.Graph(graph))
    if is_planar:
        layout = nwx.planar_layout(graph)
    else:
        layout = nwx.circular_layout(graph)
    return graph, layout, visualize_dict, prefixes, node_dict, abc, is_planar


class AhoKorasicWindow(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.dialog_btn = QInputDialog()
        self.restart_btn = QPushButton(self)
        self.restart_btn.setGeometry(QtCore.QRect(450, 700, 300, 50))
        self.restart_btn.setObjectName("restart_btn")
        self.restart_btn.setFont(QtGui.QFont('Times', 17))
        self.restart_btn.clicked.connect(self.restart)

        self.graph = plt.figure()
        self.cnv = cnv(self.graph)





        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.cnv)
        self.grid.addWidget(self.restart_btn, 100, 100, 5, 5)
        self.table = QTableWidget(self)
        self.grid.addWidget(self.table, 100, 0)
        # self.grid.update()

        self.show()
        self.re_translate_ui()
        self.get_text()

    def get_text(self):
        text, ok_pressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        if ok_pressed and text != '':

            graph, graph_pos, labels, prefixes, node_dict, abc, is_planar = calculate(text)
            self.grid.update()
            # self.cnv.flush_events()

            if is_planar:
                nwx.draw_planar(graph, with_labels=True)
            else:
                nwx.draw_circular(graph)
            nwx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=labels)
            self.grid.update()
            self.cnv.draw_idle()
            # self.cnv.



            abc.sort()
            columns_list = ["NodeValue"] + abc + ["λ"]

            # self.cnv.flush_events()
            # self.cnv.draw_idle()
            # self.cnv.flush_events()


            self.table.setColumnCount(len(columns_list))
            self.table.setRowCount(len(prefixes))
            self.table.setHorizontalHeaderLabels(columns_list)
            for i in range(self.table.rowCount()):
                for j in range(self.table.columnCount()):
                    if j == 0:
                        value = prefixes[i]
                    elif j == self.table.columnCount() - 1:
                        value = node_dict.get(prefixes[i]).suffix_link
                    else:
                        value = node_dict.get(prefixes[i]).prefix_links.get(columns_list[j])
                    if value is None:
                        value = "λ"
                    self.table.setItem(i, j, QTableWidgetItem(value))
            self.table.resizeColumnsToContents()
            self.table.resizeColumnsToContents()

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.restart_btn.setText(_translate("Preparing", "Другой словарь"))

    def restart(self):
        plt.close("all")
        self.get_text()
