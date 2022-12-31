from PyQt5.QtGui import QIcon

from windows import *
from detect import *
from capture import *

import sys
import threading
import ctypes


from multiprocessing import sharedctypes, Process, Queue

CPU_SPACE_TIME = 0.001

class InfIter:
    def __iter__(self):
        return self
    def __next__(self):
        pass

class process_capture(Process):
    def __init__(self, capture_img, capture_hwnd, vsync, vsync_state, resolution, is_quit):
        super(process_capture, self).__init__()
        self.capture_img = capture_img
        self.capture_hwnd = capture_hwnd
        self.vsync = vsync
        self.vsync_state = vsync_state
        self.resolution = resolution
        self.is_quit = is_quit

        _, _, width, height = get_fullscreen_size()
        self.screen_res = width * height * 3

    def run(self):
        for _ in InfIter():
            if np.frombuffer(self.is_quit, dtype=bool):
                break

            if np.frombuffer(self.vsync, dtype=bool)[0]:
                if np.frombuffer(self.vsync_state, dtype=bool)[0] and not np.frombuffer(self.is_quit, dtype=bool):
                    time.sleep(CPU_SPACE_TIME)
                    continue

            hwnd = get_hwnd(target="Apex Legends")
            if hwnd == 0:
                time.sleep(CPU_SPACE_TIME)
                continue
            #np.frombuffer(self.capture_hwnd, dtype=np.uint64)[:] = hwnd
            #hwnd = int(np.frombuffer(self.capture_hwnd, dtype=np.uint64)[0])

            frame, left, top, width, height = capture_app_win32(hwnd)

            if frame is None:
                time.sleep(CPU_SPACE_TIME)
                continue

            frame = np.array(frame).flatten(order='C')
            np.frombuffer(self.capture_img, dtype=np.uint8)[:] = np.pad(frame, (0, self.screen_res - len(frame)),
                                                                        'constant', constant_values=(0, 0))
            np.frombuffer(self.resolution, dtype=np.uint64)[:] = [width, height]

            np.frombuffer(self.vsync_state, dtype=bool)[:] = True


class process_detect(Process):
    def __init__(self, capture_img, vsync, vsync_state, is_quit, detected_data, detected_img, view_img,
                 gpu_accel,
                 confidence, imgsz, resolution):
        super(process_detect, self).__init__()
        self.capture_img = capture_img
        self.vsync = vsync
        self.vsync_state = vsync_state
        self.is_quit = is_quit
        self.detected_data = detected_data
        self.detected_img = detected_img
        self.view_img = view_img
        self.gpu_accel = gpu_accel
        self.confidence = confidence
        self.imgsz = imgsz
        self.resolution = resolution
        self.ai = ai_core()

        init(target=self.ai.update_model, args=('Weights/apex.pt',))


    def run(self):

        for _ in InfIter():

            if np.frombuffer(self.is_quit, dtype=bool):
                break

            if np.frombuffer(self.vsync, dtype=bool)[0]:
                if np.frombuffer(self.vsync_state, dtype=bool)[0] and not np.frombuffer(self.is_quit, dtype=bool):
                    time.sleep(CPU_SPACE_TIME)
                    continue

            resolution = np.frombuffer(self.resolution, dtype=np.uint64)
            res_length = int(resolution[0] * resolution[1] * 3)

            if res_length == 0: continue

            frame = np.frombuffer(self.capture_img, dtype=np.uint8)
            frame = frame[:res_length]
            frame = frame.reshape(resolution[1], resolution[0], 3)

            list, img = self.ai.detect(img0=frame, imgsz=640, view_img=True)

            np.frombuffer(self.vsync_state, dtype=bool)[:] = True
            ##



class process_vsync(Process):  # V-sync
    def __init__(self, vsync, vsync_state1, vsync_state2, refresh_rate, is_quit):
        super(process_vsync, self).__init__()
        self.vsync = vsync
        self.vsync_state1 = vsync_state1
        self.vsync_state2 = vsync_state2
        self.refresh_rate = refresh_rate
        self.is_quit = is_quit
        self.last_update = 0

    def run(self):
        time_space = 1 / np.frombuffer(self.refresh_rate, dtype=np.uint8)
        self.last_update = time.time()
        for _ in InfIter():
            if np.frombuffer(self.is_quit, dtype=bool):
                break
            #print(np.frombuffer(self.vsync_state1, dtype=bool)[0], np.frombuffer(self.vsync_state2, dtype=bool)[0])
            time.sleep(CPU_SPACE_TIME)
            if np.frombuffer(self.vsync, dtype=bool)[0]:
                if np.frombuffer(self.vsync_state1, dtype=bool)[0] and np.frombuffer(self.vsync_state2, dtype=bool)[0]:
                    if time.time() - self.last_update >= time_space:
                        np.frombuffer(self.vsync_state1, dtype=bool)[:] = False
                        np.frombuffer(self.vsync_state2, dtype=bool)[:] = False
                        time_space = 1 / np.frombuffer(self.refresh_rate, dtype=np.uint8)
                        self.last_update = time.time()
            else:
                break


class process_aimbot(Process):
    def __init__(self, is_quit, detected_data):
        super(process_aimbot, self).__init__()
        self.is_quit = is_quit
        self.detected_data = detected_data

    def run(self):
        for _ in InfIter():
            if np.frombuffer(self.is_quit, dtype=bool):
                break
            time.sleep(CPU_SPACE_TIME)


