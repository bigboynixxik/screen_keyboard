from mli_keyboard.arrangement.buttons_enum import AuxiliaryKeysEnum, EnglishLangEnum, NumberEnum, RussianLangEnum, \
    UtilityKeysEnum

# Папки
IMAGES_PATH = 'mli_keyboard/resources/images/'
SOUNDS_PATH = 'mli_keyboard/resources/sounds/'

# Размер главного окна
MONITOR_HD_HEIGHT = 1080
INIT_HEIGHT = 720
INIT_WIDTH = 860

# Горизонтальные и вертикальные смещения клавиш
H_OFFSET = 48.888888888888886
V_OFFSET = 73.33333333333333

# Backspace
BACKSPACE_CLICKED_COUNT_1 = 5
BACKSPACE_CLICKED_COUNT_2 = 30
BACKSPACE_SPACE_SPEED_1 = 0.5
BACKSPACE_SPACE_SPEED_2 = 0.1
BACKSPACE_SPACE_SPEED_3 = 0.02

# Вид символов на клавиатуре
DEFAULT_SYMBOL = ''
LETTER_FONT_FAMILY = 'Calibri'
LETTER_FONT_SIZE = 22
UTILITY_FONT_FAMILY = 'Calibri'
BUTTON_X_OFFSET = -18
BUTTON_Y_OFFSET = -2
BACK_COLOR = '#DCFFFF'
BACK_COLOR_LETTER = '#DCFFFF'
BACK_COLOR_UTILITY = '#90efb9'
BACK_COLOR_ARROW = '#52dc8d'
BACK_COLOR_SETTINGS = '#b6d4c3'
BACK_COLOR_ON_CLICK = '#9AF428'
BACKLIGHT_COLOR = '#78FFFF'
BACKLIGHT_COLOR_LETTER = '#78FFFF'
BACKLIGHT_COLOR_UTILITY = '#3b845b'
BACKLIGHT_COLOR_ARROW = '#23804d'
BACKLIGHT_COLOR_SETTINGS = '#6a9182'

ANIMATION_GRADIENT_COUNT = 100
REVERSE_ANIMATION_GRADIENT_COUNT = 100

# Границы клавиш
KEY_BORDER_COLOR = '#2D2E30'
KEY_BORDER_WIDTH = 3

# Перемещение клавиатуры
MOVE_COUNTDOWN_DEFAULT = 300

# Звуки нажатия
SOUND_CLICK_LETTER = SOUNDS_PATH + 'click_letter.wav'
SOUND_CLICK_SPECIAL = SOUNDS_PATH + 'click_special.wav'

# Загрузочный экран
SPLASH_INIT_HEIGHT = 400
SPLASH_INIT_WIDTH = 800

SPLASH_TITLE = 'MLI Keyboard'

SPLASH_LOADING_PROGRESS_START = 0
SPLASH_LOADING_PROGRESS_MIN = 0
SPLASH_LOADING_PROGRESS_MAX = 100
SPLASH_LOADING_TIMEOUT = 100
SPLASH_LOADING_STAGES = 1

SPLASH_LABEL_TITLE_FONT_SIZE = 60
SPLASH_LABEL_TITLE_COLOR = BACK_COLOR_ON_CLICK

SPLASH_LABEL_DESC_FONT_SIZE = 30
SPLASH_LABEL_DESC_COLOR = '#EFEFF1'

SPLASH_LABEL_LOADING_FONT_SIZE = 30
SPLASH_LABEL_LOADING_COLOR = '#EFEFF1'
SPLASH_LABEL_LOADING_TEXT = 'Загрузка...'

SPLASH_BACKGROUND_COLOR = '#2F4454'

SPLASH_PROGRESS_BAR_BACKGROUND_COLOR = '#DEFEFF'
SPLASH_PROGRESS_BAR_COLOR = '#000A0D'
SPLASH_PROGRESS_BAR_FONT_SIZE = 30
SPLASH_PROGRESS_BAR_GRADIENT_START = BACK_COLOR
SPLASH_PROGRESS_BAR_GRADIENT_STOP = BACK_COLOR_ON_CLICK

