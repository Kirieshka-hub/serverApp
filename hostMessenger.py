import socket
import threading
import sqlite3
import os
import sys
from pathlib import Path

def get_db_path():
    if sys.platform.startswith('win'):
        base_dir = os.getenv('APPDATA', os.path.expanduser('~'))
        db_dir = os.path.join(base_dir, "MyMessengerApp")
    else:
        base_dir = os.path.expanduser('~/.local/share')
        db_dir = os.path.join(base_dir, "MyMessengerApp")

    Path(db_dir).mkdir(parents=True, exist_ok=True)

    return os.path.join(db_dir, "users.db")

def create_database():
    db_path = get_db_path()
    try:
        connection = sqlite3.connect(db_path)
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
        print(f'[Server] Ошибка при создании базы данных: {e}')
    finally:
        if connection:
            connection.close()



class ServerCore:
    def __init__(self, host='', port=53210):
        self.host = host
        self.port = port

        self.clients = []
        self.client_addresses = {}

        create_database()

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(5)
        print(f'[Server] Сервер запущен на порту {self.port}')

        self.accept_thread = threading.Thread(target=self.start_accept, daemon=True)
        self.accept_thread.start()

    def start_accept(self):
        print('[Server] Ожидаем подключений...')
        while True:
            try:
                client_sock, client_addr = self.server_sock.accept()
                print(f'[Server] Подключился клиент: {client_addr}')
                self.client_addresses[client_addr] = client_sock
                self.clients.append(client_sock)
                threading.Thread(target=self.handle_client,
                                 args=(client_sock, client_addr),
                                 daemon=True).start()
            except Exception as e:
                print('[Server] Ошибка в accept:', e)
                break

    def handle_client(self, client_sock, addr):
        try:
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                if message.startswith("REGISTER:"):
                    self.register_user(message, client_sock, addr)
                elif message.startswith("LOGIN:"):
                    self.login_user(message, client_sock, addr)
                elif message.startswith("GET_CLIENT_LIST"):
                    self.send_client_list()
                elif message.startswith("TO:"):
                    self.send_message_to_client(message, client_sock)
                elif message.startswith("LOAD_CHAT:"):
                    self.load_chat(message, client_sock)
                elif message.startswith("SAVE_CHAT:"):
                    self.save_chat(message, client_sock)
                else:
                    self.broadcast_message(message, client_sock)
        except Exception as e:
            print(f"[Server] Ошибка при обработке клиента {addr}: {e}")
        finally:
            self.remove_client(addr)
            client_sock.close()

    def register_user(self, message, client_sock, addr):
        parts = message.split(":")
        if len(parts) >= 3:
            username = parts[1]
            password = parts[2]

            if len(password) < 6:
                client_sock.sendall("REGISTER_FAIL:Password must be at least 6 characters long.".encode('utf-8'))
                return
            if not any(char.isdigit() for char in password):
                client_sock.sendall("REGISTER_FAIL:Password must contain at least one digit.".encode('utf-8'))
                return
            if not any(char.isalpha() for char in password):
                client_sock.sendall("REGISTER_FAIL:Password must contain at least one letter.".encode('utf-8'))
                return

            try:
                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password, ip_address, port, is_active) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password, addr[0], addr[1], 1))
                connection.commit()
                client_sock.sendall(f"REGISTER_SUCCESS:{username}".encode('utf-8'))
            except sqlite3.IntegrityError:
                client_sock.sendall("REGISTER_FAIL:Username already exists.".encode('utf-8'))
            except Exception as e:
                client_sock.sendall(f"REGISTER_FAIL:{e}".encode('utf-8'))
            finally:
                if connection:
                    connection.close()
        else:
            client_sock.sendall("REGISTER_FAIL:Invalid format.".encode('utf-8'))

    def login_user(self, message, client_sock, addr):
        parts = message.split(":")
        if len(parts) >= 3:
            username = parts[1]
            password = parts[2]
            connection = None
            try:
                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute('SELECT password FROM users WHERE username=?', (username,))
                row = cursor.fetchone()
                if row and row[0] == password:
                    # Обновим ip/port
                    cursor.execute('''
                        UPDATE users 
                        SET ip_address=?, port=?, is_active=1 
                        WHERE username=?
                    ''', (addr[0], addr[1], username))
                    connection.commit()
                    client_sock.sendall(f"LOGIN_SUCCESS:{username}".encode('utf-8'))
                else:
                    client_sock.sendall("LOGIN_FAIL:Invalid username or password".encode('utf-8'))
            except Exception as e:
                print(f'[Server] Ошибка при логине: {e}')
                client_sock.sendall(f"LOGIN_FAIL:{e}".encode('utf-8'))
            finally:
                if connection:
                    connection.close()
        else:
            client_sock.sendall("LOGIN_FAIL:Invalid format".encode('utf-8'))

    def send_client_list(self):
        connection = None
        try:
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute('SELECT username, ip_address, port FROM users WHERE is_active=1')
            rows = cursor.fetchall()
            client_list = [f"{u}:{ip}:{pt}" for (u, ip, pt) in rows]
            msg = "CLIENT_LIST:" + ",".join(client_list)
            self.broadcast_message(msg, None)
        except Exception as e:
            print("[Server] Ошибка в send_client_list:", e)
        finally:
            if connection:
                connection.close()

    def load_chat(self, message, client_sock):
        parts = message.split(":")
        if len(parts) != 2:
            client_sock.sendall("ERROR:Wrong LOAD_CHAT format.".encode('utf-8'))
            return

        chat_partner = parts[1]
        connection = None
        try:
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            ip, port = client_sock.getpeername()

            cursor.execute('SELECT username FROM users WHERE ip_address=? AND port=?', (ip, port))
            row = cursor.fetchone()
            if not row:
                client_sock.sendall("ERROR:User not found.".encode('utf-8'))
                return
            my_username = row[0]

            cursor.execute('''
                SELECT sender_username, message
                FROM messages
                WHERE (sender_username=? AND receiver_username=?)
                   OR (sender_username=? AND receiver_username=?)
                ORDER BY id ASC
            ''', (my_username, chat_partner, chat_partner, my_username))
            all_rows = cursor.fetchall()

            lines = [r[1] for r in all_rows]  # r[1] = message
            resp = "CHAT_MESSAGES:" + "\n".join(lines)
            client_sock.sendall(resp.encode('utf-8'))

        except Exception as e:
            client_sock.sendall(f"ERROR:{e}".encode('utf-8'))
        finally:
            if connection:
                connection.close()

    def save_chat(self, message, client_sock):
        parts = message.split(":", 2)
        if len(parts) != 3:
            client_sock.sendall("ERROR:Wrong SAVE_CHAT format.".encode('utf-8'))
            return

        chat_partner = parts[1]
        chat_text = parts[2]
        if not chat_text.strip():
            return

        connection = None
        try:
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            ip, port = client_sock.getpeername()

            cursor.execute('SELECT username FROM users WHERE ip_address=? AND port=?', (ip, port))
            row = cursor.fetchone()
            if not row:
                client_sock.sendall("ERROR:User not found (SAVE_CHAT).".encode('utf-8'))
                return
            my_username = row[0]

            cursor.execute('''
                DELETE FROM messages
                WHERE (sender_username=? AND receiver_username=?)
                   OR (sender_username=? AND receiver_username=?)
            ''', (my_username, chat_partner, chat_partner, my_username))

            for line in chat_text.split("\n"):
                line = line.strip()
                if line:
                    cursor.execute('''
                        INSERT INTO messages (sender_username, receiver_username, message)
                        VALUES (?,?,?)
                    ''', (my_username, chat_partner, line))
            connection.commit()

        except Exception as e:
            client_sock.sendall(f"ERROR:{e}".encode('utf-8'))
        finally:
            if connection:
                connection.close()

    def send_message_to_client(self, message, sender_sock):
        try:
            print(message)
            parts = message.split(":")
            if len(parts) >= 4:
                target_name = parts[1]
                target_ip = parts[2]
                target_port = int(parts[-2])
                msg_content = parts[-1]

                target_sock = None
                for addr, sock in self.client_addresses.items():
                    if addr[0] == target_ip and addr[1] == target_port:
                        target_sock = sock
                        break

                if target_sock:
                    sender_ip, sender_port = sender_sock.getpeername()
                    connection = sqlite3.connect('users.db')
                    cursor = connection.cursor()
                    cursor.execute('SELECT username FROM users WHERE ip_address=? AND port=?', (sender_ip, sender_port))
                    row = cursor.fetchone()

                    if row:
                        sender_username = row[0]

                        formatted_message = f"{sender_username}: {msg_content}"
                        target_sock.sendall(formatted_message.encode('utf-8'))
                    else:
                        sender_sock.sendall("ERROR: User not found.".encode('utf-8'))
                else:
                    sender_sock.sendall("ERROR: Target client not found.".encode('utf-8'))
            else:
                sender_sock.sendall("ERROR: Invalid 'TO:' format.".encode('utf-8'))
        except Exception as e:
            print(f"[Server] send_message_to_client error: {e}")
            sender_sock.sendall(f"ERROR:{e}".encode('utf-8'))

    def broadcast_message(self, message, sender_sock):
        for sock in self.clients:
            if sock != sender_sock:
                try:
                    sock.sendall(message.encode('utf-8'))
                except:
                    pass

    def remove_client(self, addr):
        try:
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE users SET is_active=0 WHERE ip_address=? AND port=?', (addr[0], addr[1]))
            connection.commit()
        except Exception as e:
            print(f"[Server] remove_client error: {e}")
        finally:
            if connection:
                connection.close()

        if addr in self.client_addresses:
            del self.client_addresses[addr]

        for c in self.clients:
            if c.getpeername() == addr:
                self.clients.remove(c)
                break

        print(f"[Server] Клиент {addr} отключился")
        self.send_client_list()
