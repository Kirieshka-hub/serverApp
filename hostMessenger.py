import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5 import QtCore
import sys
import sqlite3
from initUI import Ui_MainWindow


def create_database():
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            ip_address TEXT,
            port INTEGER
        )
        ''')
        connection.commit()
    except sqlite3.Error as e:
        print(f'Ошибка при создании базы данных: {e}')
    finally:
        if connection:
            connection.close()


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
        self.client_addresses = {}
        self.awaiting_window = awaiting_window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(('', 53210))
        self.server_sock.listen(5)

        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        print('Сервер запущен, ожидание подключения клиента...')
        threading.Thread(target=self.broadcast_ip, daemon=True).start()

        while True:
            client_sock, client_addr = self.server_sock.accept()
            print(f'Клиент подключен от {client_addr}')

            # Сохранение сокета клиента
            self.client_addresses[client_addr] = client_sock
            threading.Thread(target=self.handle_client, args=(client_sock, client_addr), daemon=True).start()

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
        try:
            while True:
                message = client_sock.recv(1024).decode('utf-8')
                if message:
                    if message.startswith("REGISTER:"):
                        self.register_user(message, client_sock, addr)
                    elif message.startswith("LOGIN:"):
                        self.login_user(message, client_sock, addr)
                    elif message.startswith("GET_CLIENT_LIST"):
                        self.send_client_list()
                    elif message.startswith("TO:"):
                        # Обработка отправки сообщения конкретному пользователю
                        self.send_message_to_client(message, client_sock)
                    else:
                        self.broadcast_message(message, client_sock)
                else:
                    break
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
        finally:
            # Удаление клиента при отключении
            self.remove_client(addr)
            client_sock.close()

    def remove_client(self, addr):
        """Удаление клиента и обновление списка пользователей"""
        if addr in self.client_addresses:
            del self.client_addresses[addr]

        for sock in self.clients:
            if sock.getpeername() == addr:
                self.clients.remove(sock)
                break

        print(f"Client {addr} отключился")
        # Отправляем обновленный список всем клиентам
        self.send_client_list()

    def register_user(self, message, client_sock, addr):
        parts = message.split(":")
        if len(parts) >= 3:
            username = parts[1]
            password = parts[2]
            try:
                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute('INSERT INTO users (username, password, ip_address, port) VALUES (?, ?, ?, ?)',
                               (username, password, addr[0], addr[1]))
                connection.commit()
                client_sock.sendall("REGISTER_SUCCESS".encode('utf-8'))
                self.clients.append(client_sock)
                self.client_addresses[addr] = client_sock
            except sqlite3.IntegrityError:
                client_sock.sendall("REGISTER_FAIL:Username already exists".encode('utf-8'))
            except Exception as e:
                print(f"Ошибка при регистрации пользователя: {e}")
                client_sock.sendall(f"REGISTER_FAIL:{e}".encode('utf-8'))
            finally:
                if connection:
                    connection.close()
        else:
            client_sock.sendall("REGISTER_FAIL:Invalid format".encode('utf-8'))

    def login_user(self, message, client_sock, addr):
        parts = message.split(":")
        if len(parts) >= 3:
            username = parts[1]
            password = parts[2]
            try:
                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
                result = cursor.fetchone()
                if result and result[0] == password:
                    cursor.execute('UPDATE users SET ip_address = ?, port = ? WHERE username = ?', (addr[0], addr[1], username))
                    connection.commit()
                    client_sock.sendall("LOGIN_SUCCESS".encode('utf-8'))
                    self.clients.append(client_sock)
                    self.client_addresses[addr] = client_sock
                else:
                    client_sock.sendall("LOGIN_FAIL:Invalid username or password".encode('utf-8'))
            except Exception as e:
                print(f"Ошибка при входе пользователя: {e}")
                client_sock.sendall(f"LOGIN_FAIL:{e}".encode('utf-8'))
            finally:
                if connection:
                    connection.close()
        else:
            client_sock.sendall("LOGIN_FAIL:Invalid format".encode('utf-8'))

    def send_client_list(self, client_sock=None):
        try:
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute('SELECT username, ip_address, port FROM users WHERE ip_address IS NOT NULL')
            clients = cursor.fetchall()
            client_list = [f"{username}:{ip}:{port}" for username, ip, port in clients]
            message = "CLIENT_LIST:" + ",".join(client_list)

            # Отправляем сообщение каждому подключенному клиенту
            for client in self.clients:
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Ошибка при отправке списка клиенту: {e}")

        except Exception as e:
            print(f"Ошибка при получении списка клиентов: {e}")
        finally:
            if connection:
                connection.close()
    def send_message_to_client(self, message, sender_sock):
        """
        Отправляет сообщение конкретному клиенту на основе IP.
        Формат сообщения: TO:<IP>:<message>
        """
        try:
            # Извлекаем IP-адрес и сообщение из команды
            parts = message.split(":")
            if len(parts) >= 3:
                target_ip = parts[1]
                msg_content = ":".join(parts[2:])

                # Найдем сокет клиента по IP
                target_sock = None
                for addr, sock in self.client_addresses.items():
                    if addr[0] == target_ip:
                        target_sock = sock
                        break

                if target_sock:
                    target_sock.sendall(f"Сообщение от {sender_sock.getpeername()}: {msg_content}".encode('utf-8'))
                    print(f"Сообщение отправлено на {target_ip}")
                else:
                    sender_sock.sendall(f"ERROR: Клиент с IP {target_ip} не найден.".encode('utf-8'))
            else:
                sender_sock.sendall("ERROR: Неверный формат сообщения.".encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            sender_sock.sendall(f"ERROR: {e}".encode('utf-8'))

    def broadcast_message(self, message, sender):
        for client in self.clients:
            if sender != client:
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")


if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    window = MainWindow(awaiting_window)
    sys.exit(app.exec_())
