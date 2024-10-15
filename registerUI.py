from chatUI import Ui_MainWindowChat
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setStyleSheet("background-color: #fff;\n"
"    border-radius: 30px;\n"
"    box-shadow: 0px 10px 30px 5px rgba(0, 0, 0, 0.5);\n"
"  ")
        self.page.setObjectName("page")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.page)
        self.widget_2.setObjectName("widget_2")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(220, 190, 171, 71))
        self.label.setStyleSheet("font-family:sans-serif;\n"
"font-size:42px;\n"
"font-weight:500;\n"
"")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit.setGeometry(QtCore.QRect(130, 300, 370, 70))
        self.lineEdit.setStyleSheet("background-color: #eee;\n"
"    border: none;\n"
"    margin: 8px 0;\n"
"    padding: 10px 15px;\n"
"    font-size: 24px;\n"
"    border-radius: 8px;\n"
"    width: 100%;\n"
"    outline: none;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 390, 370, 70))
        self.lineEdit_2.setStyleSheet("background-color: #eee;\n"
"    border: none;\n"
"    margin: 8px 0;\n"
"    padding: 10px 15px;\n"
"    font-size: 24px;\n"
"    border-radius: 8px;\n"
"    width: 100%;\n"
"    outline: none;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(210, 530, 211, 81))
        self.pushButton.setStyleSheet("QPushButton{\n"
"    background-color: #512da8;\n"
" color: #fff;\n"
"font-size: 24px;\n"
"padding: 10px 45px;\n"
"border: 1px solid transparent;\n"
"border-radius: 8px;\n"
" font-weight: 600;\n"
"letter-spacing: 0.5px;\n"
" text-transform: uppercase;\n"
"margin-top: 10px;\n"
"cursor: pointer;\n"
"transition: background-color 0.5s ease;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(81, 45, 168, 0.8);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.widget_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(self.page)
        self.widget.setStyleSheet("background-color:rgb(86, 78, 182);\n"
"border: 1px soldi rgb(86, 78, 182);\n"
"border-top-left-radius: 180px;\n"
"border-bottom-left-radius:180px;")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(200, 270, 251, 71))
        self.label_2.setStyleSheet("font-size:42px;\n"
"color:white;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(70, 360, 511, 31))
        self.label_3.setStyleSheet("font-size:18px;\n"
"color:white;\n"
"")
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 430, 211, 81))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"\n"
" color: #fff;\n"
"    font-size: 24px;\n"
"    padding: 10px 45px;\n"
"    border: 1px solid transparent;\n"
"    border-radius: 8px;\n"
"    font-weight: 600;\n"
"    letter-spacing: 0.5px;\n"
"    text-transform: uppercase;\n"
"    margin-top: 10px;\n"
"    cursor: pointer;\n"
"    background-color: transparent;\n"
"    border-color: #fff;\n"
"    transition: background-color 0.5s ease;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(255, 255, 255, 0.8);\n"
"\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.widget)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setStyleSheet("background-color: #fff;\n"
"    border-radius: 30px;\n"
"    box-shadow: 0px 10px 30px 5px rgba(0, 0, 0, 0.5);\n"
"  ")
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_3 = QtWidgets.QWidget(self.page_2)
        self.widget_3.setStyleSheet("background-color:rgb(86, 78, 182);\n"
"border: 1px soldi rgb(86, 78, 182);\n"
"border-top-right-radius: 180px;\n"
"border-bottom-right-radius:180px;")
        self.widget_3.setObjectName("widget_3")
        self.label_4 = QtWidgets.QLabel(self.widget_3)
        self.label_4.setGeometry(QtCore.QRect(130, 300, 301, 41))
        self.label_4.setStyleSheet("font-size:42px;\n"
"color:white;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget_3)
        self.label_5.setGeometry(QtCore.QRect(30, 380, 511, 21))
        self.label_5.setStyleSheet("font-size:18px;\n"
"color:white;\n"
"")
        self.label_5.setObjectName("label_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 440, 201, 71))
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"\n"
" color: #fff;\n"
"    font-size: 24px;\n"
"    padding: 10px 45px;\n"
"    border: 1px solid transparent;\n"
"    border-radius: 8px;\n"
"    font-weight: 600;\n"
"    letter-spacing: 0.5px;\n"
"    text-transform: uppercase;\n"
"    margin-top: 10px;\n"
"    cursor: pointer;\n"
"    background-color: transparent;\n"
"    border-color: #fff;\n"
"    transition: background-color 0.5s ease;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(255, 255, 255, 0.8);\n"
"\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.widget_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_4 = QtWidgets.QWidget(self.page_2)
        self.widget_4.setObjectName("widget_4")
        self.label_6 = QtWidgets.QLabel(self.widget_4)
        self.label_6.setGeometry(QtCore.QRect(100, 160, 441, 61))
        self.label_6.setStyleSheet("font-family:sans-serif;\n"
"font-size:42px;\n"
"font-weight:500;\n"
"")
        self.label_6.setObjectName("label_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 260, 370, 70))
        self.lineEdit_3.setStyleSheet("background-color: #eee;\n"
"    border: none;\n"
"    margin: 8px 0;\n"
"    padding: 10px 15px;\n"
"    font-size: 24px;\n"
"    border-radius: 8px;\n"
"    width: 100%;\n"
"    outline: none;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 440, 370, 70))
        self.lineEdit_4.setStyleSheet("background-color: #eee;\n"
"    border: none;\n"
"    margin: 8px 0;\n"
"    padding: 10px 15px;\n"
"    font-size: 24px;\n"
"    border-radius: 8px;\n"
"    width: 100%;\n"
"    outline: none;")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_5.setGeometry(QtCore.QRect(140, 350, 370, 70))
        self.lineEdit_5.setStyleSheet("background-color: #eee;\n"
"    border: none;\n"
"    margin: 8px 0;\n"
"    padding: 10px 15px;\n"
"    font-size: 24px;\n"
"    border-radius: 8px;\n"
"    width: 100%;\n"
"    outline: none;")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 630, 201, 71))
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"    background-color: #512da8;\n"
" color: #fff;\n"
"font-size: 24px;\n"
"padding: 10px 45px;\n"
"border: 1px solid transparent;\n"
"border-radius: 8px;\n"
" font-weight: 600;\n"
"letter-spacing: 0.5px;\n"
" text-transform: uppercase;\n"
"margin-top: 10px;\n"
"cursor: pointer;\n"
"transition: background-color 0.5s ease;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(81, 45, 168, 0.8);\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_5.addWidget(self.widget_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_2.clicked.connect(self.go_to_second_page)
        self.pushButton_4.clicked.connect(self.go_to_first_page)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Sign in"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "User name"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "password"))
        self.pushButton.setText(_translate("MainWindow", "sign in"))
        self.label_2.setText(_translate("MainWindow", "Hello Friend!"))
        self.label_3.setText(_translate("MainWindow", "Register with your personal details to use all of site feautures"))
        self.pushButton_2.setText(_translate("MainWindow", "Sign up"))
        self.label_4.setText(_translate("MainWindow", "Welcome Back!"))
        self.label_5.setText(_translate("MainWindow", "Register with your personal details to use all of site feautures"))
        self.pushButton_4.setText(_translate("MainWindow", "Sign in"))
        self.label_6.setText(_translate("MainWindow", "Create a new Account"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "User name"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "password"))
        self.lineEdit_5.setPlaceholderText(_translate("MainWindow", "password"))
        self.pushButton_3.setText(_translate("MainWindow", "Sign up"))

    def go_to_second_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_first_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_third_page(self):
        self.stackedWidget.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())