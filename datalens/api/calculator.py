import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.result_display = QLineEdit()
        self.layout.addWidget(self.result_display)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]

        for row in buttons:
            button_row = QHBoxLayout()
            for label in row:
                button = QPushButton(label)
                button.clicked.connect(self.handle_button_click)
                button_row.addWidget(button)
            self.layout.addLayout(button_row)

        self.central_widget.setLayout(self.layout)

        self.current_input = ""

    def handle_button_click(self):
        clicked_button = self.sender()
        clicked_text = clicked_button.text()

        if clicked_text == "=":
            try:
                result = str(eval(self.current_input))
                self.result_display.setText(result)
            except Exception as e:
                self.result_display.setText("Error")
            self.current_input = ""
        else:
            self.current_input += clicked_text
            self.result_display.setText(self.current_input)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
