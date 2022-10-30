from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from algorithm import service_funcs, Aho_Korasic_Node, graph_visualizer


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

    graph_visualizer.visualize_graph(visualize_dict)


class AhoKorasicWindow(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.restart_btn = QPushButton(self)
        self.restart_btn.setGeometry(QtCore.QRect(450, 700, 300, 50))
        self.restart_btn.setObjectName("restart_btn")
        self.restart_btn.setFont(QtGui.QFont('Times', 17))
        self.restart_btn.clicked.connect(self.restart)

        self.re_translate_ui()
        self.get_text()

    def get_text(self):
        text, ok_pressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        if ok_pressed and text != '':
            calculate(text)

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.restart_btn.setText(_translate("Preparing", "Другой словарь"))

    def restart(self):
        self.get_text()
