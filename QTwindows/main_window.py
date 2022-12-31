import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('main_window')

        self.resize(1100, 600)

        self.status = self.statusBar()

        self.status.showMessage('欢迎!')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon('../Resources/icon.jpg'))

    main = MainWindow()

    main.show()

    sys.exit(app.exec())
