from configparser import ConfigParser

from mli_keyboard.config import BUTTON_SCALE_DEFAULT, PRESS_DELAY_DEFAULT, SETTINGS_FILE_PATH, SETTINGS_LEVEL_SCALE,\
    VOLUME_LEVEL_DEFAULT


def get_settings():
    """Выполняет чтение из файла конфигурации параметров для клавиш

    :return: Коэффициент масштабирования клавиатуры и промежуток задержки перед нажатием клавиши (в милисекундах)
    :rtype: dict
    """
    config = ConfigParser()

    try:
        with open(SETTINGS_FILE_PATH) as f:
            config.read_file(f)

        button_scale = int(config['Buttons']['button_scale'])
        press_delay = int(config['Buttons']['press_delay'])
        volume_level = int(config['Buttons']['volume_level'])

        return {
            'button_scale': button_scale / SETTINGS_LEVEL_SCALE,
            'press_delay': 100000, # press_delay / SETTINGS_LEVEL_SCALE
            'volume_level': volume_level / SETTINGS_LEVEL_SCALE,
        }
    except FileNotFoundError:
        config['Buttons'] = {
            'button_scale': BUTTON_SCALE_DEFAULT,
            'press_delay': PRESS_DELAY_DEFAULT,
            'volume_level': VOLUME_LEVEL_DEFAULT,
        }
        with open(SETTINGS_FILE_PATH, 'w') as f:
            config.write(f)

    return {
        'button_scale': BUTTON_SCALE_DEFAULT / SETTINGS_LEVEL_SCALE,
        'press_delay': PRESS_DELAY_DEFAULT / SETTINGS_LEVEL_SCALE,
        'volume_level': VOLUME_LEVEL_DEFAULT / SETTINGS_LEVEL_SCALE,
    }


def save_settings(button_scale, press_delay, volume_level):
    """Перезаписывает настройки в файл конфигураций

    :param button_scale: Коэффициент масштабирования каждой клавиши
    :type button_scale: float
    :param press_delay: Значение задержки после наведения на клавишу (в секундах)
    :type press_delay: float
    :param volume_level: Уровень громкости нажатия на клавиши
    :type volume_level: float
    """
    config = ConfigParser()

    config['Buttons'] = {
        'button_scale': str(button_scale),
        'press_delay': str(press_delay),
        'volume_level': str(volume_level),
    }

    with open(SETTINGS_FILE_PATH, 'w') as f:
        config.write(f)
