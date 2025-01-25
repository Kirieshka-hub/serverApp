import socket
import threading
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from initUI import Ui_MainWindow

class MessageHandler(QObject):
    show_warning_signal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.show_warning_signal.connect(self.show_warning)

    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self.parent, title, message)


class EmojiDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Emoji choose")
        self.setGeometry(500, 500, 300, 300)

        emojis = [
            "😂", "❤️", "🤣", "😍", "😭", "😊", "👍", "😒", "🙏", "😘",
            "🥰", "🥲", "😎", "😢", "🤔", "🤗", "😡", "🙄", "😩", "🤩",
            "🤤", "😱", "🙃", "😉", "🤪", "👏", "💔", "🔥", "🥳", "😅",
            "😤", "💀", "🎉", "🫶", "💪", "👀", "👌", "🤞", "👋", "✌️",
            "😴", "🤷", "🤝", "⭐", "🎂", "🎈", "🎊", "🍕", "🍔", "🍩"
        ]

        layout = QtWidgets.QGridLayout()
        for i, emoji in enumerate(emojis):
            button = QtWidgets.QPushButton(emoji)
            button.setFixedSize(40, 40)
            button.clicked.connect(lambda _, e=emoji: self.send_emoji(e))
            layout.addWidget(button, i // 10, i % 10)

        self.setLayout(layout)
        self.selected_emoji = None

    def send_emoji(self, emoji):
        self.selected_emoji = emoji
        self.accept()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, server_ip='127.0.0.1', server_port=53210):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.server_ip = server_ip
        self.server_port = server_port
        self.user_name = ""

        self.message_handler = MessageHandler(parent=self)

        # Привязываем кнопки
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_3.clicked.connect(self.register)
        self.ui.pushButton_7.clicked.connect(self.clear_text_edit)
        self.ui.pushButton_6.clicked.connect(self.open_emoji_dialog)
        self.ui.pushButton_5.clicked.connect(self.send_message)

        self.ui.lineEdit_6.returnPressed.connect(self.send_message)
        self.ui.listWidget.itemClicked.connect(self.client_selected)

        self.selected_client_ip_port = None

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_sock.connect((self.server_ip, self.server_port))
            print(f"[Client] Подключились к серверу: {self.server_ip}:{self.server_port}")
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except Exception as e:
            print(f"[Client] Ошибка подключения к серверу: {e}")

    def receive_loop(self):
        while True:
            try:
                data = self.client_sock.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                if message.startswith("REGISTER_SUCCESS"):
                    self.user_name = message.split(":", 1)[1]
                    self.ui.go_to_third_page()
                    self.client_sock.sendall("GET_CLIENT_LIST".encode('utf-8'))

                elif message.startswith("REGISTER_FAIL"):
                    reason = message.split(':', 1)[1]
                    self.message_handler.show_warning_signal.emit("Registration error", reason)

                elif message.startswith("LOGIN_SUCCESS"):
                    self.user_name = message.split(":", 1)[1]
                    self.ui.go_to_third_page()
                    self.client_sock.sendall("GET_CLIENT_LIST".encode('utf-8'))

                elif message.startswith("LOGIN_FAIL"):
                    self.message_handler.show_warning_signal.emit("Enter error", "There's no such a user!")

                elif message.startswith("CLIENT_LIST:"):
                    clients_info = message.split(":", 1)[1]
                    clients = clients_info.split(",")
                    self.ui.listWidget.clear()
                    for client in clients:
                        self.ui.listWidget.addItem(client)

                elif message.startswith("CHAT_MESSAGES:"):
                    chat_messages = message.split(":", 1)[1]
                    self.ui.textEdit.append(chat_messages)
                else:
                    # Любые прочие сообщения
                    self.ui.textEdit.append(message)

            except Exception as e:
                print(f"[Client] Ошибка в receive_loop: {e}")
                break

        print("[Client] Приём данных завершён")

    def client_selected(self, item):
        self.selected_client_ip_port = item.text()
        if self.selected_client_ip_port.split(':')[0] == self.user_name:
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
        else:
            self.ui.go_to_four_page()

        try:
            chat_partner = self.selected_client_ip_port.split(':')[0]
            load_chat_request = f"LOAD_CHAT:{chat_partner}"
            self.client_sock.sendall(load_chat_request.encode('utf-8'))
        except Exception as e:
            print(f"[Client] Ошибка при загрузке чата: {e}")

    def clear_text_edit(self):
        self.save_chat()
        self.ui.textEdit.clear()
        print("[Client] Текстовое поле очищено")

    def save_chat(self):
        if self.selected_client_ip_port:
            chat_partner = self.selected_client_ip_port.split(':')[0]
            chat_messages = self.ui.textEdit.toPlainText()
            msg = f"SAVE_CHAT:{chat_partner}:{chat_messages}"
            try:
                self.client_sock.sendall(msg.encode('utf-8'))
                print("[Client] Чат сохранён.")
            except Exception as e:
                print(f"[Client] Ошибка при сохранении чата: {e}")

    def send_message(self):
        text = self.ui.lineEdit_6.text()
        if text and self.selected_client_ip_port:
            try:
                final_message = f"TO:{self.selected_client_ip_port}:{text}"
                self.client_sock.sendall(final_message.encode('utf-8'))
                self.ui.textEdit.append(f"Your: {text}")
                self.ui.lineEdit_6.clear()
            except Exception as e:
                print(f"[Client] Ошибка при отправке сообщения: {e}")

    def open_emoji_dialog(self):
        dialog = EmojiDialog(self)
        if dialog.exec_():
            selected_emoji = dialog.selected_emoji
            if selected_emoji and self.selected_client_ip_port:
                current_text = self.ui.lineEdit_6.text()
                self.ui.lineEdit_6.setText(current_text + selected_emoji)

    def login(self):
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()
        msg = f"LOGIN:{username}:{password}"
        self.client_sock.sendall(msg.encode('utf-8'))

    def register(self):
        username = self.ui.lineEdit_3.text().strip()
        password = self.ui.lineEdit_4.text().strip()
        confirm_password = self.ui.lineEdit_5.text().strip()
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, 'Error', "Passwords doesn't match!")
            return

        reg_msg = f"REGISTER:{username}:{password}"
        self.client_sock.sendall(reg_msg.encode('utf-8'))
