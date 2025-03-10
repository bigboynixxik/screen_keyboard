class WindowCreators:
    @staticmethod
    def load_splash_screen():
        from mli_keyboard.windows.SplashScreen import SplashScreen
        return SplashScreen()

    @staticmethod
    def load_main_window():
        from mli_keyboard.windows.MainWindow import MainWindow
        return MainWindow()

    @staticmethod
    def load_settings_window(font_family, font_size):
        from mli_keyboard.windows.SettingsWindow import SettingsWindow
        return SettingsWindow(font_family, font_size)

    @staticmethod
    def load_add_button_window(font_family, font_size):
        from mli_keyboard.windows.AddButtonWindow import AddButtonWindow
        return AddButtonWindow(font_family, font_size)