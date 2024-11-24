import socket
import threading
# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.QtCore import pyqtSignal, QObject
from initUI import Ui_MainWindow

class MessageHandler(QObject):
    show_warning_signal = pyqtSignal(str, str)  # Сигнал для показа предупреждений

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.show_warning_signal.connect(self.show_warning)  # Связываем сигнал с методом

    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self.parent, title, message)  # Показываем предупреждение

class EmojiDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор смайлика")
        self.setGeometry(500, 500, 300, 300)

        # Список доступных смайликов
        emojis = [
            "😊", "😂", "😍", "😎", "😢", "😡", "😱", "🥳", "🤔", "🤗",
            "🙄", "😴", "😷", "🤒", "🤕", "🙃", "😉", "😋", "🤪", "🤩",
            "👍", "👎", "👏", "🙏", "👌", "🤘", "✌️", "👋", "🤝", "💪",
            "❤️", "💔", "💙", "💜", "💥", "💫", "🔥", "⭐️", "🌙", "☀️",
            "🎉", "🎊", "🎁", "🎈", "🎂", "🍕", "🍔", "🍟", "🍩", "🍪"
        ]

        layout = QtWidgets.QGridLayout()  # Используем сетку для удобного размещения смайликов

        # Создаем кнопки для каждого смайлика
        for i, emoji in enumerate(emojis):
            button = QtWidgets.QPushButton(emoji)
            button.setFixedSize(40, 40)
            button.clicked.connect(lambda _, e=emoji: self.send_emoji(e))
            layout.addWidget(button, i // 10, i % 10)

        self.setLayout(layout)
        self.selected_emoji = None

    def send_emoji(self, emoji):
        # Выбираем смайлик и закрываем диалог
        self.selected_emoji = emoji
        self.accept()


class AwaitingWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ожидание подключения')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(1400, 850, 300, 100)
        self.label = QtWidgets.QLabel("Ожидание подключения клиента...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, awaiting_window):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.message_handler = MessageHandler(parent=self)




        # Подключаем кнопку для логина и регистрации
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_3.clicked.connect(self.register)

        # Подключаем кнопку "Назад" для очистки текстового поля
        self.ui.pushButton_7.clicked.connect(self.clear_text_edit)

        # Подключаем кнопку для выбора смайликов
        self.ui.pushButton_6.clicked.connect(self.open_emoji_dialog)

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.awaiting_window = awaiting_window

        # Подключаем кнопку для отправки сообщений
        self.ui.pushButton_5.clicked.connect(self.send_message)

        # Подключаем список для выбора клиента
        self.ui.listWidget.itemClicked.connect(self.client_selected)

        self.selected_client_ip_port = None

    def connect_to_server(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_sock.bind(('', 37021))

        print('Looking for the server...')

        data, addr = udp_sock.recvfrom(1024)
        message = data.decode('utf-8')
        if message.startswith('SERVER_IP:'):
            server_ip = message.split(':')[1]
            print(f'Server IP found: {server_ip}')

            try:
                self.client_sock.connect((server_ip, 53210))
                print('Connected to server')

                self.awaiting_window.close()
                self.show()

                threading.Thread(target=self.receive_moves, daemon=True).start()

            except Exception as e:
                print(f"Failed to connect: {e}")


    def receive_moves(self):
        while True:
            try:
                message = self.client_sock.recv(1024).decode('utf-8')
                if message:
                    if message.startswith("REGISTER_SUCCESS"):
                        self.ui.go_to_third_page()
                        self.client_sock.sendall("GET_CLIENT_LIST".encode('utf-8'))
                    elif message.startswith("REGISTER_FAIL"):
                        self.message_handler.show_warning_signal.emit("Ошибка", "Такой пользователь уже существует!")
                    elif message.startswith("LOGIN_SUCCESS"):
                        self.ui.go_to_third_page()
                        self.client_sock.sendall("GET_CLIENT_LIST".encode('utf-8'))
                    elif message.startswith("LOGIN_FAIL"):
                        self.message_handler.show_warning_signal.emit("Ошибка", "Такого пользователя нет!")
                    elif message.startswith("CLIENT_LIST:"):
                        clients_info = message.split(":", 1)[1]
                        clients = clients_info.split(",")
                        self.ui.listWidget.clear()
                        for client in clients:
                            self.ui.listWidget.addItem(client)
                    else:
                        self.ui.textEdit.append(f'{message}')
            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                break

    def client_selected(self, item):
        self.selected_client_ip_port = item.text()
        print(f"Выбран клиент: {self.selected_client_ip_port}")

    def send_message(self):
        message = self.ui.lineEdit_6.text()
        if message and self.selected_client_ip_port:
            try:
                final_message = f"TO:{self.selected_client_ip_port}:{message}"
                self.client_sock.sendall(final_message.encode('utf-8'))
                self.ui.textEdit.append(f"Вы (клиенту {self.selected_client_ip_port}): {message}")
                self.ui.lineEdit_6.clear()
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

    def open_emoji_dialog(self):
        # Открываем диалоговое окно выбора смайликов
        dialog = EmojiDialog(self)
        if dialog.exec_():
            selected_emoji = dialog.selected_emoji
            if selected_emoji and self.selected_client_ip_port:
                try:
                    final_message = f"TO:{self.selected_client_ip_port}:{selected_emoji}"
                    self.client_sock.sendall(final_message.encode('utf-8'))
                    self.ui.textEdit.append(f"Вы (клиенту {self.selected_client_ip_port}): {selected_emoji}")
                except Exception as e:
                    print(f"Ошибка при отправке смайлика: {e}")

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        login_message = f"LOGIN:{username}:{password}"

        self.client_sock.sendall(login_message.encode('utf-8'))


    def register(self):
        username = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()
        confirm_password = self.ui.lineEdit_5.text()

        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают!')
            return

        registration_message = f"REGISTER:{username}:{password}"

        self.client_sock.sendall(registration_message.encode('utf-8'))


    def clear_text_edit(self):
        self.ui.textEdit.clear()
        print("Текстовое поле очищено")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    client_window = MainWindow(awaiting_window)
    client_window.connect_to_server()

    sys.exit(app.exec_())
#