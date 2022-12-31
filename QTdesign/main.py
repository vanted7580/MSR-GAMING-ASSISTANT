from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QIcon, QColor, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

from splash import *
from main_menu import *
import sys
import time

class SplashWindowInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SplashWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()
        self.ui.splash.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=0, yOffset=0, color=QColor(0, 0, 0, 90)))

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        new_left = round((screen.width()-size.width()) / 2)
        new_top = round((screen.height()-size.height()) / 2)
        self.move(new_left, new_top)

class MainWindowInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        self.ui.main.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=0, color=QColor(0, 0, 0, 20)))
        self.ui.logo.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=20, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 20)))
        self.ui.drag_bar.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 20)))
        self.ui.tabs.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 20)))
        self.ui.main_elements.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 20)))
        self.ui.bar_seach.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 20)))
        self.ui.bar_conf.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 20)))
        self.ui.bar_msg.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 20)))

        self.ui.user_interface_tab.clicked.connect(lambda: self.ui.main_elements.setCurrentIndex(0))
        self.ui.game_assistant_tab.clicked.connect(lambda: self.ui.main_elements.setCurrentIndex(1))
        self.ui.conf_tab.clicked.connect(lambda: self.ui.main_elements.setCurrentIndex(2))
        self.ui.monitor_tab.clicked.connect(lambda: self.ui.main_elements.setCurrentIndex(3))
        self.ui.advanced_tab.clicked.connect(lambda: self.ui.main_elements.setCurrentIndex(4))
        self.ui.about_tab.clicked.connect(lambda: self.ui.main_elements.setCurrentIndex(5))

        self.ui.weapon_general_tab.clicked.connect(lambda: self.ui.weapom_conf.setCurrentIndex(0))
        self.ui.weapon_rifle_tab.clicked.connect(lambda: self.ui.weapom_conf.setCurrentIndex(1))
        self.ui.weapon_smg_tab.clicked.connect(lambda: self.ui.weapom_conf.setCurrentIndex(2))
        self.ui.weapon_sniper_tab.clicked.connect(lambda: self.ui.weapom_conf.setCurrentIndex(3))
        self.ui.weapon_pistol_tab.clicked.connect(lambda: self.ui.weapom_conf.setCurrentIndex(4))

        self.ui.drag_bar.clicked.connect(self.showMinimized)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        new_left = round((screen.width()-size.width()) / 2)
        new_top = round((screen.height()-size.height()) / 2)
        self.move(new_left, new_top)

    _startPos = None
    _endPos = None
    _isTracking = False

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if type(e) != 'NoneType':
            if self._isTracking is True:
                self._endPos = e.pos() - self._startPos
                self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

start = time.time()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Resources/icon/icon.png'))

    SplashWindow = SplashWindowInterface()
    MainWindow = MainWindowInterface()

    SplashWindow.show()

    #SplashWindow.ui.splash_progress.setVisible()

    while time.time() - start <= 2:
        QApplication.processEvents()

    MainWindow.show()
    SplashWindow.close()

    MainWindow.raise_()
    MainWindow.activateWindow()

    sys.exit(app.exec())


'''

        MainMenu.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainMenu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.main.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=0, yOffset=0, color=QColor(0, 0, 0, 60)))
        self.logo_light.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=3, yOffset=3, color=QColor(0, 0, 0, 30)))
        
        self.monito_tab.clicked.connect(lambda: self.main_elements.setCurrentIndex(3))
        
        window.value_fps_core.setText("10.00")
        
        self.ui.splash_progress.setValue(50)
        
        MainWindow.ui.value_max_fps.value()
        
        self.value_fps_opencv.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            
'''


