# import matplotlib.pyplot as plt
# from PyQt5 import QtCore, QtGui
# from PyQt5.QtWidgets import (
#     QDesktopWidget,
#     QGridLayout,
#     QGroupBox,
#     QHBoxLayout,
#     QInputDialog,
#     QLineEdit,
#     QPushButton,
#     QTableWidget,
#     QTableWidgetItem,
#     QWidget,
# )
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#
#
# class AhoKorasicProcessWindow(QWidget):
#     def __init__(self):
#         super(AhoKorasicProcessWindow, self).__init__()
#
#         self.setGeometry(100, 100, 1000, 1000)
#
#         self.center()
#         self.setWindowTitle("AhoCorasik window")
#         self.grid = QGridLayout()
#         self.setLayout(self.grid)
#
#         self.verticalGroupBox = QGroupBox()
#         # self.verticalGroupBox.setGeometry(0, 0, 50, 1000)
#         layout = QHBoxLayout()
#
#         button = QPushButton("Новый словарь")
#         button.setObjectName("restart_btn")
#         button.setGeometry(QtCore.QRect(450, 700, 300, 50))
#         button.setFont(QtGui.QFont("Times", 17))
#         button.clicked.connect(self.restart)
#
#         layout.addWidget(button)
#         layout.setSpacing(10)
#
#         self.verticalGroupBox.setLayout(layout)
#         self.figure = plt.figure()
#         self.canvas = FigureCanvas(self.figure)
#         self.grid.addWidget(self.canvas, 0, 1, 9, 9)
#         self.grid.addWidget(self.verticalGroupBox, 300, 5)
#         self.table = QTableWidget(self)
#         self.grid.addWidget(self.table, 100, 1, 9, 9)
#
#         self.show()
#
#
#
#     def restart(self):
#         text, ok_pressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
#         graph, labels, prefixes, node_dict, abc = self.calculate(text)
#         self.draw_table(prefixes, node_dict, abc)
#         self.draw_scheme(graph, labels)
#
#     def draw_table(self, prefixes, node_dict, abc):
#         prefixes = list(set(prefixes))
#         prefixes.sort(key=lambda k: (len(k), k))
#         abc.sort()
#         columns_list = ["NodeValue"] + abc + ["\u03bb"]
#         self.table.setColumnCount(len(columns_list))
#         self.table.setRowCount(len(prefixes))
#         self.table.setHorizontalHeaderLabels(columns_list)
#         for i in range(self.table.rowCount()):
#             for j in range(self.table.columnCount()):
#                 if j == 0:
#                     value = prefixes[i]
#                 elif j == self.table.columnCount() - 1:
#                     value = node_dict.get(prefixes[i]).suffix_link
#                 else:
#                     value = node_dict.get(prefixes[i]).prefix_links.get(columns_list[j])
#                 if value is None:
#                     value = "\u03bb"
#                 self.table.setItem(i, j, QTableWidgetItem(value))
#         self.table.resizeColumnsToContents()
#
#     def draw_scheme(self, graph, labels):
#         print(labels)
#         # self.figure.clf()
#         # layout = graphviz_layout(graph, prog="dot")
#         # nwx.draw(graph, layout, with_labels=True)
#         # nwx.draw_networkx_edge_labels(graph, layout, edge_labels=labels)
#         # self.canvas.draw_idle()
#         pass
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())