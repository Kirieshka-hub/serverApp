import socket
import threading

class TicTacToeServer:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.clients = []

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('192.168.194.7', 65434))
        server_socket.listen(2)
        print("Сервер запущен, ожидаем подключения...")

        while len(self.clients) < 2:
            client_socket, addr = server_socket.accept()
            print(f"Подключен {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            move = client_socket.recv(1024).decode()
            if move:
                self.make_move(move)
                self.broadcast_board()

    def make_move(self, move):
        index = int(move)
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def broadcast_board(self):
        board_state = ','.join(self.board)
        for client in self.clients:
            client.send(board_state.encode())

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start_server()