SPLASH_STYLE_SHEET = f'''
            #label_title {{
                font-size: {SPLASH_LABEL_TITLE_FONT_SIZE}px;
                color: {SPLASH_LABEL_TITLE_COLOR};
            }}

            #label_desc {{
                font-size: {SPLASH_LABEL_DESC_FONT_SIZE}px;
                color: {SPLASH_LABEL_DESC_COLOR};
            }}

            #label_loading {{
                font-size: {SPLASH_LABEL_LOADING_FONT_SIZE}px;
                color: {SPLASH_LABEL_LOADING_COLOR};
            }}

            QFrame {{
                background-color: {SPLASH_BACKGROUND_COLOR};
            }}

            QProgressBar {{
                background-color: {SPLASH_PROGRESS_BAR_BACKGROUND_COLOR};
                font-size: {SPLASH_PROGRESS_BAR_FONT_SIZE}px;
                color: {SPLASH_PROGRESS_BAR_COLOR};
                border-style: none;
                border-radius: 10px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                border-radius: 10px;
                background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523,
                 stop:0 {SPLASH_PROGRESS_BAR_GRADIENT_START}, stop:1 {SPLASH_PROGRESS_BAR_GRADIENT_STOP});
            }}
        '''

# Окно настроек
MILLISECONDS_IN_SECOND = 1000

SETTINGS_DESIGN = 'Settings'
SETTINGS_FILE_PATH = 'settings.ini'
SETTINGS_FONT_FAMILY = 'Calibri'
SETTINGS_FONT_SIZE = 14
SLIDER_MIN_HEIGHT = 30

BUTTON_SCALE_DEFAULT = 100
BUTTON_SCALE_MIN_VALUE = 75
BUTTON_SCALE_MAX_VALUE = 150
BUTTON_SCALE_SINGLE_STEP = 25

PRESS_DELAY_DEFAULT = 100
PRESS_DELAY_MIN_VALUE = 25
PRESS_DELAY_MAX_VALUE = 200
PRESS_DELAY_SINGLE_STEP = 25

VOLUME_LEVEL_DEFAULT = 50
VOLUME_LEVEL_MIN_VALUE = 0
VOLUME_LEVEL_MAX_VALUE = 100

SETTINGS_LEVEL_SCALE = 100

DEFAULT_BUTTON_MIN_HEIGHT = 60
SAVE_BUTTON_MIN_HEIGHT = 60

# Названия настроек
SETTINGS_TITLE = 'Настройки'
SETTINGS_BUTTON_SCALE = 'Масштабирование'
SETTINGS_PRESS_DELAY = 'Задержка перед нажатием'
SETTINGS_VOLUME_LEVEL = 'Уровень громкости'
SETTINGS_SAVE_DESIGN = 'Сохранить'
SETTINGS_QUIT_TITLE = 'Выход'
SETTINGS_GET_DEFAULT_DESIGN = 'По-умолчанию'
SETTINGS_SAVE_CHANGES_QUEST = 'Сохранить изменения?'

# Конфигурации матриц
RU_MATRIX = [
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     RussianLangEnum.H,
     RussianLangEnum.G, RussianLangEnum.EA, RussianLangEnum.YE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.COMMA,
     RussianLangEnum.I_KRATKOE,
     RussianLangEnum.D, RussianLangEnum.M, RussianLangEnum.SHA, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, RussianLangEnum.ERY,
     RussianLangEnum.V,
     RussianLangEnum.O, RussianLangEnum.L, RussianLangEnum.YA, RussianLangEnum.U, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, RussianLangEnum.B,
     RussianLangEnum.P,
     AuxiliaryKeysEnum.INVISIBLE, RussianLangEnum.A, RussianLangEnum.S, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, RussianLangEnum.Y,
     RussianLangEnum.R,
     RussianLangEnum.E, RussianLangEnum.T, RussianLangEnum.SOFT_SIGN, RussianLangEnum.F, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, RussianLangEnum.TS,
     RussianLangEnum.J,
     RussianLangEnum.N, RussianLangEnum.I, RussianLangEnum.K, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     RussianLangEnum.HARD_SIGN,
     RussianLangEnum.Z, RussianLangEnum.CH, RussianLangEnum.SH, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE]
]