# img_tmp, t0 = captue_screen_win32()
# xywh_list, im0, t0 = detect(img0=img_tmp, imgsz=640, conf_thres=0.45, view_img=True)


class aimbot_main():
    def __init__(self):
        # 初始化必要时数据
        left, top, width, height = get_fullscreen_size()

        # 截取图像
        self.capture_img = sharedctypes.RawArray(ctypes.c_int8, width * height * 3)
        # 截取对象hwnd
        self.capture_hwnd = sharedctypes.RawArray(ctypes.c_int64, 1)
        # 截取对象分辨率
        self.resolution = sharedctypes.RawArray(ctypes.c_int64, 2)

        # 识别信息
        self.detected_data = Queue(maxsize=1)
        # 识别图像
        self.detected_img = sharedctypes.RawArray(ctypes.c_int8, width * height * 3)
        # AI置信度
        self.confidence = sharedctypes.RawArray(ctypes.c_int64, 1)
        # 图像大小
        self.imgsz = sharedctypes.RawArray(ctypes.c_int64, 1)
        # 预览结果
        self.view_img = sharedctypes.RawArray(ctypes.c_bool, 1)
        # GPU加速
        self.gpu_accel = sharedctypes.RawArray(ctypes.c_bool, 1)

        # 帧同步
        self.vsync = sharedctypes.RawArray(ctypes.c_bool, 1)
        # 帧同步状态
        self.vsync_state1 = sharedctypes.RawArray(ctypes.c_bool, 1)
        self.vsync_state2 = sharedctypes.RawArray(ctypes.c_bool, 1)
        # 刷新状态(控制刷新率)
        self.refresh_rate = sharedctypes.RawArray(ctypes.c_int8, 1)
        # 退出
        self.is_quit = sharedctypes.RawArray(ctypes.c_bool, 1)

        self.load_config()

    def load_config(self):
        # 初始化参数
        np.frombuffer(self.capture_hwnd, dtype=np.uint64)[:] = 0
        np.frombuffer(self.confidence, dtype=np.uint64)[:] = 0
        np.frombuffer(self.imgsz, dtype=np.uint64)[:] = 0
        np.frombuffer(self.imgsz, dtype=np.uint64)[:] = 0
        np.frombuffer(self.view_img, dtype=bool)[:] = False
        np.frombuffer(self.gpu_accel, dtype=bool)[:] = False

        np.frombuffer(self.vsync, dtype=bool)[:] = True
        np.frombuffer(self.vsync_state1, dtype=bool)[:] = False
        np.frombuffer(self.vsync_state2, dtype=bool)[:] = False
        np.frombuffer(self.refresh_rate, dtype=np.uint8)[:] = 30
        np.frombuffer(self.is_quit, dtype=bool)[:] = False

    def quit(self):
        np.frombuffer(self.is_quit, dtype=bool)[:] = True

    def start(self):
        self.pro_capture = process_capture(self.capture_img, self.capture_hwnd, self.vsync, self.vsync_state1,
                                      self.resolution, self.is_quit)

        self.pro_detect = process_detect(self.capture_img, self.vsync, self.vsync_state2, self.is_quit,
                                    self.detected_data, self.detected_img, self.view_img, self.gpu_accel,
                                    self.confidence, self.imgsz, self.resolution)

        self.pro_vsync = process_vsync(self.vsync, self.vsync_state1, self.vsync_state2,
                                  self.refresh_rate, self.is_quit)

        self.pro_aimbot = process_aimbot(self.is_quit, self.detected_data)

        self.pro_capture.daemon = True
        self.pro_detect.daemon = True
        #self.pro_vsync.daemon = True
        #self.pro_aimbot.daemon = True

        self.pro_capture.start()
        self.pro_detect.start()
        self.pro_vsync.start()
        self.pro_aimbot.start()

        #thr_protect = threading.Thread(target=self.process_protect)
        #thr_protect.setDaemon(True)
        #thr_protect.start()

        # np.frombuffer(self.refresh_rate, dtype=np.uint8)[:] = 100


def init(target, args):
    thread_init = threading.Thread(target=target, args=args)
    thread_init.setDaemon(True)
    thread_init.start()
    while thread_init.is_alive():
        QApplication.processEvents()


def main_window():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Resources/icon/icon.png'))

    SplashWindow = SplashWindowInterface()
    SplashWindow.show()
    window_sleep(0.2)

    load_conf()

    SplashWindow.step(33)
    window_sleep(0.2)

    MainWindow = MainWindowInterface()
    MainWindow.load_config()

    window_sleep(0.2)
    SplashWindow.step(66)

    aim_pro = aimbot_main() #####
    aim_pro.start()

    window_sleep(2)
    SplashWindow.step(99)

    save_thr = threading.Thread(target=MainWindow.auto_update)
    save_thr.setDaemon(True)
    save_thr.start()

    window_sleep(0.25)
    MainWindow.show()
    window_sleep(0.1)
    SplashWindow.close()

    exec_int = app.exec()

    SplashWindow.show()
    SplashWindow.step(99)
    window_sleep(0.2)

    aim_pro.quit()

    SplashWindow.step(50)
    window_sleep(0.4)

    SplashWindow.step(0)
    window_sleep(0.5)

    SplashWindow.close()
    return exec_int


if __name__ == '__main__':
    exit_code = main_window()
    sys.exit(exit_code)
