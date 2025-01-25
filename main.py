import sys
import socket
import threading
from PyQt5 import QtWidgets

from hostMessenger import ServerCore
from clientMessenger import MainWindow

def try_connect_to_server(ip, port=53210, timeout=0.5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def scan_for_server_tcp(port=53210):
    local_ip = socket.gethostbyname(socket.gethostname())
    subnet = ".".join(local_ip.split(".")[:3])
    print(f"[Launcher] Сканирование сети {subnet}.x на порт {port}...")

    found_server = None

    threads = []
    results = []

    def worker(target_ip):
        if try_connect_to_server(target_ip, port):
            results.append(target_ip)

    for i in range(1, 255):
        target_ip = f"{subnet}.{i}"
        t = threading.Thread(target=worker, args=(target_ip,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if results:
        found_server = results[0]

    return found_server

def main():
    server_ip = scan_for_server_tcp(port=53210)

    if server_ip:
        print(f"[Launcher] Сервер найден по адресу {server_ip}")
        host_for_client = server_ip
        server_core = None
    else:
        print("[Launcher] Сервер не найден, поднимаем локально.")
        server_core = ServerCore(host='', port=53210)
        host_for_client = '127.0.0.1'

    app = QtWidgets.QApplication(sys.argv)
    client_window = MainWindow(server_ip=host_for_client, server_port=53210)
    client_window.show()
    app.exec_()

    if server_core:
        print("[Launcher] Завершаем сервер (при выходе).")

if __name__ == "__main__":
    main()