EN_MATRIX = [
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     EnglishLangEnum.X,
     EnglishLangEnum.V, EnglishLangEnum.Z, AuxiliaryKeysEnum.QUESTION, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.COMMA,
     EnglishLangEnum.W,
     EnglishLangEnum.Y, EnglishLangEnum.L, AuxiliaryKeysEnum.DOT, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, EnglishLangEnum.H,
     EnglishLangEnum.A,
     EnglishLangEnum.E, EnglishLangEnum.R, EnglishLangEnum.B, AuxiliaryKeysEnum.SEMICOLON, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, EnglishLangEnum.C,
     EnglishLangEnum.T,
     AuxiliaryKeysEnum.INVISIBLE, EnglishLangEnum.I, EnglishLangEnum.D, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, EnglishLangEnum.M,
     EnglishLangEnum.S,
     EnglishLangEnum.O, EnglishLangEnum.N, EnglishLangEnum.K, AuxiliaryKeysEnum.COLON, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.EXCLAMATION,
     EnglishLangEnum.P, EnglishLangEnum.U, EnglishLangEnum.G, EnglishLangEnum.F, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.ROUND_LEFT_BRACKETS, AuxiliaryKeysEnum.ROUND_RIGHT_BRACKETS, EnglishLangEnum.Q,
     EnglishLangEnum.J, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE],
]

SYM_MATRIX = [
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     NumberEnum.ONE,
     NumberEnum.TWO, NumberEnum.THREE, NumberEnum.FOUR, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, NumberEnum.FIVE,
     NumberEnum.SIX,
     NumberEnum.SEVEN, NumberEnum.EIGHT, NumberEnum.NINE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.NUMERO_SIGN,
     AuxiliaryKeysEnum.ROUND_LEFT_BRACKETS, AuxiliaryKeysEnum.ROUND_RIGHT_BRACKETS, AuxiliaryKeysEnum.EXCLAMATION,
     AuxiliaryKeysEnum.QUESTION, NumberEnum.ZERO, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.SQUARE_LEFT_BRACKETS,
     AuxiliaryKeysEnum.SQUARE_RIGHT_BRACKETS, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.COMMA,
     AuxiliaryKeysEnum.DOT, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.CURLY_LEFT_BRACKETS,
     AuxiliaryKeysEnum.CURLY_RIGHT_BRACKETS, AuxiliaryKeysEnum.TILDE, AuxiliaryKeysEnum.VERTICAL_BAR,
     AuxiliaryKeysEnum.DOLLAR, AuxiliaryKeysEnum.AT, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.DOUBLE_QUOTATION,
     AuxiliaryKeysEnum.SINGLE_QUOTATION, AuxiliaryKeysEnum.PLUS, AuxiliaryKeysEnum.EQUAL,
     AuxiliaryKeysEnum.BACKSLASH, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE],
    [AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.LOW_DASH,
     AuxiliaryKeysEnum.MINUS, AuxiliaryKeysEnum.ASTERIKS, AuxiliaryKeysEnum.SLASH, AuxiliaryKeysEnum.INVISIBLE,
     AuxiliaryKeysEnum.INVISIBLE],
]

# Языковые и символьные статусы клавиатуры
DESIGN_RU = 'RU'
DESIGN_EN = 'EN'
DESIGN_OFF = 'OFF'
DESIGN_SYM = 'SYM'

QUEUE_LANG = [DESIGN_RU, DESIGN_EN]
QUEUE_SYM = [DESIGN_OFF, DESIGN_SYM]
LAYOUT_STATUSES_LANG = {DESIGN_RU: RU_MATRIX, DESIGN_EN: EN_MATRIX}
LAYOUT_STATUSES_SYM = {DESIGN_OFF: None, DESIGN_SYM: SYM_MATRIX}

