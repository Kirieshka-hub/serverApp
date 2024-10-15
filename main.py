import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import sys


class AwaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe - Ожидание подключения')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(150, 150, 300, 100)
        self.label = QLabel("Ожидание подключения клиента...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow(QMainWindow):
    def __init__(self, awaiting_window):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe - Игра')
        self.setGeometry(100, 100, 400, 400)

        self.buttons = [QPushButton(' ') for _ in range(9)]
        self.board = [' '] * 9

        self.init_ui()

        # Server setup
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(('', 53210))
        self.server_sock.listen(1)

        # Broadcast setup
        self.broadcast_event = threading.Event()

        self.awaiting_window = awaiting_window

    def init_ui(self):
        layout = QVBoxLayout()

        # Add a label above the buttons
        self.title_label = QLabel("Tic Tac Toe", self)
        self.title_label.setFont(QFont('Arial', 24))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        grid_layout = QGridLayout()

        for i in range(3):
            for j in range(3):
                button = self.buttons[i * 3 + j]
                button.setFont(QFont('Arial', 24))
                button.setFixedSize(120, 120)
                button.clicked.connect(self.button_clicked)
                button.setEnabled(False)
                button.setStyleSheet("background-color: lightgray;")
                grid_layout.addWidget(button, i, j)

        layout.addLayout(grid_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_server(self):
        print('Сервер запущен, ожидание подключения клиента...')

        threading.Thread(target=self.broadcast_ip, daemon=True).start()

        # Wait for client connection
        self.client_sock, client_addr = self.server_sock.accept()

        print(f'Клиент подключен от {client_addr}')

        self.awaiting_window.close()

        # Stop broadcasting after connection
        self.broadcast_event.set()

        # Enable buttons after client connection
        self.on_buttons()

        # Start handling messages from client
        threading.Thread(target=self.handle_client, daemon=True).start()

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
            move_str = self.client_sock.recv(1024).decode()

            if move_str.startswith("Игрок"):
                self.title_label.setText(move_str)
                self.disable_buttons()
                continue

            try:
                index = int(move_str)

                if index >= 0 and index < len(self.board) and self.board[index] == ' ':
                    button = self.buttons[index]
                    button.setText('O')
                    self.board[index] = 'O'

                    # Проверяем на победителя после хода сервера
                    if not self.check_winner():
                        self.on_buttons()

            except ValueError:
                pass

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

        for combo in winning_combinations:
            if all(self.board[i] == 'X' for i in combo):
                message = "Игрок X выиграл!"
                self.title_label.setText(message)
                self.disable_buttons()
                # Автоматически перезапускаем игру после выигрыша
                threading.Event().wait(2)
                self.restart_game()
                return True

            elif all(self.board[i] == 'O' for i in combo):
                message = "Игрок O выиграл!"
                self.title_label.setText(message)
                self.disable_buttons()
                # Автоматически перезапускаем игру после выигрыша
                threading.Event().wait(2)
                self.restart_game()
                return True

        if all(cell != ' ' for cell in self.board):
            message = "Ничья!"
            self.title_label.setText(message)
            self.disable_buttons()
            threading.Event().wait(2)  # Задержка перед перезапуском для удобства восприятия
            self.restart_game()
            return True

        return False

    def disable_buttons(self):
        for button in self.buttons:
            button.setEnabled(False)

    def on_buttons(self):
        for button in self.buttons:
            button.setEnabled(True)

    def button_clicked(self):
        button = self.sender()
        index = self.buttons.index(button)

        if self.board[index] == ' ':
            button.setText('X')
            move_str = str(index)
            try:
                # Обновляем локальное состояние доски.
                self.board[index] = 'X'

                # Отправляем ход на сервер.
                self.client_sock.send(move_str.encode())

                # Проверяем на победителя после своего хода
                if not self.check_winner():
                    self.disable_buttons()
            except Exception as e:
                print(f"Failed to send move: {e}")

    def restart_game(self):
        for i in range(len(self.board)):
            self.board[i] = ' '
            button = self.buttons[i]
            button.setText(' ')

        # Обновляем заголовок и включаем кнопки
        self.title_label.setText("Tic Tac Toe")
        self.on_buttons()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    window = MainWindow(awaiting_window)
    window.start_server()
    window.show()

    sys.exit(app.exec_())