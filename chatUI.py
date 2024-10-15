
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


class Ui_MainWindowChat(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.page)
        self.widget.setStyleSheet("background-color:rgb(87, 89, 186);\n"
"border:1px solid rgb(87, 89, 186);\n"
"border-bottom-right-radius: 180px;\n"
"border-top-right-radius: 180px;"

)
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(100, 330, 361, 51))
        self.label_2.setStyleSheet("font-size:52px;\n"
"color:white;")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(140, 400, 281, 31))
        self.label.setStyleSheet("font-size:24px;\n"
"color:white;")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_3 = QtWidgets.QWidget(self.page)
        self.widget_3.setStyleSheet("")


        self.widget_3.setObjectName("widget_3")
        self.listWidget = QtWidgets.QListWidget(self.widget_3)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 581, 771))
        self.listWidget.setStyleSheet("QListWidget {\n"
"                border:none ;\n"
"                background-color: rgba(255, 255, 255, 0.5);\n"
"             backdrop-filter:blur(20px);\n"
"            }\n"
"            QListWidget::item {\n"
"                height: 40px; /* Высота каждого элемента */\n"
"                padding: 10px; /* Отступы внутри элемента */\n"
"            }\n"
"            QListWidget::item:selected {\n"
"                background-color: blue; /* Цвет фона выбранного элемента */\n"
"                color: white; /* Цвет текста выбранного элемента */\n"
"            }\n"
"            QListWidget QScrollBar {\n"
"                background: lightblue; /* Цвет фона полосы прокрутки */\n"
"            }")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_6.addWidget(self.widget_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_2 = QtWidgets.QWidget(self.page_2)
        self.widget_2.setStyleSheet("")
        self.widget_2.setObjectName("widget_2")
        self.textEdit = QtWidgets.QTextEdit(self.widget_2)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.textEdit.setStyleSheet("\n"
"    QTextEdit {\n"
"        background-color: rgba(255, 255, 255, .1); /* Цвет фона */\n"
"        backdrop-filter: blur(10px);"   
"        color: black; /* Цвет текста */\n"
"        font-size: 24px; /* Размер шрифта */\n"
"        padding: 10px; /* Отступы внутри редактора */\n"
"        border: 1px solid #ccc; /* Граница */\n"
"        border-radius: 5px; /* Скругление углов */\n"
"    }\n"
"    \n"
"    QTextEdit:focus {\n"
"        border: 1px solid #512da8; /* Цвет границы при фокусе */\n"
"    }\n"
"    \n"
"    QTextEdit QScrollBar {\n"
"        background: #e0e0e0; /* Цвет фона полосы прокрутки */\n"
"        width: 10px; /* Ширина полосы прокрутки */\n"
"    }\n"
"\n"
"    QTextEdit QScrollBar::handle {\n"
"        background: #512da8; /* Цвет ручки полосы прокрутки */\n"
"        border-radius: 5px; /* Скругление углов ручки */\n"
"    }\n"
"\n"
"    QTextEdit QScrollBar::handle:hover {\n"
"        background: #7b1fa2; /* Цвет ручки при наведении */\n"
"    }\n"
"\n"
"    QTextEdit QScrollBar::add-line, \n"
"    QTextEdit QScrollBar::sub-line {\n"
"        background: none; /* Убираем фон для кнопок прокрутки */\n"
"    }\n"
"")
        self.textEdit.setObjectName("textEdit")
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setGeometry(QtCore.QRect(0, 620, 1176, 171))
        self.widget_4.setObjectName("widget_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit.setGeometry(QtCore.QRect(220, 30, 641, 71))
        self.lineEdit.setStyleSheet("border: none;\n"
"margin: 8px 0;\n"
"padding: 10px 15px;\n"
"font-size: 24px;\n"
"border-radius: 8px;\n"
"width: 100%;\n"
"outline: none;")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.widget_4)
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 171, 61))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: #512da8;\n"
"    color: #fff;\n"
"    font-size: 24px;\n"
"    padding: 10px 45px;\n"
"    border: 1px solid transparent;\n"
"    border-radius: 8px;\n"
"    font-weight: 600;\n"
"    letter-spacing: 0.5px;\n"
"    text-transform: uppercase;\n"
"    margin-top: 10px;\n"
"    cursor: pointer;\n"
"    transition: background-color 0.5s ease;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(81, 45, 168, 0.8);\n"
"}QPushButton {\n"
"    background-color: #512da8;\n"
"    color: #fff;\n"
"    font-size: 24px;\n"
"    padding: 10px 45px;\n"
"    border: 1px solid transparent;\n"
"    border-radius: 8px;\n"
"    font-weight: 600;\n"
"    letter-spacing: 0.5px;\n"
"    text-transform: uppercase;\n"
"    margin-top: 10px;\n"
"    cursor: pointer;\n"
"    transition: background-color 0.5s ease;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(81, 45, 168, 0.8);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_2.setGeometry(QtCore.QRect(1030, 30, 111, 61))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"    background-color: #512da8;\n"
"    color: #fff;\n"
"    font-size: 24px;\n"
"    padding: 10px 20px;\n"
"    border: 1px solid transparent;\n"
"    border-radius: 8px;\n"
"    font-weight: 600;\n"
"    letter-spacing: 0.5px;\n"
"    text-transform: uppercase;\n"
"    margin-top: 10px;\n"
"    cursor: pointer;\n"
"    transition: background-color 0.5s ease;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(81, 45, 168, 0.8);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_3.setGeometry(QtCore.QRect(890, 30, 111, 61))
        self.pushButton_3.setStyleSheet("QPushButton {\n"
"    background-color: #512da8;\n"
"    color: #fff;\n"
"    font-size: 24px;\n"
"    padding: 10px 20px;\n"
"    border: 1px solid transparent;\n"
"    border-radius: 8px;\n"
"    font-weight: 600;\n"
"    letter-spacing: 0.5px;\n"
"    text-transform: uppercase;\n"
"    margin-top: 10px;\n"
"    cursor: pointer;\n"
"    transition: background-color 0.5s ease;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(81, 45, 168, 0.8);\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_8.addWidget(self.widget_2)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.go_to_first_page)

        self.listWidget.addItem("first")
        self.listWidget.itemClicked.connect(self.go_to_second_page)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Select contact"))
        self.label.setText(_translate("MainWindow", "And double click to write "))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "input message"))
        self.pushButton.setText(_translate("MainWindow", "Back"))
        self.pushButton_2.setText(_translate("MainWindow", "Send"))
        self.pushButton_3.setText(_translate("MainWindow", "^-^"))


    def go_to_second_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_first_page(self):
        self.stackedWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindowChat()
    ui.setupUi(MainWindow)
    MainWindow.show()  # Исправлено здесь
    sys.exit(app.exec_())