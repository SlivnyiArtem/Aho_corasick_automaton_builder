# import sys
#
# import PyQt5
#
# # from PyQt5 import QtWidgets, QtCore
# from garbage_code.old_process import AhoKorasicProcessWindow
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
