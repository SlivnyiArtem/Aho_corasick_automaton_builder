from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from algorithm import service_funcs, Aho_Korasic_Node, graph_visualizer, table_visualizer


class AhoKorasicWindow(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.restart_btn = QPushButton(self)
        self.restart_btn.setGeometry(QtCore.QRect(450, 700, 300, 50))
        self.restart_btn.setObjectName("restart_btn")
        self.restart_btn.setFont(QtGui.QFont('Times', 17))
        self.restart_btn.clicked.connect(self.restart)

        self._retranslate_ui()
        self.get_text()

    def calculate(self, text):
        input_data = text
        prefixes = service_funcs.get_prefixes(service_funcs.get_words_from_str(input_data))
        abc = service_funcs.get_abc_from_str(input_data)
        node_dict = {}
        visualize_dict = {}
        for prefix in prefixes:
            node = Aho_Korasic_Node.AhoKorasicNode(prefix, abc, prefixes)
            visualize_dict[(node.value, 'lamda-link')] = node.suffix_link
            visualize_dict[(node.value[:-1], node.value)] = node.value[-1]
            node_dict[node.value] = node

        columns_list = []
        for command_word in abc:
            columns_list.append(command_word)
        table_visualizer.visualize_table(columns_list, list(node_dict.values()))
        table_visualizer.tkinter_visualizer(columns_list, list(node_dict.values()))
        graph_visualizer.visualize_graph(visualize_dict)
        '''
        Aho_Korasic_Node.AhoKorasicNode("кас", service_funcs.get_abc_from_str(input_data),
                                        service_funcs.get_prefixes
                                        (service_funcs.get_words_from_str(input_data)))
        '''

    def get_text(self):
        text, okPressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.calculate(text)

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.restart_btn.setText(_translate("Preparing", "Другой словарь"))

    def restart(self):
        self.get_text()
