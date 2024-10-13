import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create vertical layout for the main window
        main_layout = QVBoxLayout()

        # Create a text area for displaying messages
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)  # Make it read-only
        main_layout.addWidget(self.text_area)

        # Create horizontal layout for input field and send button
        input_layout = QHBoxLayout()

        # Create input field for typing messages
        self.input_field = QLineEdit()
        input_layout.addWidget(self.input_field)

        # Create send button
        self.send_button = QPushButton('Send')
        input_layout.addWidget(self.send_button)

        # Add the input layout to the main layout
        main_layout.addLayout(input_layout)

        # Set the main layout to the window
        self.setLayout(main_layout)


