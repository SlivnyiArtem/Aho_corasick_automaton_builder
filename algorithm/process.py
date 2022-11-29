from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nwx

from algorithm import service_funcs, Aho_Korasic_Node, graph_constructor


class AhoKorasicProcessWindow(QWidget):
    # NumButtons = ['plot1', 'plot2', 'plot3']

    def __init__(self):

        super(AhoKorasicProcessWindow, self).__init__()
        # font = QFont()
        # font.setPointSize(16)

        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('AhoCorasik window')
        self.grid = QGridLayout()
        self.setLayout(self.grid)


        self.verticalGroupBox = QGroupBox()
        self.verticalGroupBox.setGeometry(0, 0, 100, 100)
        layout = QHBoxLayout()

        button = QPushButton("Новый словарь")
        button.setObjectName("restart_btn")
        button.setGeometry(QtCore.QRect(450, 700, 300, 50))
        button.setFont(QtGui.QFont('Times', 17))
        button.clicked.connect(self.restart)

        layout.addWidget(button)
        layout.setSpacing(10)

        self.verticalGroupBox.setLayout(layout)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)
        self.grid.addWidget(self.verticalGroupBox, 300, 5)
        self.table = QTableWidget(self)
        self.grid.addWidget(self.table, 100, 0)

        # self.buttonLayout = QHBoxLayout()
        # self.buttonLayout.addWidget(self.verticalGroupBox)

        # self.grid.addLayout(self.buttonLayout, 0, 0)


        self.show()

        '''
        self.restart_btn: QWidget = QPushButton()
        self.restart_btn.setGeometry(QtCore.QRect(450, 700, 300, 50))
        self.restart_btn.setObjectName("restart_btn")
        self.restart_btn.setFont(QtGui.QFont('Times', 17))
        self.restart_btn.clicked.connect(self.plot3)

        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.addWidget(self.verticalGroupBox)

        
        '''

    '''
    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()
        button = QPushButton("Новый словарь")
        button.setObjectName("restart_btn")
        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalGroupBox.setLayout(layout)
        button.clicked.connect(self.plot3)
        
        for i in self.NumButtons:
            button = QPushButton(i)
            button.setObjectName(i)
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)
            button.clicked.connect(self.submitCommand)
    '''

    def calculate(self, text):
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
        is_planar, _ = nwx.check_planarity(nwx.Graph(graph))
        if is_planar:
            layout = nwx.planar_layout(graph)
        else:
            layout = nwx.circular_layout(graph)
        return graph, layout, visualize_dict, prefixes, node_dict, abc, is_planar

    def restart(self):
        text, ok_pressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        graph, graph_pos, labels, prefixes, node_dict, abc, is_planar = self.calculate(text)
        self.drawTable(prefixes, node_dict, abc)
        self.drawScheme(graph, graph_pos, labels, is_planar)
        '''
        self.figure.clf()
        text, ok_pressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        graph, graph_pos, labels, prefixes, node_dict, abc, is_planar = calculate(text)
        # self.grid.update()
        # self.cnv.flush_events()

        if is_planar:
            nx.draw_planar(graph, with_labels=True)
        else:
            nx.draw_circular(graph)
        nx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=labels)

        
        B = nx.Graph()
        B.add_nodes_from([1, 2, 3, 4], bipartite=0)
        B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

        X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
        Y = set(B) - X

        X = sorted(X, reverse=True)
        Y = sorted(Y, reverse=True)

        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
        nx.draw(B, pos=pos, with_labels=True)
        self.canvas.draw_idle()
        '''

    '''
    def submitCommand(self):
        eval('self.' + str(self.sender().objectName()) + '()')

    def plot1(self):
        self.figure.clf()

    def plot2(self):
        self.figure.clf()
        self.canvas.draw_idle()
    '''
    '''
    def analyzeText(self):
        text, ok_pressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        return calculate(text)
    '''

    def drawTable(self, prefixes, node_dict, abc):
        abc.sort()
        columns_list = ["NodeValue"] + abc + ["lambda"]
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
                    value = "lambda"
                self.table.setItem(i, j, QTableWidgetItem(value))
        self.table.resizeColumnsToContents()
        self.table.resizeColumnsToContents()

    def drawScheme(self, graph, graph_pos, labels, is_planar):
        self.figure.clf()

        # self.grid.update()
        # self.cnv.flush_events()

        if is_planar:
            nwx.draw_planar(graph, with_labels=True)
        else:
            nwx.draw_circular(graph)
        nwx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=labels)

        '''
        B = nx.Graph()
        B.add_nodes_from([1, 2, 3, 4], bipartite=0)
        B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

        X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
        Y = set(B) - X

        X = sorted(X, reverse=True)
        Y = sorted(Y, reverse=True)

        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
        nx.draw(B, pos=pos, with_labels=True)
        '''
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    '''
    def restart(self):
        plt.close("all")
        self.plot3()
    '''
