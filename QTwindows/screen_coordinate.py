import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QPushButton


def on_clicked():
    print("")

    print("wedget.x()=", wedget.x()) # 窗口坐标
    print("wedget.y()=", wedget.y()) # 窗口坐标
    print("wedget.width()=", wedget.width())  # 工作区宽度
    print("wedget.height()=", wedget.height()) # 工作区高度

    print("")

    print("wedget.geometry().x()=", wedget.geometry().x()) # 工作区坐标
    print("wedget.geometry().y()=", wedget.geometry().y()) # 工作区坐标
    print("wedget.geometry().width()=", wedget.geometry().width())  # 工作区宽度
    print("wedget.geometry().height()=", wedget.geometry().height()) # 工作区高度

    print("")

    print("wedget.frameGeometry().x()=", wedget.frameGeometry().x()) # 窗口坐标
    print("wedget.frameGeometry().y()=", wedget.frameGeometry().y()) # 窗口坐标
    print("wedget.frameGeometry().width()=", wedget.frameGeometry().width()) # 窗口宽度
    print("wedget.frameGeometry().height()=", wedget.frameGeometry().height()) # 窗口高度


app = QApplication(sys.argv)

wedget = QWidget()

button = QPushButton(wedget)
button.setText('button')

button.move(50, 50)

button.clicked.connect(on_clicked)

wedget.resize(200, 200)
wedget.move(300, 300)

wedget.setWindowTitle('screen_coordinate')

wedget.show()

sys.exit(app.exec())


