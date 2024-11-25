import socket
import threading
import sqlite3
from PyQt5 import QtCore, QtWidgets
import sys
# from initUI import Ui_MainWindow


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
            port INTEGER,
            is_active INTEGER DEFAULT 0
        )
        ''')

        # Таблица сообщений
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_username TEXT,
            receiver_username TEXT,
            message TEXT,
            FOREIGN KEY(sender_username) REFERENCES users(username),
            FOREIGN KEY(receiver_username) REFERENCES users(username)
        )   
        ''')

        connection.commit()
    except sqlite3.Error as e:
        print(f'Ошибка при создании базы данных: {e}')
    finally:
        if connection:
            connection.close()


class AwaitingWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ожидание подключения')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(100, 100, 300, 100)
        self.label = QtWidgets.QLabel("Ожидание подключения клиента...", self)
        self.label.setGeometry(50, 20, 200, 50)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, awaiting_window):
        super().__init__()
        self.clients = []
        self.client_addresses = {}
        self.awaiting_window = awaiting_window
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(('', 53210))
        self.server_sock.listen(2)

        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        print('Сервер запущен, ожидание подключения клиента...')
        threading.Thread(target=self.broadcast_ip, daemon=True).start()

        while True:
            client_sock, client_addr = self.server_sock.accept()
            print(f'Клиент подключен от {client_addr}')

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
                        self.send_client_list(client_sock)
                    elif message.startswith("TO:"):
                        self.send_message_to_client(message, client_sock)
                    elif message.startswith("LOAD_CHAT:"):
                        self.load_chat(message, client_sock)
                    elif message.startswith("SAVE_CHAT:"):
                        self.save_chat(message, client_sock)
                    else:
                        self.broadcast_message(message, client_sock)
                else:
                    break
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
        finally:
            self.remove_client(addr)
            client_sock.close()

    def register_user(self, message, client_sock, addr):
        parts = message.split(":")
        if len(parts) >= 3:
            username = parts[1]
            password = parts[2]
            try:
                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute(
                    'INSERT INTO users (username, password, ip_address, port, is_active) VALUES (?, ?, ?, ?, ?)',
                    (username, password, addr[0], addr[1], 1))
                connection.commit()
                client_sock.sendall(f"REGISTER_SUCCESS:{username}".encode('utf-8'))  # Отправляем имя клиента
                self.clients.append(client_sock)
                self.client_addresses[addr] = client_sock
            except sqlite3.IntegrityError:
                client_sock.sendall("REGISTER_FAIL:Username already exists".encode('utf-8'))
            except Exception as e:
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
                    cursor.execute('UPDATE users SET ip_address = ?, port = ?, is_active = 1 WHERE username = ?',
                                   (addr[0], addr[1], username))
                    connection.commit()
                    client_sock.sendall(f"LOGIN_SUCCESS:{username}".encode('utf-8'))  # Отправляем имя клиента
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
            cursor.execute('SELECT username, ip_address, port FROM users WHERE is_active = 1')
            clients = cursor.fetchall()
            client_list = [f"{username}:{ip}:{port}" for username, ip, port in clients]
            message = "CLIENT_LIST:" + ",".join(client_list)

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

    def load_chat(self, message, client_sock):
        connection = None
        try:
            parts = message.split(":")
            if len(parts) == 2:
                chat_partner = parts[1]
                client_address = client_sock.getpeername()
                ip_address = client_address[0]
                port = client_address[1]

                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute('SELECT username FROM users WHERE ip_address = ? AND port = ?', (ip_address,port))
                sender = cursor.fetchone()
                if sender:
                    sender_username = sender[0]

                    cursor.execute('''
                    SELECT sender_username, message
                    FROM messages
                    WHERE (sender_username = ? AND receiver_username = ?)
                       OR (sender_username = ? AND receiver_username = ?)
                    ORDER BY id ASC
                    ''', (sender_username, chat_partner, chat_partner, sender_username))

                    messages = cursor.fetchall()
                    response = "CHAT_MESSAGES:" + "\n".join(
                        [f"{msg[1]}" for msg in messages]
                    )
                    client_sock.sendall(response.encode('utf-8'))

                else:
                    client_sock.sendall("ERROR: Пользователь не найден.".encode('utf-8'))
            else:
                client_sock.sendall("ERROR: Неверный формат запроса.".encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при загрузке чата: {e}")
            client_sock.sendall(f"ERROR: {e}".encode('utf-8'))
        finally:
            if connection:
                connection.close()

    def save_chat(self, message, client_sock):
        connection = None
        try:
            parts = message.split(":", 2)
            if len(parts) == 3:
                chat_partner = parts[1]
                chat_messages = parts[2]
                client_address = client_sock.getpeername()
                ip_address = client_address[0]
                port = client_address[1]

                if not chat_messages.strip():
                    return

                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute('SELECT username FROM users WHERE ip_address = ? AND port = ?', (ip_address, port))
                sender = cursor.fetchone()
                if sender:
                    sender_username = sender[0]

                    # Удалить старые сообщения между пользователями
                    cursor.execute('''
                    DELETE FROM messages
                    WHERE (sender_username = ? AND receiver_username = ?)
                       OR (sender_username = ? AND receiver_username = ?)
                    ''', (sender_username, chat_partner, chat_partner, sender_username))

                    # Сохранить новые сообщения
                    for line in chat_messages.split("\n"):
                        if line.strip():  # Проверить, что строка не пустая
                            cursor.execute('''
                            INSERT INTO messages (sender_username, receiver_username, message)
                            VALUES (?, ?, ?)
                            ''', (sender_username, chat_partner, line))

                    connection.commit()
                    print(f"Чат между {sender_username} и {chat_partner} успешно обновлен.")
                else:
                    client_sock.sendall("ERROR: Отправитель не найден.".encode('utf-8'))
            else:
                client_sock.sendall("ERROR: Неверный формат сохранения чата.".encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при сохранении чата: {e}")
            client_sock.sendall(f"ERROR: {e}".encode('utf-8'))
        finally:
            if connection:
                connection.close()

    def remove_client(self, addr):
        try:
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE users SET is_active = 0 WHERE ip_address = ? AND port = ?', (addr[0], addr[1]))
            connection.commit()

            if addr in self.client_addresses:
                del self.client_addresses[addr]

            for sock in self.clients:
                if sock.getpeername() == addr:
                    self.clients.remove(sock)
                    break

            print(f"Client {addr} отключился")
            self.send_client_list()
        except Exception as e:
            print(f"Ошибка при деактивации пользователя: {e}")
        finally:
            if connection:
                connection.close()

    def send_message_to_client(self, message, sender_sock):
        try:
            parts = message.split(":")
            if len(parts) >= 4:
                target_ip = parts[2]
                target_port = int(parts[-2])
                msg_content = parts[-1]

                target_sock = None
                for addr, sock in self.client_addresses.items():
                    if addr[0] == target_ip and addr[1] == target_port:
                        target_sock = sock
                        break

                if target_sock:
                    target_sock.sendall(
                        f"Сообщение от {sender_sock.getpeername()} ~ : {msg_content}".encode('utf-8'))
                else:
                    sender_sock.sendall(f"ERROR: Клиент с IP {target_ip} не найден.".encode('utf-8'))
            else:
                sender_sock.sendall("ERROR: Неверный формат сообщения.".encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            sender_sock.sendall(f"ERROR: {e}".encode('utf-8'))


if __name__ == "__main__":
    create_database()
    app = QtWidgets.QApplication(sys.argv)

    awaiting_window = AwaitingWindow()
    awaiting_window.show()

    window = MainWindow(awaiting_window)
    sys.exit(app.exec_())
