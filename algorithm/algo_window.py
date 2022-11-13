from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import matplotlib.pyplot as plt
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
            visualize_dict[(node.value, node.suffix_link)] = "lambda"
        else:
            visualize_dict[(node.value, "")] = "lambda"
    graph = graph_constructor.form_graph(visualize_dict)
    return graph, nwx.planar_layout(graph), visualize_dict, prefixes, node_dict, abc






class AhoKorasicWindow(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.dialog_btn = QInputDialog()

        # self.dialog_btn =QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")


        self.restart_btn = QPushButton(self)
        self.restart_btn.setGeometry(QtCore.QRect(450, 700, 300, 50))
        self.restart_btn.setObjectName("restart_btn")
        self.restart_btn.setFont(QtGui.QFont('Times', 17))
        self.restart_btn.clicked.connect(self.restart)


        self.graph = plt.figure()
        self.cnv = cnv(self.graph)


        self.table = QTableWidget(self)






        '''
        data = {'Kitty': ['1', '2', '3', '3'],
                'Cat': ['4', '5', '6', '2'],
                'Meow': ['7', '8', '9', '5'],
                'Purr': ['4', '3', '4', '8'], }
        # Create Empty 5x5 Table
        self.table = QtGui.QTextTable(PrettyWidget)
        self.table.setRowCount(5)
        self.table.setColumnCount(5)
        # Enter data onto Table
        horHeaders = []
        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtGui.QTableWidgetItem(item)
                self.table.setItem(m, n, newitem)
        # Add Header
        self.table.setHorizontalHeaderLabels(horHeaders)
        # Adjust size of Table
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        '''


        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.cnv)
        grid.addWidget(self.restart_btn, 100,100,5,5)
        grid.addWidget(self.table, 100, 0)





        self.show()
        self.re_translate_ui()
        self.get_text()

    def get_text(self):
        text, ok_pressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        if ok_pressed and text != '':
            graph, graph_pos, labels, prefixes, node_dict, abc = calculate(text)


            nwx.draw_planar(graph, with_labels=True)
            nwx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=labels)
            self.cnv.draw_idle()
            abc.sort()
            print(prefixes)
            print(node_dict)
            print(abc)

            # cnt1 = 1 + len(abc) + 1
            cnt2 = len(prefixes)
            list1 = ["NodeValue"] + abc + ["lambda"]
            cnt1 = len(list1)


            self.table.setColumnCount(cnt1)
            self.table.setRowCount(cnt2)
            self.table.setHorizontalHeaderLabels(list1)
            print("------")
            for i in range(cnt2):
                print(node_dict.get(prefixes[i]).prefix_links)
                for j in range(cnt1):
                    #j - текущее коммандное слово
                    #i - текущий префикс

                    if j == 0:
                        value = prefixes[i]
                    elif j == cnt1 - 1:
                        value = node_dict.get(prefixes[i]).suffix_link
                    else:
                        value = node_dict.get(prefixes[i]).prefix_links.get(list1[j])
                    if value is None:
                        value = "lambda"


                    # print("VVV")
                    # print(node_dict.get(prefixes[i]).value)
                    # print(node_dict.get(prefixes[i]).prefix_links)
                    # print(node_dict.get(prefixes[i]).suffix_link)
                    self.table.setItem(i, j, QTableWidgetItem(value))
            self.table.resizeColumnsToContents()
            self.table.resizeColumnsToContents()


    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.restart_btn.setText(_translate("Preparing", "Другой словарь"))

    def restart(self):
        plt.close("all")
        self.get_text()