# Координаты и обозначения функциональных клавиш
UTILITY_BUTTONS_CONFIGS = {
    UtilityKeysEnum.SPACE: {'design': 'Пробел', 'font_size': 14, 'coord': (537.7777777777777, 293.3333333333333),
                            'sound_click_path': SOUND_CLICK_LETTER, 'back_color': BACK_COLOR_UTILITY,
                            'backlight_color': BACKLIGHT_COLOR_UTILITY},
    UtilityKeysEnum.BACKSPACE: {'design': '&lt; Back', 'font_size': 14,
                                'coord': (831.1111111111111, 146.66666666666666),
                                'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_UTILITY,
                                'backlight_color': BACKLIGHT_COLOR_UTILITY},
    UtilityKeysEnum.ENTER: {'design': 'Enter', 'font_size': 14, 'coord': (831.1111111111111, 293.3333333333333),
                            'sound_click_path': SOUND_CLICK_LETTER, 'back_color': BACK_COLOR_UTILITY,
                            'backlight_color': BACKLIGHT_COLOR_UTILITY},
    UtilityKeysEnum.CAPSLOCK: {'design': 'Caps', 'font_size': 14, 'coord': (831.1111111111111, 440.0),
                               'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_UTILITY,
                               'backlight_color': BACKLIGHT_COLOR_UTILITY},
    UtilityKeysEnum.SHIFT: {'design': 'Shift', 'font_size': 14, 'coord': (782.2222222222222, 513.3333333333333),
                            'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_UTILITY,
                            'backlight_color': BACKLIGHT_COLOR_UTILITY},
    UtilityKeysEnum.LANG: {'design': QUEUE_LANG[0], 'font_size': 14, 'coord': (293.3333333333333, 73.33333333333333),
                           'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_UTILITY,
                           'backlight_color': BACKLIGHT_COLOR_UTILITY},
    UtilityKeysEnum.SYM: {'design': '?123', 'font_size': 14, 'coord': (782.2222222222222, 73.33333333333333),
                          'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_UTILITY,
                          'backlight_color': BACKLIGHT_COLOR_UTILITY},
    UtilityKeysEnum.SETTINGS: {'design': '⛯', 'font_size': 18, 'coord': (244.44444444444443, 146.66666666666666),
                               'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_SETTINGS,
                               'backlight_color': BACKLIGHT_COLOR_SETTINGS, 'svg': True},
    UtilityKeysEnum.MOVE: {'design': '⇹', 'font_size': 24, 'coord': (293.3333333333333, 513.3333333333333),
                           'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_SETTINGS,
                           'backlight_color': BACKLIGHT_COLOR_SETTINGS},
    UtilityKeysEnum.MINIMIZE: {'design': '⤓', 'font_size': 24, 'coord': (195.55555555555554, 513.3333333333333),
                               'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_SETTINGS,
                               'backlight_color': BACKLIGHT_COLOR_SETTINGS},
    UtilityKeysEnum.EXIT: {'design': '☒', 'font_size': 18, 'coord': (244.44444444444443, 440.0),
                           'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_SETTINGS,
                           'backlight_color': BACKLIGHT_COLOR_SETTINGS},
    UtilityKeysEnum.LEFT: {'design': '←', 'font_size': 14, 'coord': (146.66666666666666, 293.3333333333333),
                           'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_ARROW,
                           'backlight_color': BACKLIGHT_COLOR_ARROW},
    UtilityKeysEnum.RIGHT: {'design': '→', 'font_size': 14, 'coord': (244.44444444444443, 293.3333333333333),
                            'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_ARROW,
                            'backlight_color': BACKLIGHT_COLOR_ARROW},
    UtilityKeysEnum.UP: {'design': '↑', 'font_size': 14, 'coord': (195.55555555555554, 220.0),
                         'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_ARROW,
                         'backlight_color': BACKLIGHT_COLOR_ARROW},
    UtilityKeysEnum.DOWN: {'design': '↓', 'font_size': 14, 'coord': (195.55555555555554, 366.66666666666663),
                           'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_ARROW,
                           'backlight_color': BACKLIGHT_COLOR_ARROW},
    UtilityKeysEnum.PLUS: {'design': '+', 'font_size': 18, 'coord': (835, 513.3333333333333),
                           'sound_click_path': SOUND_CLICK_SPECIAL, 'back_color': BACK_COLOR_SETTINGS,
                           'backlight_color': BACKLIGHT_COLOR_SETTINGS}
}
