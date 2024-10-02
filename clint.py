import socket
import threading
import sys


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"~ {message.decode('utf-8')}")
        except:
            print("Ошибка при получении сообщения.")
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((socket.gethostbyname(socket.gethostname()), 1026))
    print("~Подключенно~")

    thread_receive = threading.Thread(target=receive_messages, args=(client_socket,))
    thread_receive.start()

    thread_send = threading.Thread(target=send_messages, args=(client_socket,))
    thread_send.start()

if __name__ == "__main__":
    run_client()
