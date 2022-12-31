import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('center_window')

        self.resize(1100, 600)

        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()

        new_left = round((screen.width()-size.width()) / 2)
        new_top = round((screen.height()-size.height()) / 2)

        self.move(new_left, new_top)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainWindow()

    main.show()

    sys.exit(app.exec_())