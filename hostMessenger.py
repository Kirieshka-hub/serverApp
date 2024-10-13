import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5 import QtCore
import sys
from initUI import ChatApp


class AwaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ожидание подключения')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(800, 850, 300, 100)
        self.label = QLabel("Ожидание подключения клиента...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow(QMainWindow):
    def __init__(self, awaiting_window):
        super().__init__()
        self.setWindowTitle('Messenger')
        self.setGeometry(600, 600, 800, 600)

        # Создаем экземпляр ChatApp и устанавливаем его как центральный виджет
        self.ui = ChatApp()
        self.setCentralWidget(self.ui)

        self.ui.input_field.setReadOnly(True)

        # Настройка сервера
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(('', 53210))
        self.server_sock.listen(1)

        # Настройка широковещательной рассылки
        self.broadcast_event = threading.Event()

        self.awaiting_window = awaiting_window

        # Запускаем поток для ожидания подключения
        # threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        print('Сервер запущен, ожидание подключения клиента...')

        # Запускаем поток для широковещательной рассылки
        threading.Thread(target=self.broadcast_ip, daemon=True).start()

        # Ожидаем подключения клиента
        self.client_sock, client_addr = self.server_sock.accept()
        print(f'Клиент подключен от {client_addr}')
        self.ui.input_field.setReadOnly(False)


        # Останавливаем рассылку после подключения
        self.broadcast_event.set()

        # Закрываем окно ожидания и показываем главное окно чата
        self.awaiting_window.close()

        threading.Thread(target=self.handle_client, daemon=True).start()

        self.ui.send_button.clicked.connect(self.send_message)

    # def close_awaiting_window(self):
    #     threading.Thread(target=self.awaiting_window.close).start()

    def broadcast_ip(self):
        broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        server_ip = socket.gethostbyname(socket.gethostname())
        broadcast_message = f'SERVER_IP:{server_ip}'.encode('utf-8')

        while not self.broadcast_event.is_set():
            broadcast_sock.sendto(broadcast_message, ('<broadcast>', 37021))
            print(f'Рассылка IP-сервера: {server_ip}')
            threading.Event().wait(2)

    def handle_client(self):
        while True:
            try:
                message = self.client_sock.recv(1024).decode('utf-8')
                if message:
                    # print(f'Сообщение от клиента: {message}')
                    self.ui.text_area.append(f'Клиент: {message}')  # Отображаем сообщение в текстовом поле
            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                break

    def send_message(self):
        message = self.ui.input_field.text()
        if message:
            try:
                self.client_sock.sendall(message.encode('utf-8'))
                # print(f'Отправлено сообщение: {message}')
                self.ui.text_area.append(f'Вы: {message}')  # Отображаем отправленное сообщение
                self.ui.input_field.clear()  # Очищаем поле ввода
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    window = MainWindow(awaiting_window)
    window.start_server()
    window.show()

    sys.exit(app.exec_())