import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMainWindow
from PyQt5 import QtCore
import sys
from  initUI import Ui_MainWindow


class AwaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ожидание подключения')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(100, 100, 300, 100)
        self.label = QLabel("Ожидание подключения клиента...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow(QMainWindow):
    def __init__(self, awaiting_window):
        super().__init__()
        self.clients = []
        self.awaiting_window = awaiting_window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
            self.ui.listWidget.addItem(f"{client_addr}")

            self.notify_clients_of_new_connection()


            # self.awaiting_window.close()

            # Уведомляем всех клиентов о новом подключении
            threading.Thread(target=self.handle_client, args=(client_sock,client_addr), daemon=True).start()

    def notify_clients_of_new_connection(self):
        connected_clients = [f"{client.getpeername()}" for client in self.clients]
        message = f"Подключенные клиенты: {', '.join(connected_clients)}"
        self.broadcast_message(message, sender=None)

    def broadcast_ip(self):
        broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        server_ip = socket.gethostbyname(socket.gethostname())
        broadcast_message = f'SERVER_IP:{server_ip}'.encode('utf-8')

        while True:
            broadcast_sock.sendto(broadcast_message, ('<broadcast>', 37021))
            print(f'Рассылка IP-сервера: {server_ip}')
            threading.Event().wait(2)


    def handle_client(self, client_sock, addr):
        while True:
            try:
                message = client_sock.recv(1024).decode('utf-8')
                if message:
                    # print(f'Сообщение от клиента: {message}')
                    self.broadcast_message(message, client_sock)
                else:
                    break
            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                break
        print(f"Client {addr} disconnected")
        self.clients.remove(client_sock)
        # self.ui.listWidget.removeItemWidget(f"{addr}")
        client_sock.close()

    def broadcast_message(self, message, sender):
        for client in self.clients:
            if sender != client:
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    window = MainWindow(awaiting_window)
    # window.show()

    sys.exit(app.exec_())