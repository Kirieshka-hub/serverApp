import sys
from  PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setStyleSheet("background-color: #fff;\n"
"   border-radius: 30px;\n"
"    box-shadow: 0px 10px 30px 5px rgba(0, 0, 0, 0.5);")
        self.page_1.setObjectName("page_1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(self.page_1)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(200, 150, 181, 61))
        self.label_3.setStyleSheet("font-size:52px;")
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 280, 401, 81))
        self.lineEdit.setStyleSheet("background-color: #eee;\n"
"border: none;\n"
"    margin: 8px 0;\n"
"    padding: 10px 15px;\n"
"    font-size: 24px;\n"
"    border-radius: 8px;\n"
"    width: 100%;\n"
"    outline: none;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 380, 401, 81))
        self.lineEdit_2.setStyleSheet("background-color: #eee;\n"
"border: none;\n"
"    margin: 8px 0;\n"
"    padding: 10px 15px;\n"
"    font-size: 24px;\n"
"    border-radius: 8px;\n"
"    width: 100%;\n"
"    outline: none;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(180, 560, 201, 71))
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
"QPushButton:hover {\n"
"    background-color: rgba(81, 45, 168, 0.8);\n"
"}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.widget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_2 = QtWidgets.QWidget(self.page_1)
        self.widget_2.setStyleSheet("background-color:rgb(86, 78, 182);\n"
"border: 1px solid rgb(86, 78, 182) ; \n"
"border-top-left-radius:180px;\n"
"border-bottom-left-radius:180px;")
        self.widget_2.setObjectName("widget_2")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(160, 240, 311, 51))
        self.label.setStyleSheet("font-size:52px;\n"
"color:white;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(70, 310, 541, 41))
        self.label_2.setStyleSheet("font-size:18px;\n"
                                   "color:white;")
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 370, 201, 71))
        self.pushButton_2.setStyleSheet(
            "QPushButton { color: #fff; font-size: 24px; padding: 10px 45px; border: 1px solid transparent; border-radius: 8px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 10px; cursor: pointer; background-color: transparent; border-color: #fff; transition: background-color 0.5s ease; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.8); }")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.widget_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.stackedWidget.addWidget(self.page_1)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setStyleSheet("background-color: #fff;\n"
                                  "   border-radius: 30px;\n"
                                  "    box-shadow: 0px 10px 30px 5px rgba(0, 0, 0, 0.5);")
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_3 = QtWidgets.QWidget(self.page_3)
        self.widget_3.setStyleSheet("background-color:rgb(86, 78, 182);\n"
                                    "border: 1px solid rgb(86, 78, 182) ; \n"
                                    "border-top-right-radius:180px;\n"
                                    "border-bottom-right-radius:180px;")
        self.widget_3.setObjectName("widget_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_4.setGeometry(QtCore.QRect(170, 410, 200, 71))
        self.pushButton_4.setStyleSheet(
            "QPushButton { color: #fff; font-size: 24px; padding: 10px 45px; border: 1px solid transparent; border-radius: 8px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 10px; cursor: pointer; background-color: transparent; border-color: #fff; transition: background-color 0.5s ease; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.8); }")
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_5 = QtWidgets.QLabel(self.widget_3)
        self.label_5.setGeometry(QtCore.QRect(80, 260, 391, 81))
        self.label_5.setStyleSheet("font-size:52px;\n"
                                   "color:white;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.widget_3)
        self.label_6.setGeometry(QtCore.QRect(30, 350, 511, 41))
        self.label_6.setStyleSheet("color:white;\n"
                                   "font-size:18px;")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.widget_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_4 = QtWidgets.QWidget(self.page_3)
        self.widget_4.setObjectName("widget_4")
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setGeometry(QtCore.QRect(50, 110, 511, 81))
        self.label_4.setStyleSheet("font-size:52px;\n"
                                   "")
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 240, 371, 81))
        self.lineEdit_3.setStyleSheet("background-color: #eee;\n"
                                      "border: none;\n"
                                      "    margin: 8px 0;\n"
                                      "    padding: 10px 15px;\n"
                                      "    font-size: 24px;\n"
                                      "    border-radius: 8px;\n"
                                      "    width: 100%;\n"
                                      "    outline: none;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_4.setGeometry(QtCore.QRect(130, 340, 371, 81))
        self.lineEdit_4.setStyleSheet("background-color: #eee;\n"
                                      "border: none;\n"
                                      "    margin: 8px 0;\n"
                                      "    padding: 10px 15px;\n"
                                      "    font-size: 24px;\n"
                                      "    border-radius: 8px;\n"
                                      "    width: 100%;\n"
                                      "    outline: none;")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_5.setGeometry(QtCore.QRect(130, 440, 371, 81))
        self.lineEdit_5.setStyleSheet("background-color: #eee;\n"
                                      "border: none;\n"
                                      "    margin: 8px 0;\n"
                                      "    padding: 10px 15px;\n"
                                      "    font-size: 24px;\n"
                                      "    border-radius: 8px;\n"
                                      "    width: 100%;\n"
                                      "    outline: none;")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 620, 201, 71))
        self.pushButton_3.setStyleSheet("QPushButton {\n"
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
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(81, 45, 168, 0.8);\n"
                                        "}\n"
                                        "")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_6.addWidget(self.widget_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setStyleSheet("background-color: #fff;\n"
                                  "   border-radius: 30px;\n"
                                  "    box-shadow: 0px 10px 30px 5px rgba(0, 0, 0, 0.5);")
        self.page_4.setObjectName("page_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_5 = QtWidgets.QWidget(self.page_4)
        self.widget_5.setStyleSheet("background-color:rgb(86, 78, 182);\n"
                                    "border: 1px solid rgb(86, 78, 182) ; \n"
                                    "border-top-right-radius:180px;\n"
                                    "border-bottom-right-radius:180px;")
        self.widget_5.setObjectName("widget_5")
        self.label_7 = QtWidgets.QLabel(self.widget_5)
        self.label_7.setGeometry(QtCore.QRect(20, 330, 601, 111))
        self.label_7.setStyleSheet("font-size:38px;\n"
                                   "color:white;")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.widget_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_6 = QtWidgets.QWidget(self.page_4)
        self.widget_6.setObjectName("widget_6")
        self.listWidget = QtWidgets.QListWidget(self.widget_6)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 560, 740))
        self.listWidget.setStyleSheet(
            "QListWidget { border: 1px solid #512da8;  background-color: rgba(255, 255, 255, 0.5);  } QListWidget::item { height: 40px; margin:20px; /* Высота каждого элемента */ padding: 10px; /* Отступы внутри элемента */ } QListWidget::item:selected { background-color: none; /* Цвет фона выбранного элемента */ color: white; /* Цвет текста выбранного элемента */ } QListWidget QScrollBar { background: lightblue; /* Цвет фона полосы прокрутки */ }\n"
            "")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_8.addWidget(self.widget_6)
        self.horizontalLayout_4.addLayout(self.verticalLayout_8)
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.textEdit = QtWidgets.QTextEdit(self.page_5)
        self.textEdit.setReadOnly(True)
        self.textEdit.setGeometry(QtCore.QRect(-7, 0, 1201, 601))
        self.textEdit.setStyleSheet(
            "QTextEdit { background-color: rgba(255, 255, 255, .1); /* Цвет фона */ backdrop-filter: blur(10px); color: black; /* Цвет текста */ font-size: 24px; /* Размер шрифта */ padding: 10px; /* Отступы внутри редактора */ border: 1px solid #ccc; /* Граница */ border-radius: 5px; /* Скругление углов */ } QTextEdit:focus { border: 1px solid #512da8; /* Цвет границы при фокусе */ } QTextEdit QScrollBar { background: #e0e0e0; /* Цвет фона полосы прокрутки */ width: 10px; /* Ширина полосы прокрутки */ } QTextEdit QScrollBar::handle { background: #512da8; /* Цвет ручки полосы прокрутки */ border-radius: 5px; /* Скругление углов ручки */ } QTextEdit QScrollBar::handle:hover { background: #7b1fa2; /* Цвет ручки при наведении */ } QTextEdit QScrollBar::add-line, QTextEdit QScrollBar::sub-line { background: none; /* Убираем фон для кнопок прокрутки */ }\n"
            "")
        self.textEdit.setObjectName("textEdit")
        self.widget_7 = QtWidgets.QWidget(self.page_5)
        self.widget_7.setGeometry(QtCore.QRect(-10, 590, 1201, 191))
        self.widget_7.setStyleSheet("")
        self.widget_7.setObjectName("widget_7")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget_7)
        self.lineEdit_6.setGeometry(QtCore.QRect(220, 50, 581, 81))
        self.lineEdit_6.setStyleSheet("background-color: #eee;\n"
                                      "border: none;\n"
                                      "    margin: 8px 0;\n"
                                      "    padding: 10px 15px;\n"
                                      "    font-size: 24px;\n"
                                      "    border-radius: 8px;\n"
                                      "    width: 100%;\n"
                                      "    border:1px solid #512da8;\n"
                                      "    outline: none;")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_7)
        self.pushButton_5.setGeometry(QtCore.QRect(1020, 50, 161, 71))
        self.pushButton_5.setStyleSheet("QPushButton {\n"
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
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(81, 45, 168, 0.8);\n"
                                        "}\n"
                                        "\n"
                                        "")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.widget_7)
        self.pushButton_6.setGeometry(QtCore.QRect(850, 50, 151, 71))
        self.pushButton_6.setStyleSheet("QPushButton {\n"
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
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(81, 45, 168, 0.8);\n"
                                        "}\n"
                                        "")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.widget_7)
        self.pushButton_7.setGeometry(QtCore.QRect(30, 50, 171, 71))
        self.pushButton_7.setStyleSheet("QPushButton {\n"
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
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(81, 45, 168, 0.8);\n"
                                        "}\n"
                                        "\n"
                                        "")
        self.pushButton_7.setObjectName("pushButton_7")
        self.stackedWidget.addWidget(self.page_5)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton_2.clicked.connect(self.go_to_second_page)
        self.pushButton_4.clicked.connect(self.go_to_first_page)
        # self.pushButton.clicked.connect(self.go_to_third_page)
        # self.pushButton_3.clicked.connect(self.go_to_third_page)
        self.pushButton_7.clicked.connect(self.go_to_third_page)

        # self.listWidget.addItem("first")
        # self.listWidget.itemClicked.connect(self.go_to_four_page)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Messenger"))
        MainWindow.setWindowIcon(QtGui.QIcon("img/chat_bubble_conversation_contact_icon_264230.ico"))
        self.label_3.setText(_translate("MainWindow", "Sign in"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "user name"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "password"))
        self.pushButton.setText(_translate("MainWindow", "Sign in"))
        self.label.setText(_translate("MainWindow", "Hello Friend!"))
        self.label_2.setText(
            _translate("MainWindow", "Register with your personal details to use all of site feautures"))
        self.pushButton_2.setText(_translate("MainWindow", "Sign up"))
        self.pushButton_4.setText(_translate("MainWindow", "Sign in"))
        self.label_5.setText(_translate("MainWindow", "Welcome Back!"))
        self.label_6.setText(
            _translate("MainWindow", "Register with your personal details to use all of site feautures"))
        self.label_4.setText(_translate("MainWindow", "Create a new Account"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "user name"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "password"))
        self.lineEdit_5.setPlaceholderText(_translate("MainWindow", "password"))
        self.pushButton_3.setText(_translate("MainWindow", "Sign up"))
        self.label_7.setText(_translate("MainWindow", "Click to write a message"))
        self.lineEdit_6.setPlaceholderText(_translate("MainWindow", "Input message"))
        self.pushButton_5.setText(_translate("MainWindow", "Send"))
        self.pushButton_6.setText(_translate("MainWindow", "-_-"))
        self.pushButton_7.setText(_translate("MainWindow", "Back"))

    def go_to_second_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def go_to_first_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()

    def go_to_third_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def go_to_four_page(self):
        self.stackedWidget.setCurrentIndex(3)


    def styled_message(self, message):
        styled_message = f"""
                        <div style="background-color: lightblue; border-radius: 10px; padding: 10px; margin: 5px 0;">
                            <span style="font-family: Arial, sans-serif; font-size: 14px; color: black;">
                                Вы (клиенту {self.selected_client_ip_port}): {message}
                            </span>
                        </div>
                        """
        return styled_message
    def display_message(self, message):
        styled_message = self.styled_message(message)
        self.textEdit.append(styled_message)  # Добавление сообщения в QTextEdit



if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())