import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QPushButton


class QuitWindow(QMainWindow):
    def __init__(self, parent=None):

        super(QuitWindow, self).__init__(parent)

        self.setWindowTitle('quit_window')

        self.resize(1100, 600)

        self.quit_button = QPushButton('quit button')
        self.quit_button.clicked.connect(self.method_quit_button)

        self.button_2 = QPushButton('butt')

        layout = QHBoxLayout()
        layout.addWidget(self.quit_button)
        layout.addWidget(self.button_2)

        main_window = QWidget()
        main_window.setLayout(layout)

        self.setCentralWidget(main_window)

    def method_quit_button(self):
        sender = self.sender()

        print(sender.text() + ' pressed')

        app = QApplication.instance()

        app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = QuitWindow()

    main.show()

    sys.exit(app.exec_())
