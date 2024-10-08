import sys
import socket
import threading
from PyQt5 import QtWidgets, QtGui


class TicTacToeClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.194.7', 65434))

        threading.Thread(target=self.receive_board).start()

    def init_ui(self):
        self.setWindowTitle('Крестики-нолики')
        self.grid_layout = QtWidgets.QGridLayout()

        self.buttons = [QtWidgets.QPushButton(' ') for _ in range(9)]

        for i in range(3):
            for j in range(3):
                button = self.buttons[i * 3 + j]
                button.setFont(QtGui.QFont('Arial', 24))
                button.clicked.connect(lambda _, x=i * 3 + j: self.make_move(x))
                self.grid_layout.addWidget(button, i, j)

        self.setLayout(self.grid_layout)

    def make_move(self, index):
        if self.buttons[index].text() == ' ':
            self.client_socket.send(str(index).encode())

    def receive_board(self):
        while True:
            board_state = self.client_socket.recv(1024).decode().split(',')
            for i in range(9):
                self.buttons[i].setText(board_state[i])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client = TicTacToeClient()
    client.show()
    sys.exit(app.exec_())