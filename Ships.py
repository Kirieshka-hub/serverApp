import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox, QVBoxLayout, \
    QStackedWidget


class SeaBattle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Морской бой")
        self.setGeometry(500, 500, 800, 600)
        self.grid_size = 10  # Размер сетки
        self.ships_positions = []  # Список для хранения позиций кораблей
        #
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.init_game_page()
        self.init_second_page()

    def init_game_page(self):
        game_page = QWidget()
        self.grid_layout = QGridLayout(game_page)
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                button = QPushButton("")
                button.setFixedSize(50, 50)
                button.setStyleSheet("background-color: lightblue; border: 1px solid navy;")
                self.grid_layout.addWidget(button, i, j)
                self.buttons[i][j] = button

        change_button = QPushButton("Изменить расположение кораблей")
        change_button.clicked.connect(self.reset_ships)
        self.grid_layout.addWidget(change_button, self.grid_size, 0, 1, self.grid_size)

        done_button = QPushButton("Готово")
        done_button.clicked.connect(self.show_second_page)
        self.grid_layout.addWidget(done_button, self.grid_size + 1, 0, 1, self.grid_size)

        self.place_ships()

        self.stacked_widget.addWidget(game_page)

    def init_second_page(self):
        second_page = QWidget()
        layout = QVBoxLayout(second_page)

        first_grid_layout = QGridLayout()

        first_buttons = [[None for _ in range(10)] for _ in range(10)]

        for i in range(10):
            for j in range(10):
                button = QPushButton("")
                button.setFixedSize(50, 50)
                button.setStyleSheet("background-color: lightblue; border: 1px solid navy;")
                first_grid_layout.addWidget(button, i, j)
                first_buttons[i][j] = button

                if (i, j) in self.ships_positions:
                    button.setText("🚢")

        layout.addLayout(first_grid_layout)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator.setLineWidth(2)
        layout.addWidget(separator)

        second_grid_layout = QGridLayout()

        second_buttons = [[None for _ in range(10)] for _ in range(10)]

        for i in range(10):
            for j in range(10):
                button = QPushButton("")
                button.setFixedSize(50, 50)
                button.setStyleSheet("background-color: lightblue; border: 1px solid navy;")
                second_grid_layout.addWidget(button, i, j)
                second_buttons[i][j] = button

                if (i, j) in self.ships_positions:
                    button.setText("🚢")

        layout.addLayout(second_grid_layout)

        done_button = QPushButton("Готово")
        done_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))  # Go back to game page

        layout.addWidget(done_button)

        # Add the second page to the stacked widget
        self.stacked_widget.addWidget(second_page)

    def is_place_valid(self, row, col, length, orientation):
        if orientation == 'horizontal':
            if col + length > self.grid_size:
                return False
            for i in range(-1, length + 1):
                if row < 0 or row >= self.grid_size or col + i < 0 or col + i >= self.grid_size:
                    return False
                if self.buttons[row][col + i].text() == "🚢":
                    return False
        else:
            if row + length > self.grid_size:
                return False
            for i in range(-1, length + 1):
                if row + i < 0 or row + i >= self.grid_size or col < 0 or col >= self.grid_size:
                    return False
                if self.buttons[row + i][col].text() == "🚢":
                    return False

        return True

    def place_ships(self):
        ships = [
            (1, 4),
            (2, 3),
            (3, 2),
            (4, 1)
        ]

        for count, length in ships:
            for _ in range(count):
                placed = False
                while not placed:
                    orientation = random.choice(['horizontal', 'vertical'])
                    if orientation == 'horizontal':
                        row = random.randint(0, self.grid_size - 1)
                        col = random.randint(0, self.grid_size - length)
                        if self.is_place_valid(row, col, length, orientation):
                            for i in range(length):
                                self.buttons[row][col + i].setText("🚢")
                                # Store ship positions
                                self.ships_positions.append((row, col + i))
                            placed = True
                    else:
                        row = random.randint(0, self.grid_size - length)
                        col = random.randint(0, self.grid_size - 1)
                        if self.is_place_valid(row, col, length, orientation):
                            for i in range(length):
                                self.buttons[row + i][col].setText("🚢")
                                # Store ship positions
                                self.ships_positions.append((row + i, col))
                            placed = True

    def reset_ships(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].setText("")
                self.buttons[i][j].setStyleSheet("background-color: lightblue; border: 1px solid navy;")

        self.ships_positions.clear()
        self.place_ships()

    def show_second_page(self):

        second_page_index = 1

        second_page_widget = self.stacked_widget.widget(second_page_index)

        first_grid_layout = second_page_widget.layout().itemAt(0).layout()

        for (i, j) in self.ships_positions:
            first_grid_layout.itemAt(i * 10 + j).widget().setText("🚢")

        self.stacked_widget.setCurrentIndex(second_page_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeaBattle()
    window.show()
    sys.exit(app.exec_())