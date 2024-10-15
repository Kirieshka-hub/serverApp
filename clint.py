import sys
import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AwaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe - Waiting for Server')
        self.setGeometry(900, 100, 300, 100)
        self.label = QLabel("Looking for the server...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow(QMainWindow):
    def __init__(self, awaiting_window):
        super().__init__()

        # Set up window properties
        self.setWindowTitle('Tic Tac Toe - Game')
        self.setGeometry(900, 100, 400, 400)

        # Initialize buttons and board state
        self.buttons = [QPushButton(' ') for _ in range(9)]
        self.board = [' '] * 9

        # Set up UI components using QVBoxLayout
        self.init_ui()

        # Initialize socket
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Reference to awaiting window
        self.awaiting_window = awaiting_window

    def init_ui(self):
        layout = QVBoxLayout()

        # Add a title label above the buttons
        self.title_label = QLabel("Tic Tac Toe", self)
        self.title_label.setFont(QFont('Arial', 24))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        grid_layout = QGridLayout()

        for i in range(3):
            for j in range(3):
                button = self.buttons[i * 3 + j]
                button.setFont(QFont('Arial', 24))
                button.clicked.connect(self.button_clicked)
                button.setStyleSheet("background-color: lightgray;")
                button.setFixedSize(120, 120)
                button.setEnabled(False)
                grid_layout.addWidget(button, i, j)

        layout.addLayout(grid_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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

                for button in self.buttons:
                    button.setEnabled(True)

                threading.Thread(target=self.receive_moves, daemon=True).start()

            except Exception as e:
                print(f"Failed to connect: {e}")

    def receive_moves(self):
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
                    button.setText('X')
                    self.board[index] = 'X'

                    # Проверяем на победителя после хода сервера
                    if not self.check_winner():
                        self.on_buttons()

            except ValueError:
                pass

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
            button.setText('O')
            move_str = str(index)
            try:
                # Обновляем локальное состояние доски.
                self.board[index] = 'O'

                # Отправляем ход на сервер.
                self.client_sock.send(move_str.encode())

                # Проверяем на победителя после своего хода
                if not self.check_winner():
                    self.disable_buttons()  # Отключаем кнопки после хода
            except Exception as e:
                print(f"Failed to send move: {e}")

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
            threading.Event().wait(2)
            self.restart_game()
            return True

        return False

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

    client_window = MainWindow(awaiting_window)

    client_window.connect_to_server()

    client_window.show()

    sys.exit(app.exec_())