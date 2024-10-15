import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel
from PyQt5 import QtCore
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

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Ссылка на ожидающее окно
        self.awaiting_window = awaiting_window

        # Подключаем кнопку отправки сообщения
        self.ui.pushButton_5.clicked.connect(self.send_message)

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



            # self.client_sock.sendall(msg.encode('utf-8'))

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
                    count = 0
                    # Проверяем, является ли полученное сообщение списком клиентов
                    if message.startswith("Подключенные клиенты:"):
                        # Очищаем QListWidget перед добавлением новых клиентов
                        self.ui.listWidget.clear()
                        # Извлекаем информацию об адресах и добавляем их в QListWidget
                        clients_info = message.split(":")[1].strip()
                        clients = clients_info.split(",")
                        self.ui.listWidget.addItem(clients[count] + clients[count+1])
                        count += 2

                    else:
                        self.ui.textEdit.append(f'Сервер: {message}')  # Добавляем сообщение от сервера в текстовое поле
            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                break

    def send_message(self):
        message = self.ui.lineEdit_6.text()
        if message:
            try:
                self.client_sock.sendall(message.encode('utf-8'))
                self.ui.textEdit.append(f"Вы: {message}")
                self.ui.lineEdit_6.clear()
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    client_window = MainWindow(awaiting_window)
    client_window.connect_to_server()

    sys.exit(app.exec_())
