import argparse
import sys
from PyQt5 import QtWidgets
from hostMessenger import create_database, MainWindow, AwaitingWindow  # Импортируйте необходимые классы из вашего сервера
from clientMessenger import MainWindow as ClientMainWindow

def main():
    parser = argparse.ArgumentParser(description='Запуск сервера или клиента.')
    parser.add_argument('--mode', choices=['server', 'client'], required=True,
                        help='Выберите режим: server или client')
    args = parser.parse_args()

    if args.mode == 'server':
        create_database()  # Создайте базу данных перед запуском сервера
        app = QtWidgets.QApplication(sys.argv)
        awaiting_window = AwaitingWindow()
        awaiting_window.show()
        server_window = MainWindow(awaiting_window)  # Запустите серверное окно
        sys.exit(app.exec_())
    else:
        app = QtWidgets.QApplication(sys.argv)
        awaiting_window = AwaitingWindow()
        awaiting_window.show()
        client_window = ClientMainWindow(awaiting_window)  # Запустите клиентское окно
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
