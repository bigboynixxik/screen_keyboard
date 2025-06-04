from mli_keyboard.config import DESIGN_OFF, DESIGN_SYM, QUEUE_LANG, QUEUE_SYM


class FSM:
    """Класс, реализующий конечный детерминированный автомат для работы с переключаемыми состояниями в клавиатуре
    """

    class WindowsGroup:
        """Группа состояний для управления взаимодействием между всеми окнами: загрузочным экраном, главным окном и
        окном настроек
        """
        splash_screen = None
        main_window = None
        settings_window = None
        switch_window = None

        @classmethod
        def start_app(cls, splash_screen):
            """Запускает приложение, запустив, первым шагом, загрузочный экран

            :param splash_screen: Экземпляр загрузочного окна
            :type splash_screen: class:`windows.SplashScreen.SplashScreen`
            """
            cls.splash_screen = splash_screen
            cls.splash_screen.activateWindow()
            cls.splash_screen.show()

        @classmethod
        def from_splash_to_main(cls, main_window):
            """Переключает интерфейс с загрузочного окна на главное окно

            :param main_window: Экземпляр главного окна
            :type main_window: class:`windows.MainWindow.MainWindow`
            """
            cls.main_window = main_window
            cls.main_window.activateWindow()
            cls.main_window.show()
            cls.splash_screen.close()
            cls.splash_screen = None

        @classmethod
        def from_main_to_settings(cls, settings_window):
            """Переключает интерфейс с главного окна на настройки

            :param settings_window: Экземпляр окна с настройками
            :type settings_window: class:`windows.SettingsWindow.SettingsWindow`
            """
            cls.settings_window = settings_window
            cls.main_window.hide()
            cls.settings_window.activateWindow()
            cls.settings_window.show()

        @classmethod
        def from_settings_to_main(cls):
            """Переключает интерфейс с окна настроек на главное окно
            """
            cls.settings_window = None
            cls.main_window.activateWindow()
            cls.main_window.show()

        @classmethod
        def switch_flexibility_buttons(cls):
            cls.main_window.hide()
            cls.main_window.switch_flexibility_buttons()
            cls.main_window.activateWindow()
            cls.main_window.show()

        @classmethod
        def redraw_main(cls):
            """Вызывает перерисовку главного окна
            """
            cls.main_window.redraw_window()

    class LangSymGroup:
        """Группа состояний для изменения раскладки клавиатуры
        """
        lang = QUEUE_LANG[0]
        sym = QUEUE_SYM[0]

        @classmethod
        def get_next_lang(cls):
            """Возвращает обозначение следующего языка по очереди переключения из конфигурационного файла

            :return: Обозначение выбранного языка в двух символах
            :rtype: str
            """
            return QUEUE_LANG[QUEUE_LANG.index(cls.lang) + 1] if QUEUE_LANG.index(cls.lang) + 1 < len(QUEUE_LANG) else \
                QUEUE_LANG[0]

        @classmethod
        def get_prev_lang(cls):
            """Возвращает обозначение предыдущего языка по очереди переключения из конфигурационного файла

            :return: Обозначение выбранного языка в двух символах
            :rtype: str
            """
            return QUEUE_LANG[QUEUE_LANG.index(cls.lang) - 1] if QUEUE_LANG.index(cls.lang) - 1 >= 0 else QUEUE_LANG[-1]

        @classmethod
        def next_lang(cls):
            """Переключает раскладку клавиатуры на следующий по очереди язык
            """
            cls.sym = DESIGN_OFF
            cls.lang = cls.get_next_lang()

        @classmethod
        def next_sym(cls):
            """Переключает раскладку клавиатуры на следующую по очереди символьную раскладку
            """
            if cls.sym == DESIGN_SYM:
                cls.sym = DESIGN_OFF
            else:
                cls.sym = DESIGN_SYM
            cls.lang = cls.get_prev_lang()

    class CapsGroup:
        """Группа состояний для изменения регистра буквенных клавиш на клавиатуре
        """
        shift_pressed = False
        caps_lock_pressed = False

        @classmethod
        def switch_caps(cls):
            """Переключает клавишу Caps Lock
            """
            cls.caps_lock_pressed = not cls.caps_lock_pressed

        @classmethod
        def switch_shift(cls):
            """Переключает клавишу Shift
            """
            cls.shift_pressed = not cls.shift_pressed