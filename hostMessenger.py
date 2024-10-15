import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import QtCore
import sys


class AwaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ожидание подключения')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(800, 850, 300, 100)
        self.label = QLabel("Ожидание подключения клиента...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow:
    def __init__(self, awaiting_window):
        self.clients = []
        self.awaiting_window = awaiting_window

        # Настройка сервера
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(('', 53210))
        self.server_sock.listen(5)

        # Запускаем поток для ожидания подключения
        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        print('Сервер запущен, ожидание подключения клиента...')

        # Запускаем поток для широковещательной рассылки
        threading.Thread(target=self.broadcast_ip, daemon=True).start()

        while True:
            client_sock, client_addr = self.server_sock.accept()
            print(f'Клиент подключен от {client_addr}')
            self.clients.append(client_sock)

            # Уведомляем всех клиентов о новом подключении
            threading.Thread(target=self.handle_client, args=(client_sock,), daemon=True).start()

    def broadcast_ip(self):
        broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        server_ip = socket.gethostbyname(socket.gethostname())
        broadcast_message = f'SERVER_IP:{server_ip}'.encode('utf-8')

        while True:
            broadcast_sock.sendto(broadcast_message, ('<broadcast>', 37021))
            print(f'Рассылка IP-сервера: {server_ip}')
            threading.Event().wait(2)

    def handle_client(self, client_sock):
        while True:
            try:
                message = client_sock.recv(1024).decode('utf-8')
                if message:
                    # print(f'Сообщение от клиента: {message}')
                    self.broadcast_message(message)
            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                break

    def broadcast_message(self, message):
        for client in self.clients:
            try:
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    window = MainWindow(awaiting_window)

    sys.exit(app.exec_())