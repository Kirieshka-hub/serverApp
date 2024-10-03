import socket
import uuid
import threading


HOST = '192.168.136.7'
PORT = 65432


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break


def start_client():
    client_id = str(uuid.uuid4())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))


        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

        print(f'Ваш ID: {client_id}')

        while True:
            try:
                message = input()
                if message.lower() == 'exit':
                    print(f"[{client_id}] disconnect")
                    break
                full_message = f'[{client_id}] {message}'
                client_socket.send(full_message.encode('utf-8'))
            except:
                pass

if __name__ == "__main__":
    start_client()
