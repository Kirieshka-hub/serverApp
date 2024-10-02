import socket
import threading
import sys


clients = []

def handle_client(client_socket, address):
    print(f"Подключен: {address}")
    clients.append(client_socket)


def disconn(client_socket, address):
    client_socket.close()
    clients.remove(client_socket)
    print(f"Отключен: {address}")

def receive_messages(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"~ {message.decode('utf-8')}")
        except:
            disconn(client_socket, address)
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostbyname(socket.gethostname()), 1026))
    server_socket.listen(5)
    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, address = server_socket.accept()
        thread_receive = threading.Thread(target=receive_messages, args=(client_socket,address))
        thread_receive.start()

        thread_send = threading.Thread(target=send_messages, args=(client_socket,))
        thread_send.start()

        thread_send = threading.Thread(target=handle_client, args=(client_socket,address))
        thread_send.start()
if __name__ == "__main__":
    run_server()
