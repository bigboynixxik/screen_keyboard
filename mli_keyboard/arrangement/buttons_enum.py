from enum import Enum


class KeysEnum(Enum):
    """Дополнение Enum необходимыми методами
    """
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class RussianLangEnum(KeysEnum):
    """Клавиши букв русского алфавита
    """
    A = 1072
    B = 1073
    V = 1074
    G = 1075
    D = 1076
    E = 1077
    J = 1078
    Z = 1079
    I = 1080
    I_KRATKOE = 1081
    K = 1082
    L = 1083
    M = 1084
    N = 1085
    O = 1086
    P = 1087
    R = 1088
    S = 1089
    T = 1090
    Y = 1091
    F = 1092
    H = 1093
    TS = 1094
    CH = 1095
    SH = 1096
    SHA = 1097
    HARD_SIGN = 1098
    ERY = 1099
    SOFT_SIGN = 1100
    EA = 1101
    U = 1102
    YA = 1103
    YE = 1105


class EnglishLangEnum(KeysEnum):
    """Клавиши букв английского алфавита
    """
    A = 97
    B = 98
    C = 99
    D = 100
    E = 101
    F = 102
    G = 103
    H = 104
    I = 105
    J = 106
    K = 107
    L = 108
    M = 109
    N = 110
    O = 111
    P = 112
    Q = 113
    R = 114
    S = 115
    T = 116
    U = 117
    V = 118
    W = 119
    X = 120
    Y = 121
    Z = 122


class NumberEnum(KeysEnum):
    """Клавиши цифр
    """
    ZERO = 48
    ONE = 49
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57


class AuxiliaryKeysEnum(KeysEnum):
    """Клавиши вспомогательных символов
    """
    INVISIBLE = -1
    SPACE = 32
    EXCLAMATION = 33
    DOUBLE_QUOTATION = 34
    HASHTAG = 35
    DOLLAR = 36
    PERCENT = 37
    AMPERSAND = 38
    SINGLE_QUOTATION = 39
    ROUND_LEFT_BRACKETS = 40
    ROUND_RIGHT_BRACKETS = 41
    ASTERIKS = 42
    PLUS = 43
    COMMA = 44
    MINUS = 45
    DOT = 46
    SLASH = 47
    COLON = 58
    SEMICOLON = 59
    LESS_THAN = 60
    EQUAL = 61
    MORE_THAN = 62
    QUESTION = 63
    AT = 64
    SQUARE_LEFT_BRACKETS = 91
    BACKSLASH = 92
    SQUARE_RIGHT_BRACKETS = 93
    CIRCUMFLEX = 94
    LOW_DASH = 95
    APOSTROPHE = 96
    CURLY_LEFT_BRACKETS = 123
    VERTICAL_BAR = 124
    CURLY_RIGHT_BRACKETS = 125
    TILDE = 126
    DELETE = 127
    LONG_MINUS = 8211
    EURO = 8364
    NUMERO_SIGN = 8470


class UtilityKeysEnum(KeysEnum):
    """Функциональные клавиши
    """
    SPACE = 'space'
    BACKSPACE = 'backspace'
    ENTER = 'enter'
    CAPSLOCK = 'capslock'
    SHIFT = 'shift'
    LANG = 'lang'
    SYM = 'sym'
    SETTINGS = 'settings'
    MOVE = 'move'
    MINIMIZE = 'minimize'
    EXIT = 'exit'
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
    PLUS = 43
