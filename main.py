from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMainWindow
from PyQt5 import QtCore
import sys
from  initUI import Ui_MainWindow



class Bd(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.rg)
        self.ui.pushButton_3.clicked.connect(self.auth)
        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]

    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit == 0):
                    return
            funct(self)
        return wrapper

    @check_input
    def rg(self):
        name = self.ui.lineEdit.text()
        password = self.ui.lineEdit_3.text()

    @check_input
    def auth(self):
        name = self.ui.lineEdit.text()
        password = self.ui.lineEdit_3.text()
