import configparser

config = configparser.ConfigParser()

CONFIG_NAME = 'config.ini'
SECTION_NAME = 'data'

config_default = {
    'value_aim_range_general': 50,
    'value_dead_range_general': 25,
    'value_pid_d_general': 50,
    'value_pid_i_general': 50,
    'value_pid_p_general': 50,

    'value_enabled_rifle': 0,
    'value_aim_range_rifle': 50,
    'value_dead_range_rifle': 25,
    'value_pid_d_rifle': 50,
    'value_pid_i_rifle': 50,
    'value_pid_p_rifle': 50,

    'value_enabled_smg': 0,
    'value_aim_range_smg': 50,
    'value_dead_range_smg': 25,
    'value_pid_d_smg': 50,
    'value_pid_i_smg': 50,
    'value_pid_p_smg': 50,

    'value_enabled_sniper': 0,
    'value_aim_range_sniper': 50,
    'value_dead_range_sniper': 25,
    'value_pid_d_sniper': 50,
    'value_pid_i_sniper': 50,
    'value_pid_p_sniper': 50,

    'value_enabled_pistol': 0,
    'value_aim_range_pistol': 50,
    'value_dead_range_pistol': 25,
    'value_pid_d_pistol': 50,
    'value_pid_i_pistol': 50,
    'value_pid_p_pistol': 50,

    'value_max_fps': 120,
    'value_confidence': 50,
    'value_image_size': 20,
    'value_gpu_accel': 0,
    'value_weights': 0,
    'value_capture_target': 0,
    'value_capture_method': 0,

    'value_view_source': 0,

    'value_custom_weights': 'yolov7.pt',
    'value_custom_capture': 'Apex Legends',
    'value_frame_sync': 1,
    'value_unlimited_fps': 0
}

config[SECTION_NAME] = config_default

def get_value(name):
    return config[SECTION_NAME][name]

def set_value(name, value):
    config[SECTION_NAME][name] = str(value)

def save_conf():
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)
    load_conf()
    return

def load_conf():
    if len(config.read(CONFIG_NAME)) == 0:
        with open(CONFIG_NAME, 'w') as configfile:
            config.write(configfile)
    config.read(CONFIG_NAME)
    return

def set_default():
    config[SECTION_NAME] = config_default

'''
MainWindow.ui.value_enabled_pistol.isChecked()
MainWindow.ui.value_capture_method.currentIndex()
MainWindow.ui.value_capture_method.setCurrentIndex(2)
'''

'''
view value
value_fps_core
value_fps_opencv
value_latency_ai
value_latency_capture
value_latency_mouse
'''
