import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import sys
from initUI import ChatApp


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
        self.ui = ChatApp()
        self.setWindowTitle('Messenger')
        self.setGeometry(1000, 600, 800, 600)

        self.ui = ChatApp()
        self.setCentralWidget(self.ui)

        self.ui.input_field.setReadOnly(True)

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Reference to awaiting window
        self.awaiting_window = awaiting_window


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
                self.ui.input_field.setReadOnly(False)

                self.awaiting_window.close()

                threading.Thread(target=self.receive_moves, daemon=True).start()

                self.ui.send_button.clicked.connect(self.send_message)


            except Exception as e:
                print(f"Failed to connect: {e}")


    def receive_moves(self):
        while True:
            try:
                message = self.client_sock.recv(1024).decode('utf-8')
                if message:
                    # print(f'Сообщение от сервера: {message}')
                    # Отображаем сообщение в текстовом поле чата
                    self.ui.text_area.append(f'Сервер: {message}')
            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                break

    def send_message(self):
        message = self.ui.input_field.text()
        if message:
            try:
                # Отправляем сообщение на сервер
                self.client_sock.sendall(message.encode('utf-8'))
                # print(f'Отправлено сообщение: {message}')
                # Отображаем сообщение в текстовом поле чата
                self.ui.text_area.append(f'Вы: {message}')
                self.ui.input_field.clear()  # Очищаем поле ввода

            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    client_window = MainWindow(awaiting_window)
    client_window.connect_to_server()
    client_window.show()

    sys.exit(app.exec_())