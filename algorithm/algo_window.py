from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from main import calculate


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


    def get_text(self):
        text, okPressed = QInputDialog.getText(self, "Ввести словарь", "Словарь:", QLineEdit.Normal, "")
        if okPressed and text != '':
            calculate(text)


    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.restart_btn.setText(_translate("Preparing", "Другой словарь"))


    def restart(self):
        print('a')
        self.get_text()
