import time

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox

from splash import *
from main_menu import *
from config_manager import *

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
        new_left = round((screen.width( ) -size.width()) / 2)
        new_top = round((screen.height( ) -size.height()) / 2)
        self.move(new_left, new_top)

    def step(self,v=0):
        self.ui.splash_progress.setProperty("value", v)

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

        self.ui.label_monitor_show.setAlignment(Qt.AlignCenter)

        self.ui.quit_tab.clicked.connect(self.quit)
        self.ui.value_reset.clicked.connect(self.reset_config)

        self.ui.button_save_conf.clicked.connect(self.manual_save_conf)
        self.ui.button_read_conf.clicked.connect(self.manual_read_conf)

    def quit(self):
        self.save_config()
        save_conf()
        self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        new_left = round((screen.width( ) -size.width()) / 2)
        new_top = round((screen.height( ) -size.height()) / 2)
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

    def show_(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def reset_config(self):
        set_default()
        save_conf()
        self.load_config()
        QMessageBox.information(self, "Notification", "All settings has been reset.", QMessageBox.Yes)

    def manual_read_conf(self):
        load_conf()
        self.load_config()
        QMessageBox.information(self, "Notification", "Config has been loaded.", QMessageBox.Yes)

    def manual_save_conf(self):
        self.save_config()
        save_conf()
        QMessageBox.information(self, "Notification", "Config has been saved.", QMessageBox.Yes)

    def auto_update(self):
        while 1:
            time.sleep(0.8)
            self.save_config()

    def load_config(self):
        self.ui.value_aim_range_general.setValue(int(get_value('value_aim_range_general')))
        self.ui.value_dead_range_general.setValue(int(get_value('value_dead_range_general')))
        self.ui.value_pid_d_general.setValue(int(get_value('value_pid_d_general')))
        self.ui.value_pid_i_general.setValue(int(get_value('value_pid_i_general')))
        self.ui.value_pid_p_general.setValue(int(get_value('value_pid_p_general')))
        self.ui.value_aim_range_rifle.setValue(int(get_value('value_aim_range_rifle')))
        self.ui.value_dead_range_rifle.setValue(int(get_value('value_dead_range_rifle')))
        self.ui.value_pid_d_rifle.setValue(int(get_value('value_pid_d_rifle')))
        self.ui.value_pid_i_rifle.setValue(int(get_value('value_pid_i_rifle')))
        self.ui.value_pid_p_rifle.setValue(int(get_value('value_pid_p_rifle')))
        self.ui.value_aim_range_smg.setValue(int(get_value('value_aim_range_smg')))
        self.ui.value_dead_range_smg.setValue(int(get_value('value_dead_range_smg')))
        self.ui.value_pid_d_smg.setValue(int(get_value('value_pid_d_smg')))
        self.ui.value_pid_i_smg.setValue(int(get_value('value_pid_i_smg')))
        self.ui.value_pid_p_smg.setValue(int(get_value('value_pid_p_smg')))
        self.ui.value_aim_range_sniper.setValue(int(get_value('value_aim_range_sniper')))
        self.ui.value_dead_range_sniper.setValue(int(get_value('value_dead_range_sniper')))
        self.ui.value_pid_d_sniper.setValue(int(get_value('value_pid_d_sniper')))
        self.ui.value_pid_i_sniper.setValue(int(get_value('value_pid_i_sniper')))
        self.ui.value_pid_p_sniper.setValue(int(get_value('value_pid_p_sniper')))
        self.ui.value_aim_range_pistol.setValue(int(get_value('value_aim_range_pistol')))
        self.ui.value_dead_range_pistol.setValue(int(get_value('value_dead_range_pistol')))
        self.ui.value_pid_d_pistol.setValue(int(get_value('value_pid_d_pistol')))
        self.ui.value_pid_i_pistol.setValue(int(get_value('value_pid_i_pistol')))
        self.ui.value_pid_p_pistol.setValue(int(get_value('value_pid_p_pistol')))
        self.ui.value_max_fps.setValue(int(get_value('value_max_fps')))
        self.ui.value_confidence.setValue(int(get_value('value_confidence')))
        self.ui.value_image_size.setValue(int(get_value('value_image_size')))
        self.ui.value_weights.setCurrentIndex(int(get_value('value_weights')))
        self.ui.value_capture_target.setCurrentIndex(int(get_value('value_capture_target')))
        self.ui.value_capture_method.setCurrentIndex(int(get_value('value_capture_method')))
        self.ui.value_view_source.setCurrentIndex(int(get_value('value_view_source')))
        self.ui.value_custom_weights.setText(get_value('value_custom_weights'))
        self.ui.value_custom_capture.setText(get_value('value_custom_capture'))
        self.ui.value_enabled_rifle.setChecked(bool(int(get_value('value_enabled_rifle'))))
        self.ui.value_enabled_smg.setChecked(bool(int(get_value('value_enabled_smg'))))
        self.ui.value_enabled_sniper.setChecked(bool(int(get_value('value_enabled_sniper'))))
        self.ui.value_enabled_pistol.setChecked(bool(int(get_value('value_enabled_pistol'))))
        self.ui.value_gpu_accel.setChecked(bool(int(get_value('value_gpu_accel'))))
        self.ui.value_frame_sync.setChecked(bool(int(get_value('value_frame_sync'))))
        self.ui.value_unlimited_fps.setChecked(bool(int(get_value('value_unlimited_fps'))))
        return

    def save_config(self):
        set_value('value_aim_range_general', self.ui.value_aim_range_general.value())
        set_value('value_dead_range_general', self.ui.value_dead_range_general.value())
        set_value('value_pid_d_general', self.ui.value_pid_d_general.value())
        set_value('value_pid_i_general', self.ui.value_pid_i_general.value())
        set_value('value_pid_p_general', self.ui.value_pid_p_general.value())
        set_value('value_aim_range_rifle', self.ui.value_aim_range_rifle.value())
        set_value('value_dead_range_rifle', self.ui.value_dead_range_rifle.value())
        set_value('value_pid_d_rifle', self.ui.value_pid_d_rifle.value())
        set_value('value_pid_i_rifle', self.ui.value_pid_i_rifle.value())
        set_value('value_pid_p_rifle', self.ui.value_pid_p_rifle.value())
        set_value('value_aim_range_smg', self.ui.value_aim_range_smg.value())
        set_value('value_dead_range_smg', self.ui.value_dead_range_smg.value())
        set_value('value_pid_d_smg', self.ui.value_pid_d_smg.value())
        set_value('value_pid_i_smg', self.ui.value_pid_i_smg.value())
        set_value('value_pid_p_smg', self.ui.value_pid_p_smg.value())
        set_value('value_aim_range_sniper', self.ui.value_aim_range_sniper.value())
        set_value('value_dead_range_sniper', self.ui.value_dead_range_sniper.value())
        set_value('value_pid_d_sniper', self.ui.value_pid_d_sniper.value())
        set_value('value_pid_i_sniper', self.ui.value_pid_i_sniper.value())
        set_value('value_pid_p_sniper', self.ui.value_pid_p_sniper.value())
        set_value('value_aim_range_pistol', self.ui.value_aim_range_pistol.value())
        set_value('value_dead_range_pistol', self.ui.value_dead_range_pistol.value())
        set_value('value_pid_d_pistol', self.ui.value_pid_d_pistol.value())
        set_value('value_pid_i_pistol', self.ui.value_pid_i_pistol.value())
        set_value('value_pid_p_pistol', self.ui.value_pid_p_pistol.value())
        set_value('value_confidence', self.ui.value_confidence.value())
        set_value('value_max_fps', self.ui.value_max_fps.value())
        set_value('value_image_size', self.ui.value_image_size.value())
        set_value('value_weights', self.ui.value_weights.currentIndex())
        set_value('value_capture_target', self.ui.value_capture_target.currentIndex())
        set_value('value_capture_method', self.ui.value_capture_method.currentIndex())
        set_value('value_view_source', self.ui.value_view_source.currentIndex())
        set_value('value_custom_weights', self.ui.value_custom_weights.text())
        set_value('value_custom_capture', self.ui.value_custom_capture.text())
        set_value('value_enabled_rifle', int(self.ui.value_enabled_rifle.isChecked()))
        set_value('value_enabled_smg', int(self.ui.value_enabled_smg.isChecked()))
        set_value('value_enabled_sniper', int(self.ui.value_enabled_sniper.isChecked()))
        set_value('value_enabled_pistol', int(self.ui.value_enabled_pistol.isChecked()))
        set_value('value_gpu_accel', int(self.ui.value_gpu_accel.isChecked()))
        set_value('value_frame_sync', int(self.ui.value_frame_sync.isChecked()))
        set_value('value_unlimited_fps', int(self.ui.value_unlimited_fps.isChecked()))
        return

'''
    MainWindow.ui.label_monitor_show.setPixmap(QPixmap('Resources/icon/icon.png').scaled(400, 300, QtCore.Qt.KeepAspectRatio))
'''

def window_sleep(t=1):
    start = time.time()
    while time.time() - start <= t:
        QApplication.processEvents()
    return