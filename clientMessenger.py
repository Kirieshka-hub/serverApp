import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel
from PyQt5 import QtCore, QtWidgets
import sys
from initUI import Ui_MainWindow


class AwaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ожидание подключения')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(1400, 850, 300, 100)
        self.label = QLabel("Ожидание подключения клиента...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow(QMainWindow):
    def __init__(self, awaiting_window):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_3.clicked.connect(self.register)

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.awaiting_window = awaiting_window

        self.ui.pushButton_5.clicked.connect(self.send_message)

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
                        error_msg = message.split(":", 1)[1] if ":" in message else "Registration failed"
                        QtWidgets.QMessageBox.warning(self, 'Ошибка', error_msg)
                    elif message.startswith("LOGIN_SUCCESS"):
                        self.ui.go_to_third_page()
                        self.client_sock.sendall("GET_CLIENT_LIST".encode('utf-8'))
                    elif message.startswith("LOGIN_FAIL"):
                        error_msg = message.split(":", 1)[1] if ":" in message else "Login failed"
                        QtWidgets.QMessageBox.warning(self, 'Ошибка', error_msg)
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

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        login_message = f"LOGIN:{username}:{password}"
        try:
            self.client_sock.sendall(login_message.encode('utf-8'))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', f'Не удалось отправить данные для входа: {e}')
            return

    def register(self):
        username = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()
        confirm_password = self.ui.lineEdit_5.text()

        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают.')
            return

        registration_message = f"REGISTER:{username}:{password}"
        try:
            self.client_sock.sendall(registration_message.encode('utf-8'))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', f'Не удалось отправить данные регистрации: {e}')
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    client_window = MainWindow(awaiting_window)
    client_window.connect_to_server()

    sys.exit(app.exec_())
