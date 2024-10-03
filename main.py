import socket
import threading
import time


HOST = '192.168.136.7'
PORT = 65432
clients = []
client_last_activity = {}
client_message_count = {}
MAX_CLIENTS = 100
MESSAGE_LIMIT = 5
LIMIT_INTERVAL = 10
TIMEOUT = 60


def handle_client(conn, addr):
    print(f'**Подключен {addr}**')
    clients.append(conn)
    client_last_activity[conn] = time.time()
    client_message_count[conn] = []

    try:
        while True:

            if time.time() - client_last_activity[conn] > TIMEOUT:
                print(f'**Клиент {addr} отключен из-за бездействия.**')
                break

            message = conn.recv(1024).decode('utf-8')
            if message:
                client_last_activity[conn] = time.time()

                current_time = time.time()
                client_message_count[conn] = [timestamp for timestamp in client_message_count[conn] if
                                              current_time - timestamp < LIMIT_INTERVAL]
                if len(client_message_count[conn]) >= MESSAGE_LIMIT:
                    print(f'**Клиент {addr} отключен из-за спама.**')
                    break
                client_message_count[conn].append(current_time)

                for client in clients:
                    if client != conn:
                        client.send(message.encode('utf-8'))
            else:
                break
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        clients.remove(conn)
        del client_last_activity[conn]
        del client_message_count[conn]
        print(f'**Отключен {addr}**')


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print('**Сервер запущен, ожидает клиентов...**')

        while True:
            if len(clients) >= MAX_CLIENTS:
                print('**Достигнут максимальный лимит подключенных клиентов. Ожидание освобождения.**')
                time.sleep(5)
                continue

            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()
