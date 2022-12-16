import sys
from PyQt5 import QtWidgets, QtCore
from process import AhoKorasicProcessWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ахо-Корасик")
        self.setFixedSize(1200, 800)

        self.central_widget = QtWidgets.QWidget(self)
        self.stacked_widget = QtWidgets.QStackedWidget(self.central_widget)
        self.stacked_widget.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.setCentralWidget(self.central_widget)
        self.stacked_widget.addWidget(AhoKorasicProcessWindow(self))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = AhoKorasicProcessWindow()
    w.show()
    sys.exit(app.exec_())
